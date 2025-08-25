#!/usr/bin/env python3


import asyncio
import sys
import argparse
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def perform_ocr(image_path: str) -> str:
    """
    Perform OCR on an image using the MCP OCR server
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text from the image
    """
    server_params = StdioServerParameters(
        command="python",
        args=["working_ocr_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(
                "perform_ocr",
                {"image_path": image_path}
            )
            
            return result.content[0].text

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Run OCR on an image using the local MCP server",
        usage="python ocr_client.py <image_path> [--out OUTPUT_PATH]",
    )
    parser.add_argument("image_path", help="Path to the image file to OCR")
    parser.add_argument(
        "--out",
        dest="out",
        help="Optional path to save the extracted text. If a directory is provided, a file will be created inside it.",
    )
    args = parser.parse_args()

    image_path = args.image_path

    # Check if image file exists
    if not Path(image_path).exists():
        print(f"Error: Image file '{image_path}' not found!")
        sys.exit(1)

    try:
        print(f" Processing image: {image_path}")
        text = await perform_ocr(image_path)

        print("\n OCR Results:")
        print("=" * 50)
        print(text)
        print("=" * 50)

        # Save to file if requested
        if args.out:
            out_path = Path(args.out)
            if out_path.is_dir() or str(args.out).endswith(("/", "\\")):
                # Save into provided directory using image stem
                out_path = out_path / (Path(image_path).stem + "_ocr.txt")
            # Ensure parent directory exists
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")
            print(f" Saved OCR text to: {out_path}")

    except Exception as e:
        print(f" Error processing image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())