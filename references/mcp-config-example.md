# MCP Configuration Example

Add this to your `~/.hermes/config.yaml`:

## Basic Configuration

```yaml
mcp_servers:
  # DingTalk Document Parser
  dingtalk_doc:
    command: "python"
    args: ["/Users/xdf/Documents/XDF/mcp-dingtalk-doc/server.py"]
    env:
      DINGTALK_COOKIE: "your_dingtalk_cookie_here"
      DINGTALK_DOC_OUTPUT_DIR: "/Users/xdf/Documents/dingtalk_docs"
    timeout: 60
    connect_timeout: 30
```

## With Cookie from Environment

If you prefer to set cookie via shell:

```bash
export DINGTALK_COOKIE="your_cookie_value"
```

```yaml
mcp_servers:
  dingtalk_doc:
    command: "python"
    args: ["/Users/xdf/Documents/XDF/mcp-dingtalk-doc/server.py"]
    # env not needed if set in shell
```

## Using Node.js Version (Recommended)

```yaml
mcp_servers:
  dingtalk_doc:
    command: "node"
    args: ["/Users/xdf/Documents/XDF/mcp-dingtalk-doc/nodejs/dist/index.js"]
    env:
      DINGTALK_COOKIE: "your_cookie_here"
```

## How to Get Cookie

### Method 1: Browser DevTools
1. Open DingTalk web (https://alidocs.dingtalk.com)
2. Login with QR code
3. Open DevTools (F12) → Application/Storage → Cookies
4. Copy the cookie string

### Method 2: Node.js Auto-Login
```bash
cd /Users/xdf/Documents/XDF/mcp-dingtalk-doc/nodejs
npm install
npm run cookie:login
# Browser opens, scan QR code, cookie auto-saved
```

## Testing the Configuration

After adding to config.yaml and restarting Hermes:

1. Check if tools are available:
   ```
   User: 列出钉钉MCP工具
   ```

2. Expected tools:
   - `mcp_dingtalk_doc_parse_document`
   - `mcp_dingtalk_doc_get_html`

3. Test conversion:
   ```
   User: 把这份钉钉文档转成markdown: https://alidocs.dingtalk.com/document/xxx
   ```
