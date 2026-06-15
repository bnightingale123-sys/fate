# 紫微斗数 MCP Server - 部署与使用指南

让豆包、Claude、ChatGPT 等 AI 调用你的紫微斗数排盘服务。

---

## 文件说明

| 文件 | 说明 |
|---|---|
| `mcp_server.py` | **核心服务** - 紫微斗数排盘引擎 + MCP Server |
| `index.html` | 原有网页版（保持不变） |
| `claude_desktop_config.json` | Claude Desktop 配置文件 |
| `doubao_mcp_config.json` | 豆包桌面端配置文件 |
| `MCP_DEPLOY_GUIDE.md` | 本文件 |

---

## 一、让豆包调用（本地）

1. 打开豆包桌面版 → 设置 → MCP 配置
2. 添加 MCP Server：
   - **命令**：`python`
   - **参数**：`C:\Users\Administrator\Desktop\zwei-web\mcp_server.py`
3. 保存后即可使用

在豆包中直接说：
> 帮我排个紫微斗数盘：2000年1月1日中午12点，男，阳历

---

## 二、让 Claude Desktop 调用（本地）

1. 编辑 Claude Desktop 的 MCP 配置文件，添加：

```json
{
  "mcp_servers": {
    "ziwei-doushu": {
      "command": "python",
      "args": ["C:\\Users\\Administrator\\Desktop\\zwei-web\\mcp_server.py"]
    }
  }
}
```

2. 重启 Claude Desktop 即可使用

---

## 三、部署到 skymans.cn（远程）

更方便的是部署到服务器上，所有 AI 都能远程调用。

```bash
# 服务器上
pip install mcp uvicorn

# 启动 HTTP 服务（端口 8000）
python mcp_server.py --http 0.0.0.0:8000
```

推荐用 Nginx 反代 + HTTPS：

```nginx
server {
    listen 443 ssl;
    server_name skymans.cn;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /mcp {
        proxy_pass http://127.0.0.1:8000/mcp;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

远程端点：`https://skymans.cn/mcp`

---

## 四、AI 中使用的示例 Prompt

**豆包/Claude/ChatGPT 通用：**

> 请帮我做紫微斗数命理分析：
> - 出生：2000年1月1日 中午12点
> - 性别：男
> - 历法：阳历

AI 会自动调用 `full_ziwei_analysis` 工具完成排盘和解读。

---

## 五、可用工具

| 工具 | 功能 |
|---|---|
| `calculate_ziwei_chart` | 紫微斗数排盘（返回原始命盘数据） |
| `get_ziwei_report` | 命理解读（基于排盘结果生成详细报告） |
| `full_ziwei_analysis` | **一键完整分析**（排盘+解读一步到位） |
