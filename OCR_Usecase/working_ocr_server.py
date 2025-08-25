#!/usr/bin/env python3
"""
Working MCP OCR Server
"""

import asyncio
import sys
import os
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Optional: Try to import OCR libraries
try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("Warning: OCR libraries not installed. Install with: pip install pillow pytesseract", file=sys.stderr)

# If OCR libs are present, try to locate the Tesseract binary explicitly (Windows-friendly)
if 'pytesseract' in globals():
    try:
        # Allow override via environment variable
        env_cmd = os.getenv("TESSERACT_CMD")
        candidate_paths = [
            env_cmd if env_cmd else None,
            os.path.join(os.getenv("LOCALAPPDATA", ""), "Programs", "Tesseract-OCR", "tesseract.exe"),
            r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        ]
        candidate_paths = [p for p in candidate_paths if p]
        for p in candidate_paths:
            if Path(p).exists():
                pytesseract.pytesseract.tesseract_cmd = p
                break
    except Exception:
        # Non-fatal; will be handled during OCR call
        pass

# Create server instance
app = Server("ocr-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="perform_ocr",
            description="Perform OCR on an image file using Tesseract",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image file to process"
                    }
                },
                "required": ["image_path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    if name == "perform_ocr":
        image_path = arguments.get("image_path", "")
        
        try:
            # Check if file exists
            if not Path(image_path).exists():
                return [TextContent(
                    type="text",
                    text=f"Error: Image file '{image_path}' not found."
                )]
            
            if HAS_OCR:
                # Perform actual OCR
                image = Image.open(image_path)
                extracted_text = pytesseract.image_to_string(image)
                
                if extracted_text.strip():
                    result = f"OCR Results from '{image_path}':\n\n{extracted_text}"
                else:
                    result = f"No text found in image '{image_path}'"
            else:
                # Fallback mock result
                result = f"Mock OCR result for '{image_path}' (OCR libraries not installed)\n\nSample extracted text:\nInvoice #12345\nDate: 2024-01-15\nTotal: $123.45"
            
            return [TextContent(
                type="text",
                text=result
            )]
        except getattr(sys.modules.get('pytesseract', None), 'TesseractNotFoundError', Exception) as e:
            # If Tesseract binary is missing, provide a mock response for graceful degradation
            if 'TesseractNotFoundError' in e.__class__.__name__:
                result = (
                    f"Mock OCR result for '{image_path}' (Tesseract binary not found)\n\n"
                    "Sample extracted text:\nInvoice #12345\nDate: 2024-01-15\nTotal: $123.45"
                )
                return [TextContent(type="text", text=result)]
            # For other exceptions, surface the error
            return [TextContent(
                type="text",
                text=f"Error processing image '{image_path}': {str(e)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error processing image '{image_path}': {str(e)}"
            )]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the server using stdio"""
    try:
        # Use stdio for MCP communication
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())