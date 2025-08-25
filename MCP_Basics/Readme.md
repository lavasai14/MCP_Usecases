# MCP Multi-Server Demo

This project demonstrates a **multi-server MCP setup** where a single client interacts with **two MCP servers** exposing both prompts and resources.  
It showcases **asynchronous communication**, prompt execution, resource retrieval, and multi-server orchestration.



## Server Details

### **Server A (`mcp_server_a.py`)**
- **Prompt**: `greet-user-a(name)` → Greets user with server A message.  
- **Resource**: `resource://hello-a` → Returns a simple "Hello from Server A".  

### **Server B (`mcp_server_b.py`)**
- **Prompt**: `greet-user-b(name)` → Greets user with current UTC time (Server B).  
- **Resource**: `resource://time-b` → Returns current UTC time as resource.

---

## Client Details

### **Multi-Server Client (`multi_mcp_client.py`)**
- Connects to **both Server A and Server B** concurrently using `AsyncExitStack`.  
- Lists prompts and resources from both servers.  
- Calls prompts with user parameters and prints results.  
- Reads resources from each server and prints content.  
- Demonstrates memory-free, multi-server interaction.

### **Single-Server Clients**
- **`mcp_prompt_client.py`** → Example of calling a single server prompt.  
- **`mcp_client.py`** → Example of reading a single server resource.

---

## Setup

1. Install dependencies:
```bash
pip install mcp asyncio python-dotenv


             +-----------------------------+
             |       multi_mcp_client      |
             |  - Connects to both servers|
             |  - Calls prompts & reads   |
             |    resources               |
             +-------------+---------------+
                           |
              +------------+------------+
              |                         |
              v                         v
    +----------------+         +----------------+
    |   Server A     |         |   Server B     |
    |----------------|         |----------------|
    | Prompts:       |         | Prompts:       |
    | - greet-user-a |         | - greet-user-b |
    | Resources:     |         | Resources:     |
    | - hello-a      |         | - time-b       |
    +----------------+         +----------------+
           ^                            ^
           | Async prompt/resource call |
           +----------------------------+


