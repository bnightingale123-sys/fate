# yourfate.xyz 部署指南 (Vercel)

## 架构

```
Vercel 免费托管
├── index.html            ← 静态前端（排盘 + 解读 + 支付弹窗）
├── api/index.py          ← Serverless 后端（5 个路由合一）
│     ├── /config
│     ├── /api/verify-payment
│     ├── /api/create-lianlian-order
│     ├── /webhook/stripe
│     └── /webhook/lianlian
└── Vercel KV (Upstash Redis)  ← 支付记录存储
```

Stripe 使用 **Payment Link**（托管收银台），后端无需 API 密钥。

---

## 部署步骤

### 1. 导入项目

1. Vercel 面板 → **Add New… → Project**
2. 导入 GitHub 仓库 `bnightingale123-sys/fate`
3. Framework Preset 选 **Other**（自动检测即可）
4. 点 **Deploy**（首次部署会失败属正常，环境变量还没配）

### 2. 创建 KV 数据库

1. Vercel 面板 → **Storage** → **Create Database** → 选 **KV**
2. 命名如 `yourfate-kv`，区域选 **Hong Kong (hkg1)**
3. 关联到刚创建的项目（自动注入 `KV_REST_API_URL` / `KV_REST_API_TOKEN`）

### 3. 配置环境变量

项目 → **Settings → Environment Variables**，添加：

| Key | Value |
|-----|-------|
| `STRIPE_PAYMENT_LINK` | `https://buy.stripe.com/eVq5kDgDY8et2Um2h3g3600` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_NQnzVJmFdwftND4Ocwk4n54YmJWtrao9` |
| `DOMAIN` | `https://yourfate.xyz` |

（连连的 4 个密钥拿到后也在这里添加）

### 4. 重新部署

环境变量保存后 → **Deployments** → 最新一次部署 → **Redeploy**

### 5. 绑定域名

1. 项目 → **Settings → Domains** → 添加 `yourfate.xyz` 和 `www.yourfate.xyz`
2. 在你的域名 DNS 添加 Vercel 提示的 CNAME 记录
3. 等 HTTPS 证书自动签发（约 1 分钟）

### 6. 验证

- 访问 `https://yourfate.xyz` → 页面正常
- `https://yourfate.xyz/config` → 返回 JSON
- Stripe 支付链接测试支付一笔 $19.99 → webhook 确认后自动解锁

---

## 备选：传统服务器部署（Render / VPS）

如果不用 Vercel，项目里保留了完整 Flask 版本：

- `server.py` — Flask 后端（SQLite 存储）
- `start.sh` / `yourfate.nginx.conf` — 服务器启动 + NGINX 配置
- `requirements_web.txt` — 服务器依赖

```bash
pip install -r requirements_web.txt
bash start.sh
```

---

## Stripe Payment Link 设置提醒

在 Stripe Dashboard → Payment Links → 该支付链接 → **After payment** 页面：
- 重定向地址填 `https://yourfate.xyz`（用户支付后回到网站，前端会自动轮询解锁）
- Webhook 端点已创建：`https://yourfate.xyz/webhook/stripe`，事件 `checkout.session.completed`
