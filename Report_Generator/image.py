#!/usr/bin/env python3
"""
Single-file demo: MCP server provides an image + text resource,
client fetches them and generates a PDF report.
"""

import sys
import asyncio
import base64
import json
import os
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --------------------------
# MCP SERVER PART
# --------------------------
mcp = FastMCP("ReportServer")

def load_image_as_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Image resource
@mcp.resource("resource://logo")
def logo_resource() -> Resource:
    return Resource(
        uri="resource://logo",
        name="Company Logo",
        description="Logo image in PNG format",
        mimeType="image/png",
        contents=[{
            "type": "blob",
            "mimeType": "image/png",
            "data": load_image_as_base64("logo.png"),  # <- make sure logo.png exists
        }],
    )

# Text resource
@mcp.resource("resource://summary")
def summary_resource() -> Resource:
    return Resource(
        uri="resource://summary",
        name="Quarterly Summary",
        description="Business summary text",
        mimeType="text/plain",
        contents=[{
            "type": "text",
            "text": "This quarter, revenue grew by 25%. Customer satisfaction improved to 92%.",
        }],
    )

# --------------------------
# MCP CLIENT PART
# --------------------------
async def run_client():
    params = StdioServerParameters(command=sys.executable, args=[__file__])
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # ---- Fetch logo ----
            logo_res = await session.read_resource("resource://logo")
            logo_data = None
            # Normalize contents regardless of SDK return type
            contents = []
            if hasattr(logo_res, "model_dump"):
                try:
                    contents = logo_res.model_dump().get("contents", [])
                except Exception:
                    contents = []
            if not contents:
                contents = getattr(logo_res, "contents", [])
            if not contents and isinstance(logo_res, dict):
                contents = logo_res.get("contents", [])

            # First pass: look for direct blob
            for c in contents:
                ctype = getattr(c, "type", None) if hasattr(c, "type") else (c.get("type") if isinstance(c, dict) else None)
                if ctype == "blob":
                    logo_data = getattr(c, "data", None) if hasattr(c, "data") else (c.get("data") if isinstance(c, dict) else None)
                    if logo_data:
                        break

            # Second pass: sometimes a text/plain content has JSON with nested contents
            if not logo_data:
                for c in contents:
                    text_val = getattr(c, "text", None) if hasattr(c, "text") else (c.get("text") if isinstance(c, dict) else None)
                    if text_val:
                        try:
                            payload = json.loads(text_val)
                            inner_contents = payload.get("contents", [])
                            for ic in inner_contents:
                                if (isinstance(ic, dict) and ic.get("type") == "blob") or (hasattr(ic, "type") and getattr(ic, "type") == "blob"):
                                    logo_data = ic.get("data") if isinstance(ic, dict) else getattr(ic, "data", None)
                                    if logo_data:
                                        break
                            if logo_data:
                                break
                        except Exception:
                            continue

            logo_path = None
            if logo_data:
                logo_bytes = base64.b64decode(logo_data)
                logo_path = os.path.abspath("logo_tmp.png")
                with open(logo_path, "wb") as f:
                    f.write(logo_bytes)

            # ---- Fetch summary ----
            summary_res = await session.read_resource("resource://summary")
            summary_text = ""
            for c in getattr(summary_res, "contents", []):
                if getattr(c, "type", None) == "text":
                    summary_text = getattr(c, "text", "")

            # ---- Generate PDF ----
            doc = SimpleDocTemplate("report.pdf", pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            if logo_path and os.path.exists(logo_path):
                story.append(Image(logo_path, width=120, height=60))
                story.append(Spacer(1, 20))

            story.append(Paragraph("Quarterly Report", styles["Title"]))
            story.append(Spacer(1, 12))
            story.append(Paragraph(summary_text, styles["Normal"]))
            story.append(Spacer(1, 12))
            story.append(Paragraph("Report generated using MCP resources.", styles["Italic"]))

            doc.build(story)
            print("PDF report generated as report.pdf")


# --------------------------
# ENTRYPOINT
# --------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--client":
        asyncio.run(run_client())
    else:
        print("Starting MCP server... (resources: logo, summary)")
        mcp.run()
