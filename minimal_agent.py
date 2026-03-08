"""
minimal_agent.py — A bare-bones coding agent using a local LLM via Ollama.

Usage:
    1. Install Ollama: https://ollama.com
    2. Pull a model: ollama pull qwen2.5-coder:7b
    3. Start Ollama: ollama serve
    4. pip install openai rich
    5. python minimal_agent.py

The agent can read/write files, list directories, search code, and run shell commands.
"""

import json
import subprocess
import os
import glob as glob_module
from openai import OpenAI

# ── Configuration ──────────────────────────────────────────────────────
MODEL = os.environ.get("AGENT_MODEL", "qwen2.5-coder:7b")
BASE_URL = os.environ.get("AGENT_BASE_URL", "http://localhost:11434/v1")
API_KEY = os.environ.get("AGENT_API_KEY", "ollama")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# ── Tool Definitions ──────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative file path"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and folders in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path (default: current directory)"}
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command and return its output. Use for running tests, git, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Creates the file if it doesn't exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to write to"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Find files matching a glob pattern (e.g., '**/*.py').",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern"},
                    "path": {"type": "string", "description": "Root directory (default: '.')"},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep_code",
            "description": "Search for a text pattern in file contents. Returns matching lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Search pattern"},
                    "path": {"type": "string", "description": "Directory to search in"},
                    "file_type": {"type": "string", "description": "File extension filter (e.g., 'py')"},
                },
                "required": ["pattern"],
            },
        },
    },
]


# ── Tool Implementations ─────────────────────────────────────────────

def read_file(path: str) -> str:
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        return f"Error: File not found: {path}"
    try:
        with open(path, "r") as f:
            content = f.read()
        if len(content) > 10_000:
            return content[:10_000] + f"\n\n... [truncated, file is {len(content)} chars]"
        return content
    except Exception as e:
        return f"Error reading file: {e}"


def list_directory(path: str = ".") -> str:
    path = path or "."
    try:
        entries = sorted(os.listdir(path))
        result = []
        for entry in entries:
            full = os.path.join(path, entry)
            marker = "/" if os.path.isdir(full) else ""
            result.append(f"  {entry}{marker}")
        return f"Contents of {os.path.abspath(path)}:\n" + "\n".join(result)
    except Exception as e:
        return f"Error: {e}"


def run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30,
        )
        output = result.stdout + result.stderr
        if len(output) > 5_000:
            output = output[:5_000] + "\n... [truncated]"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error: {e}"


def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def search_files(pattern: str, path: str = ".") -> str:
    try:
        matches = sorted(glob_module.glob(pattern, root_dir=path or ".", recursive=True))
        if not matches:
            return f"No files matching '{pattern}'"
        result = matches[:50]
        output = f"Files matching '{pattern}':\n"
        output += "\n".join(f"  {m}" for m in result)
        if len(matches) > 50:
            output += f"\n  ... and {len(matches) - 50} more"
        return output
    except Exception as e:
        return f"Error: {e}"


def grep_code(pattern: str, path: str = ".", file_type: str = "") -> str:
    cmd = f'grep -rn "{pattern}" "{path or "."}"'
    if file_type:
        cmd += f' --include="*.{file_type}"'
    cmd += " | head -30"
    return run_command(cmd)


TOOL_MAP = {
    "read_file": read_file,
    "list_directory": list_directory,
    "run_command": run_command,
    "write_file": write_file,
    "search_files": search_files,
    "grep_code": grep_code,
}


# ── Agent Loop ────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful coding assistant with access to the local filesystem.
You can read files, list directories, write files, search for files, grep code, and run shell commands.
Always read relevant files before making changes. Think step by step.
When editing code, write the complete updated file."""


def run_agent():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"\n  Coding Agent  (model: {MODEL})")
    print(f"  Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        while True:
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=TOOLS,
                    temperature=0.1,
                )
            except Exception as e:
                print(f"\n  Error calling LLM: {e}")
                print("  Make sure Ollama is running: ollama serve\n")
                messages.pop()  # Remove failed user message
                break

            choice = response.choices[0]
            message = choice.message

            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)

                    print(f"  [{fn_name}({fn_args})]")

                    if fn_name in TOOL_MAP:
                        result = TOOL_MAP[fn_name](**fn_args)
                    else:
                        result = f"Error: Unknown tool '{fn_name}'"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
                continue
            else:
                print(f"\nAgent: {message.content}\n")
                messages.append({"role": "assistant", "content": message.content})
                break


if __name__ == "__main__":
    run_agent()
