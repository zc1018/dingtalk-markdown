#!/usr/bin/env python3
"""
DingTalk Document → Markdown Converter

Fetches documents from DingTalk via MCP and converts to Markdown.
Usage:
    python dingtalk_to_md.py <dingtalk_url_or_id> [--output OUTPUT.md]
"""

import argparse
import subprocess
import sys
import tempfile
import os
import json
from pathlib import Path
from datetime import datetime


def call_mcp_parse_document(url_or_node_id: str, output_dir: str = None) -> dict:
    """
    Call DingTalk MCP parse_document tool.
    
    Note: This is a placeholder - actual MCP call is done via Hermes Agent.
    In practice, the agent will call mcp_dingtalk_doc_parse_document directly.
    
    Returns simulated result structure:
    {
        "node_id": str,
        "dentry_key": str,
        "output_dir": str,
        "html_file": str
    }
    """
    # This function documents the expected MCP response structure
    # Actual implementation is handled by Hermes Agent's MCP client
    return {
        "node_id": url_or_node_id,
        "output_dir": output_dir or tempfile.mkdtemp(),
        "html_file": "document.html"
    }


def convert_html_to_markdown(html_path: str, output_path: str) -> str:
    """
    Convert HTML file to Markdown using markitdown.
    
    Args:
        html_path: Path to HTML file
        output_path: Output markdown file path
    
    Returns:
        Path to converted markdown file
    """
    try:
        result = subprocess.run(
            ['markitdown', html_path, '-o', output_path],
            capture_output=True,
            text=True,
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting HTML: {e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("Error: markitdown not found. Install with: pip install markitdown", file=sys.stderr)
        sys.exit(1)


def convert_with_pandoc(html_path: str, output_path: str) -> str:
    """
    Fallback: Convert HTML to Markdown using pandoc.
    
    Args:
        html_path: Path to HTML file
        output_path: Output markdown file path
    
    Returns:
        Path to converted markdown file
    """
    try:
        result = subprocess.run(
            ['pandoc', '-f', 'html', '-t', 'markdown', html_path, '-o', output_path],
            capture_output=True,
            text=True,
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting with pandoc: {e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("Error: pandoc not found. Install with: brew install pandoc", file=sys.stderr)
        sys.exit(1)


def format_output(content: str, source: str, include_metadata: bool = True) -> str:
    """
    Format markdown content with optional metadata header.
    
    Args:
        content: Markdown content
        source: Original DingTalk source (URL or ID)
        include_metadata: Whether to add metadata header
    
    Returns:
        Formatted markdown string
    """
    if not include_metadata:
        return content
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header = f"""---
source: DingTalk Document
source_id: {source}
converted_at: {timestamp}
converter: markitdown
---

"""
    return header + content


def main():
    parser = argparse.ArgumentParser(
        description='Convert DingTalk document to Markdown'
    )
    parser.add_argument('source', help='DingTalk URL or NODE_ID')
    parser.add_argument(
        '-o', '--output',
        help='Output markdown file path (default: stdout)'
    )
    parser.add_argument(
        '--html-output',
        help='Keep intermediate HTML file at this path'
    )
    parser.add_argument(
        '--use-pandoc',
        action='store_true',
        help='Use pandoc instead of markitdown'
    )
    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Skip metadata header'
    )
    
    args = parser.parse_args()
    
    print(f"Source: {args.source}")
    print("Note: This script requires DingTalk MCP to fetch the document.")
    print("The actual document fetching is done via Hermes Agent MCP tools.")
    print("\nExpected workflow:")
    print(f"  1. mcp_dingtalk_doc_parse_document('{args.source}')")
    print(f"  2. markitdown <html_file> -o {args.output or 'output.md'}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
