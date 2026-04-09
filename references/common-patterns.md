# Common Usage Patterns

## Pattern 1: Single DingTalk Document to Markdown

**Scenario**: User has a DingTalk document URL to convert

```python
# User: 把这份钉钉文档转成markdown
# Document: https://alidocs.dingtalk.com/document/abc123

# Step 1: Fetch from DingTalk via MCP
result = mcp_dingtalk_doc_parse_document(
    url_or_node_id="https://alidocs.dingtalk.com/document/abc123",
    save_files=True,
    output_dir="/tmp/ding_doc_abc123"
)

# Step 2: Convert HTML to Markdown
html_file = result['output_dir'] + '/document.html'
terminal(f"markitdown '{html_file}' -o /tmp/output.md")

# Step 3: Read and return
content = read_file("/tmp/output.md")
```

## Pattern 2: Quick Content Extraction (No File Saving)

**Scenario**: Just need the text content, no images/files

```python
# Step 1: Get HTML content only
result = mcp_dingtalk_doc_get_html(
    url_or_node_id="doc_node_id"
)

# Step 2: Save HTML to temp
write_file("/tmp/doc.html", result['html'])

# Step 3: Convert
terminal("markitdown /tmp/doc.html -o /tmp/doc.md")

# Step 4: Return content
content = read_file("/tmp/doc.md")
```

## Pattern 3: Batch Processing Multiple DingTalk Docs

**Scenario**: Process multiple documents from a folder/list

```python
doc_urls = [
    "https://alidocs.dingtalk.com/document/doc1",
    "https://alidocs.dingtalk.com/document/doc2",
    "doc3_node_id"  # Can use NODE_ID directly
]

results = []
for i, url in enumerate(doc_urls, 1):
    # Fetch
    result = mcp_dingtalk_doc_parse_document(
        url_or_node_id=url,
        save_files=True,
        output_dir=f"/tmp/ding_docs/doc_{i}"
    )
    
    # Convert
    html_path = result['output_dir'] + '/document.html'
    md_path = f"/tmp/ding_docs/doc_{i}.md"
    terminal(f"markitdown '{html_path}' -o '{md_path}'")
    
    results.append(md_path)

# All markdown files are ready
```

## Pattern 4: DingTalk Doc with Image Extraction

**Scenario**: Document contains images that need to be preserved

```python
# Step 1: Parse with save_files=True (includes images)
result = mcp_dingtalk_doc_parse_document(
    url_or_node_id="doc_url",
    save_files=True,
    output_dir="/tmp/doc_with_images"
)

# Images are saved in output_dir/images/
# HTML references them with relative paths

# Step 2: Convert
html_path = result['output_dir'] + '/document.html'
terminal(f"markitdown '{html_path}' -o /tmp/output.md")

# Note: markitdown will handle image references
# Images remain in original location
```

## Pattern 5: Using NODE_ID Instead of Full URL

**Scenario**: User only provides the document ID

```python
# DingTalk URLs look like:
# https://alidocs.dingtalk.com/document/abc123def456
#                              ^^^^^^^ NODE_ID

# You can use either:
node_id = "abc123def456"

# Option A: Full URL
mcp_dingtalk_doc_parse_document(
    url_or_node_id=f"https://alidocs.dingtalk.com/document/{node_id}"
)

# Option B: Just NODE_ID (MCP server handles it)
mcp_dingtalk_doc_parse_document(
    url_or_node_id=node_id
)
```

## Pattern 6: Fallback to Pandoc

**Scenario**: markitdown not available or fails

```python
html_path = "/tmp/document.html"
md_path = "/tmp/document.md"

# Try markitdown first
try:
    terminal(f"markitdown '{html_path}' -o '{md_path}'")
except:
    # Fallback to pandoc
    terminal(f"pandoc -f html -t markdown '{html_path}' -o '{md_path}'")

content = read_file(md_path)
```

## Pattern 7: Convert and Upload to Another System

**Scenario**: Get DingTalk doc, convert, send to Notion/Slack/etc

```python
# 1. Fetch from DingTalk
result = mcp_dingtalk_doc_parse_document(url_or_node_id="doc_url")

# 2. Convert to Markdown
html_path = result['output_dir'] + '/document.html'
terminal(f"markitdown '{html_path}' -o /tmp/doc.md")

# 3. Read content
content = read_file("/tmp/doc.md")

# 4. Send to another platform
# e.g., Notion, Slack, Discord, etc.
```
