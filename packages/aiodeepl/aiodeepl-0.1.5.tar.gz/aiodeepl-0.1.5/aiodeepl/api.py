"""
DeepL API wrapper for Python.
"""

from __future__ import annotations
import asyncio
import httpx
import ujson as json
from enum import Enum
from typing import Any, overload, Literal, Iterable, Callable
from datetime import datetime
from io import BytesIO
from pathlib import Path
from pydantic import BaseModel, ConfigDict, model_validator, PrivateAttr
from pydantic import ValidationError, field_validator
from vermils.io import aio
from . import exc

DEFAULT_FREE_HOST = "api-free.deepl.com"
DEFAULT_PRO_HOST = "api.deepl.com"

MAX_BODY_BYTES = 128 * 1024  # 128 KiB


class Language(str, Enum):
    AR = "AR"
    """Arabic"""
    BG = "BG"
    """Bulgarian"""
    CS = "CS"
    """Czech"""
    DA = "DA"
    """Danish"""
    DE = "DE"
    """German"""
    EL = "EL"
    """Greek"""
    EN = "EN"
    """English (unspecified variant for backward compatibility; please select EN-GB or EN-US instead)"""
    EN_GB = "EN-GB"
    """English (British)"""
    EN_US = "EN-US"
    """English (American)"""
    ES = "ES"
    """Spanish"""
    ET = "ET"
    """Estonian"""
    FI = "FI"
    """Finnish"""
    FR = "FR"
    """French"""
    HU = "HU"
    """Hungarian"""
    ID = "ID"
    """Indonesian"""
    IT = "IT"
    """Italian"""
    JA = "JA"
    """Japanese"""
    KO = "KO"
    """Korean"""
    LT = "LT"
    """Lithuanian"""
    LV = "LV"
    """Latvian"""
    NB = "NB"
    """Norwegian (Bokmål)"""
    NL = "NL"
    """Dutch"""
    PL = "PL"
    """Polish"""
    PT = "PT"
    """Portuguese (unspecified variant for backward compatibility; please select PT-BR or PT-PT instead)"""
    PT_BR = "PT-BR"
    """Portuguese (Brazilian)"""
    PT_PT = "PT-PT"
    """Portuguese (all Portuguese varieties excluding Brazilian Portuguese)"""
    RO = "RO"
    """Romanian"""
    RU = "RU"
    """Russian"""
    SK = "SK"
    """Slovak"""
    SL = "SL"
    """Slovenian"""
    SV = "SV"
    """Swedish"""
    TR = "TR"
    """Turkish"""
    UK = "UK"
    """Ukrainian"""
    ZH = "ZH"
    """Chinese (simplified)"""


class LangInfo(BaseModel):
    model_config = ConfigDict(extra="allow")
    language: str
    name: str
    supports_formality: bool | None = None


class GlossaryPair(BaseModel):
    source_lang: Language | str
    target_lang: Language | str

    @field_validator("source_lang", "target_lang", mode="after")
    def to_upper(cls, v: str | Language):
        if isinstance(v, Language):
            v = v.value
        return v.upper()

    def __eq__(self, other):
        if not isinstance(other, GlossaryPair | tuple):
            return NotImplemented
        if not isinstance(other, tuple):
            other = (other.source_lang, other.target_lang)
        return (self.source_lang, self.target_lang) == other


class GlossaryRequest(GlossaryPair):
    name: str
    entries: str | None = None
    entries_format: Literal["tsv", "csv"] | None = None


class GlossaryResponse(GlossaryPair):
    model_config = ConfigDict(extra="allow")
    name: str
    glossary_id: str
    ready: bool
    creation_time: datetime
    entry_count: int


class Usage(BaseModel):
    model_config = ConfigDict(extra="allow")
    character_count: int
    character_limit: int


class TextRequest(BaseModel):
    """Check https://developers.deepl.com/docs/api-reference/translate#request-body-descriptions"""
    model_config = ConfigDict(
        use_enum_values=True, validate_assignment=True)
    text: list[str]
    """The text to translate."""
    target_lang: Language | str
    """The target language to translate to."""
    source_lang: Language | str | None = None
    """The source language of the text."""
    context: str | None = None
    """The context of the text."""
    split_sentences: Literal['0', '1', "nonewlines"] | None = None
    """Whether to split the input into sentences."""
    preserve_formatting: bool | None = None
    """Keeps punctuation, upper/lower case... etc"""
    formality: Literal["default", "more", "prefer_more",
                       "less", "prefer_less"] | None = None
    tagged_handling: Literal["xml", "html"] | None = None
    """Whether the input text is tagged HTML/XML. Default split_sentences to nonewlines."""
    glossary_id: str | None = None
    outline_detection: bool | None = None
    """Whether to use default outline detection for HTML/XML splitting"""
    non_splitting_tags: list[str] | None = None
    splitting_tags: list[str] | None = None
    ignore_tags: list[str] | None = None

    @model_validator(mode="after")
    def post_check(self):
        if self.glossary_id is not None:
            if self.source_lang is None:
                raise ValueError(
                    "source_lang is required when glossary_id is present")
        return self


class TextResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    text: str
    detected_source_language: str | None = None


class FileStatus(BaseModel):
    model_config = ConfigDict(extra="allow")
    document_id: str
    status: Literal["queued", "translating", "done", "error"]
    seconds_remaining: int | None = None
    billed_characters: int | None = None
    message: str | None = None


class FileResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    document_id: str
    document_key: str


class Translator(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True, validate_assignment=True)
    api_key: str
    use_pro: bool = False
    free_host: str | None = None
    pro_host: str | None = None

    proxy: str | None = None
    retries: int = 3
    timeout: float | None = 10.0

    _cli: httpx.AsyncClient = PrivateAttr(default=None)

    @property
    def host(self):
        return self.pro_host if self.use_pro else self.free_host

    def respawn_cli(self, **kw):
        self._cli = httpx.AsyncClient(
            proxy=self.proxy, timeout=self.timeout,
            trust_env=False, **kw)

    @model_validator(mode="after")
    def post_init(self):
        if self.free_host is None:
            self.free_host = DEFAULT_FREE_HOST
        if self.pro_host is None:
            self.pro_host = DEFAULT_PRO_HOST

        self.respawn_cli()
        return self

    @overload
    async def translate(
        self,
        text: str,
        target_lang: Language | str,
        source_lang: Language | str | None = None,
        context: str | None = None,
        split_sentences: Literal['0', '1', "nonewlines"] | None = None,
        preserve_formatting: bool | None = None,
        formality: Literal["default", "more", "prefer_more",
                           "less", "prefer_less"] | None = None,
        tagged_handling: Literal["xml", "html"] | None = None,
        glossary_id: str | None = None,
        outline_detection: bool | None = None,
        non_splitting_tags: list[str] | None = None,
        splitting_tags: list[str] | None = None,
        ignore_tags: list[str] | None = None,
    ) -> TextResponse: ...

    @overload
    async def translate(
        self,
        text: list[str] | tuple[str, ...] | TextRequest,
        target_lang: Language | str,
        source_lang: Language | str | None = None,
        context: str | None = None,
        split_sentences: Literal['0', '1', "nonewlines"] | None = None,
        preserve_formatting: bool | None = None,
        formality: Literal["default", "more", "prefer_more",
                           "less", "prefer_less"] | None = None,
        tagged_handling: Literal["xml", "html"] | None = None,
        glossary_id: str | None = None,
        outline_detection: bool | None = None,
        non_splitting_tags: list[str] | None = None,
        splitting_tags: list[str] | None = None,
        ignore_tags: list[str] | None = None,
    ) -> list[TextResponse]: ...

    async def translate(
        self,
        text: str | list[str] | tuple[str, ...] | TextRequest,
        target_lang: Language | str,
        source_lang: Language | str | None = None,
        context: str | None = None,
        split_sentences: Literal['0', '1', "nonewlines"] | None = None,
        preserve_formatting: bool | None = None,
        formality: Literal["default", "more", "prefer_more",
                           "less", "prefer_less"] | None = None,
        tagged_handling: Literal["xml", "html"] | None = None,
        glossary_id: str | None = None,
        outline_detection: bool | None = None,
        non_splitting_tags: list[str] | None = None,
        splitting_tags: list[str] | None = None,
        ignore_tags: list[str] | None = None,
    ) -> TextResponse | list[TextResponse]:
        """Check https://developers.deepl.com/docs/api-reference/translate#request-body-descriptions"""
        str_input = False
        if not isinstance(text, TextRequest):
            if isinstance(text, str):
                text = [text]
                str_input = True
            text = TextRequest(
                text=text,
                target_lang=target_lang,
                source_lang=source_lang,
                context=context,
                split_sentences=split_sentences,
                preserve_formatting=preserve_formatting,
                formality=formality,
                tagged_handling=tagged_handling,
                glossary_id=glossary_id,
                outline_detection=outline_detection,
                non_splitting_tags=non_splitting_tags,
                splitting_tags=splitting_tags,
                ignore_tags=ignore_tags,
            )
        req = httpx.Request(
            "POST",
            f"https://{self.host}/v2/translate",
            headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
            json=text.model_dump(exclude_none=True),
        )

        if len(req.content) > MAX_BODY_BYTES:
            raise ValueError("Request body is too large, reduce text size!")

        r = await self._api_call(req)

        try:
            ret = [TextResponse.model_validate(t)
                   for t in json.loads(r.text)["translations"]]
            return ret[0] if str_input else ret
        except (ValidationError, KeyError, IndexError) as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def translate_file(
        self,
        file: bytes | BytesIO | Path | str,
        target_lang: Language | str,
        source_lang: Language | str | None = None,
        filename: str | None = None,
        formality: Literal["default", "more", "less",
                           "prefer_more", "prefer_less"] = "default",
        glossary_id: str | None = None,
        output_format: str | None = None,
        status_callback: Callable[[FileStatus], Any] | None = None,
    ) -> bytes:
        """Check https://developers.deepl.com/docs/api-reference/document"""
        if isinstance(file, (Path, str)):
            if not await aio.path.exists(file):
                raise FileNotFoundError(file)
            filename = filename or Path(file).name
            async with aio.open(file, "rb") as f:
                file = await f.read()

        if filename is None:
            raise ValueError("filename is required when file is not a Path")

        data = {
            "target_lang": target_lang,
            "source_lang": source_lang,
            "formality": formality,
            "glossary_id": glossary_id,
            "output_format": output_format,
        }
        for k, v in data.copy().items():
            if v is None:
                del data[k]

        # Upload the file
        r = await self._api_call(
            data,
            "/v2/document",
            files={"file": (filename, file)},
            as_json=False,
        )
        try:
            fr = FileResponse.model_validate(json.loads(r.text))

            # Poll status until done
            while True:
                await asyncio.sleep(1)
                r = await self._api_call(
                    {"document_key": fr.document_key},
                    f"/v2/document/{fr.document_id}",
                )
                status = FileStatus.model_validate(json.loads(r.text))
                if status_callback is not None:
                    status_callback(status)
                match status.status:
                    case "done":
                        break
                    case "error":
                        raise RuntimeError(status.message)
                    case "translating" | "queued":
                        ...
                    case _:
                        raise RuntimeError(f"Unexpected status {status.status}")

            # Download the result
            r = await self._api_call(
                {"document_key": fr.document_key},
                f"/v2/document/{fr.document_id}/result",
            )
            return r.content

        except ValidationError as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def usage_get(self) -> Usage:
        r = await self._api_call(None, "/v2/usage")
        try:
            return Usage.model_validate(json.loads(r.text))
        except ValidationError as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def language_available_get(
            self, type: Literal["source", "target"]) -> list[LangInfo]:
        r = await self._api_call(None, "/v2/languages", params={"type": type})
        try:
            return list(LangInfo.model_validate(x) for x in json.loads(r.text))
        except ValidationError as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def glossary_available_pairs(self) -> tuple[GlossaryPair, ...]:
        """List all available language pairs for glossaries."""
        r = await self._api_call(
            None, "/v2/glossary-language-pairs"
        )
        try:
            return tuple(
                GlossaryPair.model_validate(x)
                for x in json.loads(r.text)["supported_languages"])
        except (KeyError, ValidationError) as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def glossary_create(
        self,
        name: str,
        source_lang: Language | str,
        target_lang: Language | str,
        entries: str | Iterable[tuple[str, str]],
        entries_format: Literal["csv", "tsv"] = "tsv",
    ) -> GlossaryResponse:
        if isinstance(source_lang, Language):
            source_lang = source_lang.value
        if isinstance(target_lang, Language):
            target_lang = target_lang.value
        if not isinstance(entries, str):
            sep = '\t' if entries_format == "tsv" else ','
            entries = '\n'.join(f"{src}{sep}{tgt}" for src, tgt in entries)
        r = await self._api_call(
            {
                "name": name,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "entries": entries,
                "entries_format": entries_format,
            },
            "/v2/glossaries",
        )
        try:
            return GlossaryResponse.model_validate(json.loads(r.text))
        except ValidationError as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def glossary_list(self) -> list[GlossaryResponse]:
        r = await self._api_call(None, "/v2/glossaries")
        try:
            return list(GlossaryResponse.model_validate(x)
                        for x in json.loads(r.text)["glossaries"])
        except (KeyError, ValidationError) as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def glossary_get_info(self, glossary_id: str) -> GlossaryResponse:
        r = await self._api_call(None, f"/v2/glossaries/{glossary_id}")
        try:
            return GlossaryResponse.model_validate(json.loads(r.text))
        except ValidationError as e:
            raise RuntimeError(f"Invalid response from server {r.text}") from e

    async def glossary_get_entries(
        self,
        glossary_id: str,
        entries_format: Literal["text/tab-separated-values"] = "text/tab-separated-values"
    ) -> list[tuple[str, str]]:
        r = await self._api_call(None, f"/v2/glossaries/{glossary_id}/entries",
                                 headers={"Accept": entries_format})
        try:
            if entries_format == "text/tab-separated-values":
                sep = '\t'
            else:
                sep = ','
            ret = []
            for l in r.text.splitlines():
                splits = l.split(sep, 1)
                ret.append((splits[0], splits[1]))  # make sure there are only 2 splits
            return ret
        except KeyError as e:
            raise RuntimeError(
                f"Invalid response from server {r.text}") from e

    async def glossary_delete(self, glossary_id: str) -> None:
        await self._api_call(
            None, f"/v2/glossaries/{glossary_id}", "DELETE")

    async def _api_call(
            self,
            req: dict | httpx.Request | None,
            path: str | None = None,
            method: str | None = None,
            headers: dict[str, str] | None = None,
            params: dict[str, Any] | None = None,
            files: dict[str, Any] | None = None,
            as_json: bool = True,
    ) -> httpx.Response:
        """Make an API call."""
        if not isinstance(req, httpx.Request):
            if path is None:
                raise ValueError("path is required when req is a dict")
            req = httpx.Request(
                method or ("POST" if req is not None else "GET"),
                f"https://{self.host}{path}",
                headers={
                    "Authorization": f"DeepL-Auth-Key {self.api_key}",
                    **(headers or {})},
                params=params,
                json=req if as_json else None,
                data=req if not as_json else None,
                files=files,
            )
        retry = 0
        sleep_time = 1.0
        backoff = 1.5
        while True:
            try:
                r = await self._cli.send(req)

                if r.status_code == 429:
                    raise exc.TooManyRequests()
                elif r.status_code == 456:
                    raise exc.QuotaExceeded()
                elif r.status_code >= 500 and r.status_code < 600:
                    raise exc.BackendError()
                r.raise_for_status()

                return r
            except (exc.TooManyRequests, exc.BackendError):
                if retry < self.retries:
                    retry += 1
                    await asyncio.sleep(sleep_time)
                    sleep_time *= backoff
                    continue
                raise
            except httpx.HTTPStatusError as e:
                raise RuntimeError(
                    f"When {req.method} to {req.url} got {e}") from e
