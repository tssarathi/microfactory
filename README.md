# microfactory

## Prerequisites (macOS)

- [uv](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Ollama](https://ollama.com/download): `curl -fsSL https://ollama.com/install.sh | sh`

## Setup

Pull the model:

```bash
ollama pull qwen3.5:9b
```

## Running

Start the Ollama server:

```bash
ollama serve
```

In a separate terminal, run the app:

```bash
uv run python main.py
```
