# Build Your Own Coding Agent

A practical, hands-on guide to open-source AI coding assistants — from choosing the right model to building a working agent from scratch.

## Who Is This For?

Tech-savvy professionals who want to understand and use AI coding agents without relying on closed-source tools. No ML background required — if you know what `pip install` and `git` do, you're good.

## What's Covered

| Topic | What You'll Learn |
|-------|-------------------|
| **Architecture** | How every coding agent works under the hood (LLM + tools + agent loop) |
| **Model Selection** | How to browse Hugging Face, read model cards, and interpret benchmarks (SWE-bench, BigCodeBench, HumanEval+) |
| **Local Inference** | Setting up [Ollama](https://ollama.com) (CLI) and [LM Studio](https://lmstudio.ai) (GUI) to run models on your machine |
| **Build from Scratch** | A complete ~150-line Python coding agent with file I/O, shell execution, and code search |
| **Ready-Made Tools** | Using [Aider](https://aider.chat), [SWE-agent](https://swe-agent.com), and [OpenCode](https://opencode.ai) with local or API models |
| **API Models** | When and how to use Claude, GPT-4.1, DeepSeek, and Gemini |
| **Security** | Sandboxing, path restrictions, command allowlisting |

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) or [LM Studio](https://lmstudio.ai) installed
- A coding model pulled locally (e.g., `ollama pull qwen2.5-coder:7b`)

### Run the Minimal Agent

```bash
pip install openai
python minimal_agent.py
```

This starts an interactive terminal agent that can read/write files, run commands, and search your codebase — all powered by a local model.

### Render the Guide

The guide is written as a [Quarto](https://quarto.org) document. To render it:

```bash
# HTML (recommended)
quarto render coding-agents-guide.qmd --to html

# PDF
quarto render coding-agents-guide.qmd --to pdf
```

Pre-rendered versions (`coding-agents-guide.html`, `coding-agents-guide.pdf`) are included in the repo.

## Project Structure

```
coding-agents-guide/
├── README.md                      # This file
├── coding-agents-guide.qmd        # The full guide (Quarto source)
├── coding-agents-guide.html       # Pre-rendered HTML
├── coding-agents-guide.pdf        # Pre-rendered PDF
└── minimal_agent.py               # Standalone runnable agent
```

## Configuration

The minimal agent can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_MODEL` | `qwen2.5-coder:7b` | Model name (must be available in your runtime) |
| `AGENT_BASE_URL` | `http://localhost:11434/v1` | API endpoint (Ollama default) |
| `AGENT_API_KEY` | `ollama` | API key (not needed for local models) |

To use LM Studio instead of Ollama:

```bash
AGENT_BASE_URL=http://localhost:1234/v1 AGENT_API_KEY=lm-studio python minimal_agent.py
```

## License

MIT
