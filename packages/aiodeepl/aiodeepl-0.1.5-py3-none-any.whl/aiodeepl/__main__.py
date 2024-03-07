import argparse
import asyncio
import urllib.request
import sys
from pathlib import Path
from getpass import getpass
from aiodeepl import __author__, __version__
from aiodeepl import Translator, Language, FileStatus
from platformdirs import user_config_dir

CONFIG_VERSION = "1.0.0"


async def main() -> int:
    parser = argparse.ArgumentParser(description="aiodeepl")
    config_dir = Path(user_config_dir(
        "aiodeepl", __author__, CONFIG_VERSION, ensure_exists=True))
    default_config_path = config_dir / "config.json"

    parser.add_argument("-c", "--config", help="Path to the config file",
                        default=default_config_path)
    parser.add_argument("-k", "--key", help="Your DeepL API key", default=None)
    parser.add_argument(
        "-q", "--quota", help="Return your DeepL API quota", action="store_true")
    parser.add_argument("-l", "--languages", help=f"Return a list of supported languages from server, e.g. [{
        ", ".join(l.value for l in Language)}]", action="store_true")
    parser.add_argument("-t", "--text", help="The text to translate", default=None)
    parser.add_argument("-s", "--sauce", help="The source language", default=None)
    parser.add_argument("-d", "--dest", help="The destination language")
    parser.add_argument("-f", "--file", help="The file to translate", default=None)
    parser.add_argument("-o", "--output", help="The file to output to", default=None)
    parser.add_argument("-V", "--version", action="store_true",
                        help="Print the version and exit")

    args = parser.parse_args()

    if args.version:
        print(f"aiodeepl {__version__}")
        return 0

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found at {config_path}")
        api_key = args.key or getpass("Enter your DeepL API key: ")
        translator = Translator(api_key=api_key)
        if input("Do you want to save this key to config? (Y/n) ").strip().lower() or 'y' == 'y':
            config_path.write_text(translator.model_dump_json())
            print(f"Config written to {config_path}")
    else:
        translator = Translator.model_validate_json(config_path.read_text())
        translator.api_key = (args.key
                              or translator.api_key
                              or getpass("Enter your DeepL API key: "))

    system_proxies = urllib.request.getproxies()
    proxy = system_proxies.get("http", system_proxies.get("https"))
    if proxy:
        translator.proxy = proxy

    if args.quota:
        quota = await translator.usage_get()
        print(f"Used: {quota.character_count}, Limit: {quota.character_limit}")
        return 0

    if args.languages:
        srcl = await translator.language_available_get("source")
        destl = await translator.language_available_get("target")
        print("Source languages:")
        for lang in srcl:
            print(f"\t{lang.language:5} - {lang.name:10}")
        print("\nDestination languages:")
        for lang in destl:
            print(
                f"\t{lang.language:5} - {lang.name:10}{
                    f", supports formality"
                    if lang.supports_formality else ''}")
        print("\nGlossary pairs:")
        for i, pair in enumerate(
                await translator.glossary_available_pairs()):
            print(f"({pair.source_lang} -> {pair.target_lang})", end=", ")
            if i % 5 == 4:
                print()
        return 0

    if args.file is None:
        text = sys.stdin.read() if args.text is None else args.text
    elif args.output is None:
        print("You must specify an output file")
        return 2

    if text:
        res = await translator.translate(text, source_lang=args.sauce, target_lang=args.dest)
        print(res.text)
    elif args.file:
        def cb(status: FileStatus):
            match status.status:
                case "translating":
                    print(f"Translating {status.seconds_remaining}s to finish")
                case "done":
                    print("Translation done")
                case "error":
                    print(f"Error: {status.message}")
                case "queued":
                    print("Waiting for queue")
        file_path = Path(args.file)
        try:
            data = file_path.read_bytes()
        except FileNotFoundError:
            print(f"File not found: {args.file}")
            return 2
        out_path = Path(args.output)
        out = await translator.translate_file(
            data,
            filename=file_path.name,
            source_lang=args.sauce, target_lang=args.dest,
            output_format=out_path.suffix[1:] or file_path.suffix[1:] or "pdf",
            status_callback=cb)
        out_path.write_bytes(out)
        print(f"Output written to {out_path}")
    else:
        print("You must specify either text or file")
        return 2

    return 0

sys.exit(asyncio.run(main()))
