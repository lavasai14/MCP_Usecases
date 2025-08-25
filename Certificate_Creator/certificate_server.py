# server/certificate_server.py
from mcp.server.fastmcp import FastMCP
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

app = FastMCP("certificate-server")

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------
# Resource: Certificate Template (helper function)
# -------------------
def certificate_template() -> str:
    return os.path.join(DATA_DIR, "certificate.png")

# -------------------
# Tool: Generate Text for Certificate
# -------------------
@app.tool("generate_text")
def generate_text(name: str, course: str, date: str) -> str:
    return f" {name} {course} {date}."

# -------------------
# Tool: Create Certificate Image
# -------------------
@app.tool("create_certificate")
def create_certificate(name: str, course: str, date: str) -> str:
    # 1. Get the text
    text = generate_text(name, course, date)

    # 2. Load template
    template_path = certificate_template()
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # 3. Choose font (ensure arial.ttf exists)
    font_path = "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, 40)
    except OSError:
        # Fallback to default bitmap font if TTF not available
        font = ImageFont.load_default()

    # 4. Overlay text (example coordinates)
    draw.text((150, 300), text, font=font, fill="black")

    # 5. Save output
    file_name = f"{name.replace(' ', '_')}_certificate.png"
    output_path = os.path.join(OUTPUT_DIR, file_name)
    image.save(output_path)

    return output_path

# -------------------
# Run MCP Server
# -------------------
if __name__ == "__main__":
    print("Certificate MCP Server is starting...")
    app.run()
