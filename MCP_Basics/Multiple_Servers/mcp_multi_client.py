#!/usr/bin/env python3
import sys
import asyncio
from contextlib import AsyncExitStack
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    # Define both servers
    paramsA = StdioServerParameters(command=sys.executable, args=["mcp_server_a.py"])
    paramsB = StdioServerParameters(command=sys.executable, args=["mcp_server_b.py"])

    async with AsyncExitStack() as stack:
        # Connect to Server A
        readA, writeA = await stack.enter_async_context(stdio_client(paramsA))
        sessA = ClientSession(readA, writeA)
        await stack.enter_async_context(sessA)
        await sessA.initialize()

        # Connect to Server B
        readB, writeB = await stack.enter_async_context(stdio_client(paramsB))
        sessB = ClientSession(readB, writeB)
        await stack.enter_async_context(sessB)
        await sessB.initialize()

        print("=== Connected to two MCP servers ===")

        # ---- List prompts on both
        print("\n[Server A] Prompts:")
        promptsA = await sessA.list_prompts()
        for p in promptsA.prompts:
            desc = getattr(p, "description", "") or ""
            print(f" - {p.name}" + (f" — {desc}" if desc else ""))

        print("\n[Server B] Prompts:")
        promptsB = await sessB.list_prompts()
        for p in promptsB.prompts:
            desc = getattr(p, "description", "") or ""
            print(f" - {p.name}" + (f" — {desc}" if desc else ""))

        # ---- Call one prompt on each
        print("\n[Server A] Calling prompt: greet-user-a")
        respA = await sessA.get_prompt("greet-user-a", {"name": "Lavanthi"})
        try:
            print("  ->", respA.messages[0].content.text)
        except Exception:
            # Fallbacks for different client structures
            partsA = getattr(respA, "completion", None) or getattr(respA, "contents", [])
            for part in partsA:
                text = getattr(part, "text", None) or str(part)
                print("  ->", text)

        print("\n[Server B] Calling prompt: greet-user-b")
        respB = await sessB.get_prompt("greet-user-b", {"name": "Lavanthi"})
        try:
            print("  ->", respB.messages[0].content.text)
        except Exception:
            partsB = getattr(respB, "completion", None) or getattr(respB, "contents", [])
            for part in partsB:
                text = getattr(part, "text", None) or str(part)
                print("  ->", text)

        # ---- List resources and read one from each
        print("\n[Server A] Resources:")
        resA_list = await sessA.list_resources()
        for r in resA_list.resources:
            print(f" - {r.name} ({r.uri})")
        print("Reading resource://hello-a")
        resA = await sessA.read_resource("resource://hello-a")
        for c in getattr(resA, "contents", []):
            print("  ->", getattr(c, "text", None) or str(c))

        print("\n[Server B] Resources:")
        resB_list = await sessB.list_resources()
        for r in resB_list.resources:
            print(f" - {r.name} ({r.uri})")
        print("Reading resource://time-b")
        resB = await sessB.read_resource("resource://time-b")
        for c in getattr(resB, "contents", []):
            print("  ->", getattr(c, "text", None) or str(c))

if __name__ == "__main__":
    asyncio.run(main())
