#!/usr/bin/env python3
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

mcp = FastMCP("ServerB")

# --- Prompt: greet-user-b
@mcp.prompt("greet-user-b")
async def greet_user_b(name: str = "friend") -> str:
    return f"[B] Hi {name}! Time now is {datetime.utcnow().isoformat()}Z (Server B)."

# --- Resource: resource://time-b
@mcp.resource("resource://time-b")
def time_resource_b() -> Resource:
    return Resource(
        uri="resource://time-b",
        name="time-b",
        description=f"UTC time from Server B: {datetime.utcnow().isoformat()}Z",
    )

if __name__ == "__main__":
    print("Starting MCP Server B...")
    mcp.run()
