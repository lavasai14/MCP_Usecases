# mcp_server.py
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("PromptServer")

# Define a prompt
@mcp.prompt("greet-user")
async def greet_user_prompt(name: str = "stranger") -> str:
    """
    A simple prompt that greets the user.
    """
    return f"Hello, {name}! Welcome to the MCP world."

if __name__ == "__main__":
    print("Starting MCP Prompt Server...")
    mcp.run()
