# dingtalk-markdown

> 将钉钉文档转换为 AI 最喜欢的 Markdown 格式

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 项目介绍

**dingtalk-markdown** 是一个专门用于获取钉钉文档并转换为 Markdown 格式的工具集。它能够：

- 🔗 通过 MCP（Model Context Protocol）连接钉钉文档服务
- 📄 处理钉钉特有的 `application/x-alidocs-word` 文档格式
- 🔄 将复杂嵌套结构转换为干净的 Markdown
- 🤖 让 AI 更好地理解和处理钉钉文档内容

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| **MCP 集成** | 通过 Model Context Protocol 协议与钉钉文档服务通信 |
| **格式解析** | 专门处理钉钉文档的 `x-alidocs-word` 自定义格式 |
| **Markdown 转换** | 使用 Microsoft Markitdown 进行高质量文档转换 |
| **自定义解析器** | 针对钉钉嵌套列表结构的专用解析逻辑 |
| **Hermes Skill** | 可作为 Hermes Agent 的技能插件使用 |

## 🚀 快速开始

### 方法一：一键安装（推荐）

使用 `npx` 一键安装所有依赖和 Skill：

```bash
# 一键安装 Skill 到 Hermes
npx skills add zc1018/dingtalk-markdown -g

# 或安装到特定 Agent
npx skills add zc1018/dingtalk-markdown --agent hermes
```

### 方法二：手动安装

#### 环境要求

- Python 3.8+
- Node.js 16+（用于 MCP 服务）
- `markitdown` 工具

#### 安装依赖

```bash
# 1. 安装 Python 依赖
pip install markitdown

# 2. 克隆 Skill 到 Hermes
git clone https://github.com/zc1018/dingtalk-markdown.git \
  ~/.hermes/skills/markitdown-dingding

# 3. 安装 MCP 服务（Node.js 版本）
cd /path/to/mcp-dingtalk-doc/nodejs
npm install
npm run cookie:login  # 首次登录获取 Cookie
```

### 配置 Hermes

在 `~/.hermes/config.yaml` 中添加 MCP 服务器配置：

```yaml
mcp_servers:
  dingtalk_doc:
    command: "node"
    args: ["/path/to/mcp-dingtalk-doc/nodejs/dist/index.js"]
    env:
      DINGTALK_DOC_OUTPUT_DIR: "/Users/yourname/Documents/dingtalk_docs"
    timeout: 120
    connect_timeout: 60
```

### 安装后验证

```bash
# 1. 验证 Skill 安装
ls ~/.hermes/skills/markitdown-dingding

# 2. 验证 markitdown 安装
markitdown --version

# 3. 登录钉钉获取 Cookie
cd /path/to/mcp-dingtalk-doc/nodejs
npm run cookie:login

# 4. 重启 Hermes 加载新 Skill
hermes
```

## 📚 使用方法

### 方法一：作为 Hermes Skill 使用（推荐）

**1. 安装 Skill**

```bash
# 使用 npx 一键安装
npx skills add zc1018/dingtalk-markdown -g

# 或手动克隆
git clone https://github.com/zc1018/dingtalk-markdown.git \
  ~/.hermes/skills/markitdown-dingding
```

**2. 在 Hermes 中使用**

```
# 加载 Skill
/skills markitdown-dingding

# 转换钉钉文档
转换这个钉钉文档：https://alidocs.dingtalk.com/i/nodes/xxxxx

# 或直接使用自然语言
把这份钉钉文档转成 Markdown：https://alidocs.dingtalk.com/i/nodes/xxxxx
```

**3. 支持的指令**

| 指令 | 说明 |
|------|------|
| `转换钉钉文档 [URL]` | 获取并转换单个文档 |
| `批量转换 [多个URL]` | 批量处理多个文档 |
| `提取 Node ID` | 从 URL 中提取文档 ID |
| `自定义输出路径` | 指定 Markdown 输出位置 |

### 方法二：直接使用脚本

```python
# 使用提供的辅助脚本
python scripts/dingtalk_to_md.py

# 或手动处理
from hermes_tools import mcp_tool, execute_code

# 1. 获取钉钉文档
result = mcp_tool(server="dingtalk_doc", tool="get_document", ...)

# 2. 转换为 Markdown
# 使用 markitdown 或自定义解析器
```

### 方法三：命令行转换

```bash
# 转换本地文件
markitdown "document.html" -o output.md

# 转换 PDF
markitdown "document.pdf" -o output.md
```

## 🏗️ 项目结构

```
dingtalk-markdown/
├── SKILL.md                          # Hermes Skill 定义文件
├── README.md                         # 本文件
├── scripts/
│   └── dingtalk_to_md.py            # 转换辅助脚本
└── references/
    ├── common-patterns.md           # 常见使用模式
    └── mcp-config-example.md        # MCP 配置示例
```

## ⚙️ 配置详情

### 钉钉文档格式说明

钉钉文档使用自定义的 `application/x-alidocs-word` 格式，其结构为：

```json
{
  "parts": {
    "part_id": {
      "data": {
        "body": [["h1", {...}, ["span", ...]], ...]
      }
    }
  }
}
```

这种嵌套列表格式需要专门的解析器处理。

### MCP 工具说明

| 工具名 | 功能 |
|--------|------|
| `get_document` | 获取文档原始数据 |
| `download_document` | 下载文档为 HTML |
| `search_documents` | 搜索文档 |

## 📝 使用示例

### 示例 1：获取并转换单个文档

```python
# 钉钉文档 URL
url = "https://alidocs.dingtalk.com/i/nodes/R1zknDm0WR3e100Zc2on3deQVBQEx5rG"

# 提取 Node ID
node_id = "R1zknDm0WR3e100Zc2on3deQVBQEx5rG"

# 使用 MCP 获取文档
# 然后使用 markitdown 或自定义解析器转换
```

### 示例 2：批量处理

```python
# 批量转换多个文档
urls = [
    "https://alidocs.dingtalk.com/i/nodes/xxxxx",
    "https://alidocs.dingtalk.com/i/nodes/yyyyy",
]

for url in urls:
    # 获取并转换每个文档
    convert_dingtalk_to_md(url)
```

## ⚠️ 注意事项

1. **Cookie 有效期**：钉钉 Cookie 会过期，需要定期重新登录
   ```bash
   npm run cookie:login
   ```

2. **文档权限**：确保你的钉钉账号有权限访问目标文档

3. **格式限制**：
   - 暂不支持复杂表格的完美转换
   - 部分富媒体内容可能需要手动处理
   - 文档中的评论和批注不会被转换

4. **MCP 限制**：当前 MCP 仅支持读取，不支持写入钉钉文档

## 🔧 故障排除

### 问题：无法获取文档

**解决**：
- 检查 Cookie 是否过期
- 确认文档 URL 正确
- 验证是否有文档访问权限

### 问题：转换后的 Markdown 格式错乱

**解决**：
- 钉钉文档使用了特殊格式，尝试使用自定义解析器
- 检查 `references/common-patterns.md` 中的处理模式

### 问题：MCP 服务无法启动

**解决**：
```bash
# 检查 Node.js 版本
node --version  # 需要 16+

# 重新安装依赖
cd mcp-dingtalk-doc/nodejs
rm -rf node_modules
npm install
```

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m 'Add xxx'`
4. 推送分支：`git push origin feature/xxx`
5. 创建 Pull Request

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [Microsoft Markitdown](https://github.com/microsoft/markitdown) - 文档转换引擎
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol
- DingTalk Open Platform - 钉钉开放平台

---

> 💡 **提示**：这个工具主要是为 AI Agent（如 Hermes、Claude 等）设计的，让 AI 能够更好地理解和处理钉钉文档内容。
