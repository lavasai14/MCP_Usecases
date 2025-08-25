# agent/certificate_agent.py
import os
import sys
from pathlib import Path

# Ensure we can import from the sibling 'server' directory
CURRENT_DIR = Path(__file__).resolve().parent
SERVER_DIR = CURRENT_DIR.parent / "server"
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

from certificate_server import create_certificate  # type: ignore


def request_certificate(name: str, course: str, date: str) -> str:
    # Directly call the server tool function for local testing
    return create_certificate(name=name, course=course, date=date)

# Example usage
if __name__ == "__main__":
    name = "Alice Johnson"
    course = "Data Science"
    date = "21-Aug-2025"

    file_path = request_certificate(name, course, date)
    print(f"Certificate generated at: {file_path}")
