# MCP PDF Report Demo

A single-file demo showing how to use **MCP (Modular Control Protocol)** to generate a PDF report from server-provided resources (image + text).

---

## Features

- **MCP Server**
  - Provides an image resource (`logo.png`) via MCP.
  - Provides a text resource (quarterly summary).
- **MCP Client**
  - Fetches the server resources.
  - Generates a PDF report (`report.pdf`) combining the image and text.
- **Self-contained**
  - Both server and client are in a single Python file (`report_demo.py`).

---

mcp_report_project/
├─ logo.png                     # Company logo image (resource)
├─ report_demo.py               # Single-file MCP server + client
├─ output/                      # PDF reports generated here
├─ requirements.txt             # Python dependencies
└─ README.md                    # Documentation

---
## Setup

1. **Clone the repository**
```bash
git clone <repo_url>
cd mcp_report_project

