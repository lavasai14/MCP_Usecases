# mcp_client.py
import sys
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters

async def main():
    # Spawn the server process
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            await session.initialize()
            
            # List available resources
            listed = await session.list_resources()
            print("Available Resources:")
            for r in listed.resources:
                print(f" - {r.name} ({r.uri})")

            # Read the hello resource
            res = await session.read_resource("resource://hello")
            print("\nResource Content:")
            for c in res.contents:
                print(c.text)

if __name__ == "__main__":
    asyncio.run(main())
