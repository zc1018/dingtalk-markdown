---
name: markitdown-dingding
description: Fetch documents from DingTalk via MCP, convert to HTML, then convert to Markdown. Use when users need to extract content from DingTalk documents (钉钉文档) and convert to Markdown format for further processing.
---

# DingTalk Document → Markdown Converter

Fetch documents from DingTalk and convert to Markdown in one workflow.

## Overview

This skill combines the DingTalk Document MCP Server with Markdown conversion:
1. **Fetch** document from DingTalk using MCP (`parse_document` or `get_html`)
2. **Generate** HTML from DingTalk's proprietary format
3. **Convert** HTML to clean Markdown using markitdown or pandoc

## Prerequisites

### 1. DingTalk MCP Server Setup

The MCP server is located at `/Users/xdf/Documents/XDF/mcp-dingtalk-doc/`

**Node.js version (recommended)** - Supports automatic cookie management:

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  dingtalk_doc:
    command: "node"
    args: ["/Users/xdf/Documents/XDF/mcp-dingtalk-doc/nodejs/dist/index.js"]
    env:
      DINGTALK_DOC_OUTPUT_DIR: "/Users/xdf/Documents/dingtalk_docs"
    timeout: 120
    connect_timeout: 60
```

**Get Cookie:**
- Node.js version reads from `dingtalk_cookies.json` automatically
- Run `npm run cookie:login` in the nodejs directory for automatic browser login
- Or manually copy cookie from browser DevTools

### 2. Markitdown Installation

```bash
pip install markitdown
```

## MCP Tools Available

After configuration, these tools will be available:

| Tool | Description | Use Case |
|------|-------------|----------|
| `mcp_dingtalk_doc_parse_document` | Parse DingTalk doc, save HTML + files | Full document extraction with images |
| `mcp_dingtalk_doc_get_html` | Get HTML content only (no files) | Quick content extraction |

## Workflow

### Basic Flow

```
DingTalk URL/ID → MCP parse_document → HTML → markitdown → Markdown
```

### Step-by-Step

1. **Get DingTalk document URL or NODE_ID from user**
   - Full URL: `https://alidocs.dingtalk.com/i/nodes/xxxxx`
   - Or just NODE_ID: `R1zknDm0WR3e100Zc2on3deQVBQEx5rG`

2. **Call MCP tool to fetch document**:
   ```python
   # Option A: parse_document (saves files)
   result = mcp_dingtalk_doc_parse_document(
       url_or_node_id="https://alidocs.dingtalk.com/i/nodes/...",
       save_files=True,
       output_dir="/Users/xdf/Documents/dingtalk_docs"
   )
   
   # Option B: get_html (content only)
   result = mcp_dingtalk_doc_get_html(
       url_or_node_id="doc_node_id"
   )
   ```

3. **Convert HTML to Markdown**:
   ```bash
   # If parse_document saved HTML file
   markitdown "/path/to/output/document.html" -o output.md
   
   # Or if you have HTML content directly
   echo "$html_content" > /tmp/doc.html
   markitdown /tmp/doc.html -o output.md
   ```

## Usage Examples

### Example 1: Full Document Extraction

```python
# 1. Parse DingTalk document
result = mcp_dingtalk_doc_parse_document(
    url_or_node_id="https://alidocs.dingtalk.com/i/nodes/abc123",
    save_files=True
)

# 2. Convert HTML to Markdown
html_path = result['output_dir'] + '/document.html'
terminal(f"markitdown '{html_path}' -o /tmp/output.md")

# 3. Read markdown content
content = read_file("/tmp/output.md")
```

### Example 2: Quick Content Extraction

```python
# 1. Get HTML content directly
result = mcp_dingtalk_doc_get_html(
    url_or_node_id="document_node_id"
)

# 2. Save HTML to temp file
html_content = result['html']
write_file("/tmp/ding_doc.html", html_content)

# 3. Convert to Markdown
terminal("markitdown /tmp/ding_doc.html -o /tmp/ding_doc.md")

# 4. Return markdown
content = read_file("/tmp/ding_doc.md")
```

## Error Handling

### Common Issues

| Issue | Solution |
|-------|----------|
| `Cookie expired` | Run `npm run cookie:login` in nodejs directory or manually update cookie |
| `Document not found` | Verify URL/ID is correct and accessible |
| `Permission denied` | Ensure document is shared with your account |
| `markitdown not found` | Run `pip install markitdown` |

### MCP Connection Issues

If MCP tools not appearing:
1. Check server is running: `node /Users/xdf/Documents/XDF/mcp-dingtalk-doc/nodejs/dist/index.js`
2. Verify config syntax in `~/.hermes/config.yaml`
3. Restart Hermes Agent after config changes

## Best Practices

1. **Use `parse_document`** when you need:
   - Complete document with images
   - Preserved formatting
   - Local file archive

2. **Use `get_html`** when you need:
   - Quick content extraction
   - No file saving
   - In-memory processing

3. **Always check output**:
   - Review markdown for formatting issues
   - Verify images are properly referenced
   - Check for DingTalk-specific formatting

## References

- [DingTalk MCP Server](/Users/xdf/Documents/XDF/mcp-dingtalk-doc/README.md)
- [Markitdown GitHub](https://github.com/microsoft/markitdown)
