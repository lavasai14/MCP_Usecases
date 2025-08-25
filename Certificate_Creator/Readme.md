# Certificate Generator MCP System

This project provides a **certificate generation system** using MCP (Modular Control Protocol).  
It can generate personalized certificate images dynamically with names, courses, and dates.

---

## Features

- **MCP Server (`certificate_server.py`)**
  - Provides tools for generating certificate text and images.
  - Uses a certificate template (`certificate.png`) from the `data` folder.
  - Generates PNG certificates in the `output` folder.
- **Agent (`certificate_agent.py`)**
  - Client script to request a certificate from the server.
  - Can be used for local testing or integrated into larger automation pipelines.

---
certificate_project/
├─ agent/
│  └─ certificate_agent.py         # Client/agent script
├─ server/
│  └─ certificate_server.py        # MCP server with tools
├─ data/
│  └─ certificate.png              # Certificate template image
├─ output/                         # Generated certificates
├─ requirements.txt                # Python dependencies
└─ README.md                       # Project documentation


## Setup

1. **Clone the repository**
```bash
git clone <repo_url>
cd <repo_folder>

