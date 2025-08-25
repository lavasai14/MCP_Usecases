# MCP Travel System

This project demonstrates a **Modular Control Protocol (MCP)** based travel system with two setups: **without agents** (hardcoded tool calls) and **with agents** (dynamic orchestration).

---

## Features

- **Travel Server Tools**:
  - `get_weather`: Returns weather info for a city (mock data).
  - `get_flight_details`: Returns flight info between two cities (mock data).
  - `generate_itinerary_pdf`: Generates a PDF itinerary with city, days, and activities.
- **Client**:
  - Connects to the server via MCP over `stdio`.
  - Calls tools sequentially (non-agent) or lets agents decide tool execution.
- **PDF Generation**: Uses ReportLab to create a simple travel itinerary.

---

## Requirements

- Python 3.10+
- Dependencies:

```bash
pip install mcp reportlab pillow pytesseract

