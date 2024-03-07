# Asynchronous API for DeepL Translator

It also shipped with a simple command line interface.

## Installation

```bash
pip install -U aiodeepl
```

## API Usage

Documentation is yet complete. Apart from the following example, you can also refer to the `__main__.py` file for more examples.

```python
import aiodeepl

async def main():
    translator = aiohttp.Translator(api_key="123")
    result = await translator.translate("Hello, World!", target_lang="DE")
    print(result)
```

## CLI Usage

```bash
aiodeepl --api-key 123 -t "Hello, World!" -d DE
```

You can save `api_key` in config file or input it interactively for security.

To translate a document, you can use the following command:

```bash
aiodeepl --api-key 123 -f README.pdf -d DE -o README_DE.pdf
```
