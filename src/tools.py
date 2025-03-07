"""This module defines the tools used by the agent.

Feel free to modify or add new tools to suit your specific needs.

To learn how to create a new tool, see:
- https://python.langchain.com/docs/concepts/tools/
- https://python.langchain.com/docs/how_to/#tools
"""

from __future__ import annotations

import requests
from io import BytesIO
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

def scrape_webpage(url):
    """Extract text from a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return " ".join(paragraphs)[:5000]  # Limit to 5000 characters
    except requests.RequestException as e:
        return f"Error fetching content: {e}"

def extract_pdf_from_url(url):
    """Download and extract text from a PDF URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        pdf_text = []
        with BytesIO(response.content) as pdf_file:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                pdf_text.append(page.extract_text())

        return "\n".join(pdf_text)[:5000]  # Limit to 5000 characters
    except requests.RequestException as e:
        return f"Error fetching PDF: {e}"
    except Exception as e:
        return f"Error processing PDF: {e}"
