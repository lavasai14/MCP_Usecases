# MCP OCR Server & Client

This project implements a **local OCR system** using MCP (Modular Control Protocol) with a **server-client architecture**. It can extract text from images using **Tesseract OCR**, or provide mock results if the OCR libraries or Tesseract binary are not installed.

---

## Features

- Perform OCR on images using Tesseract.
- Mock OCR fallback if libraries or binaries are missing.
- MCP-based architecture for modular communication.
- Save extracted text to a file optionally.
- Fully asynchronous using `asyncio`.

---

## Requirements

- Python 3.10+
- MCP package: `pip install mcp`
- Optional (for real OCR):
  ```bash
  pip install pillow pytesseract
