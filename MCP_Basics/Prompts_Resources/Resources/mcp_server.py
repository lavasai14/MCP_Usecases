# mcp_server.py
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

mcp = FastMCP("SimpleResourceServer")

# Register a single resource
@mcp.resource("resource://hello")
def hello_resource() -> Resource:
    return Resource(
        uri="resource://hello",
        name="Hello Resource",
        description="A simple resource that just says hello!"
    )

if __name__ == "__main__":
    print("Starting Simple MCP server...")
    mcp.run()   # starts stdio server
