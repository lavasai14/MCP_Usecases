# mcp_prompt_client.py
import sys
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    # Spawn the server process
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],  # Server with prompts
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize session
            await session.initialize()

            # List available prompts
            listed = await session.list_prompts()
            print("Available Prompts:")
            for p in listed.prompts:
                print(f" - {p.name} ({p.description})")

            # Use the greet-user prompt
            res = await session.get_prompt("greet-user", {"name": "Lavanthi"})
            print("\nPrompt Response:")
            print(res.messages[0].content.text)

if __name__ == "__main__":
    asyncio.run(main())
