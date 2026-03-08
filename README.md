# Build Your Own Coding Agent

A practical, hands-on guide to open-source AI coding assistants: from choosing the right model to building a working agent from scratch.

## Who Is This For?

Tech-savvy professionals who want to understand and use AI coding agents without relying on closed-source tools. No ML background required; if you know what `pip install` and `git` do, you're good.

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

## Hardware Requirements

Running LLMs locally requires more resources than a typical development setup. Here's what you need depending on which model you want to run:

| Model size | RAM | GPU VRAM | Example hardware | Speed |
|-----------|-----|----------|-----------------|-------|
| **7B** (Q4 quantized) | 8 GB | 6 GB | Any modern laptop | ~30 tokens/sec |
| **13B** (Q4) | 16 GB | 10 GB | Gaming laptop / desktop | ~20 tokens/sec |
| **32B** (Q4) | 32 GB | 24 GB | RTX 4090 / Mac M2 Pro (32GB) | ~15 tokens/sec |
| **70B** (Q4) | 64 GB | 48 GB | 2x RTX 4090 / Mac M2 Ultra | ~8 tokens/sec |

**Key notes:**

- **No GPU? No problem.** Both Ollama and LM Studio can run models on CPU only — it's just slower (roughly 3-5x). A 7B model on a modern laptop CPU is still usable.
- **Apple Silicon is great for this.** M1/M2/M3/M4 Macs use unified memory (RAM = VRAM), so a MacBook Pro with 32GB can comfortably run 32B models. This is one of the best price/performance setups for local LLMs.
- **Quantization matters.** A "Q4" (4-bit quantized) model uses ~4x less memory than the full-precision version with minimal quality loss. All models on Ollama are quantized by default.
- **Start small.** A 7B model on 8GB RAM is enough to follow this entire guide and build a working agent. Scale up once you've validated the workflow.

> **Don't have the hardware?** You can skip local inference entirely and use API-based models (see the guide's [API section](#configuration)). You can also use free-tier GPU providers like [Google Colab](https://colab.google) or [Lightning AI](https://lightning.ai) to run larger models remotely.

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
