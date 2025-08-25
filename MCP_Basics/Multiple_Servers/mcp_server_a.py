#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

mcp = FastMCP("ServerA")

# --- Prompt: greet-user-a
@mcp.prompt("greet-user-a")
async def greet_user_a(name: str = "stranger") -> str:
    return f"[A] Hello, {name}! You're connected to Server A."

# --- Resource: resource://hello-a
@mcp.resource("resource://hello-a")
def hello_resource_a() -> Resource:
    return Resource(
        uri="resource://hello-a",
        name="hello-a",
        description="Hello from Server A (resource://hello-a)",
    )

if __name__ == "__main__":
    print("Starting MCP Server A...")
    mcp.run()
