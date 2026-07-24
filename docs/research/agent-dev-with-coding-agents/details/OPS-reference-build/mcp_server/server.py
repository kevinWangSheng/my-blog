"""Minimal MCP server exposing expense-agent's three tools over stdio.

Run as a Claude Code MCP server so the tools surface as
mcp__expense__expense_ocr_extract etc. and become matchable by the
.claude/settings.json permission rules.

MCP tool spec (name / description / inputSchema) mirrors the strict schemas in
src/tools/schemas.py one-to-one. Tool names use underscores (no dots) so they
satisfy both the Messages API name regex AND the Claude Code MCP tool-segment
convention. Requires: python -m pip install "mcp".

Register in .mcp.json (project root):
  {"mcpServers": {"expense": {"command": "python",
    "args": ["mcp_server/server.py"]}}}

Smoke-test note: `_tool_list()` is a PLAIN (non-decorated) helper. The
@app.list_tools() decorator wraps a handler whose return type / awaitability is
an implementation detail of the installed `mcp` SDK version, so calling the
decorated function directly can raise even when `mcp` is installed. The smoke
test asserts on `_tool_list()` instead, which is import-only and SDK-version
independent.
"""

from __future__ import annotations

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from src.tools.fx_rate import fx_rate
from src.tools.ocr_extract import ocr_extract
from src.tools.post_ledger_entry import post_ledger_entry
from src.tools.schemas import (
    FX_RATE_TOOL,
    OCR_EXTRACT_TOOL,
    POST_LEDGER_ENTRY_TOOL,
)

app = Server("expense")


def _tool_list() -> list[Tool]:
    """Plain helper: build the MCP Tool list from the strict schemas.

    Both the @app.list_tools() handler and the smoke test call this, so the
    smoke test never depends on the SDK decorator's calling convention.
    """
    return [
        Tool(
            name=t["name"],
            description=t["description"],
            inputSchema=t["input_schema"],
        )
        for t in (OCR_EXTRACT_TOOL, FX_RATE_TOOL, POST_LEDGER_ENTRY_TOOL)
    ]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return _tool_list()


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "expense_ocr_extract":
        out = ocr_extract(arguments["file_path"])
    elif name == "expense_fx_rate":
        out = fx_rate(arguments["currency"], arguments["date"])
    elif name == "expense_post_ledger_entry":
        out = post_ledger_entry(arguments)
    else:
        raise ValueError(f"unknown tool: {name}")
    return [TextContent(type="text", text=str(out))]


async def _main() -> None:
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(_main())
