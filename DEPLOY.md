# yourfate.xyz 部署指南

## 1. 上传代码到服务器

```bash
# 在服务器上
mkdir -p /var/www/yourfate.xyz
cd /var/www/yourfate.xyz

# 从本地上传（在本机执行）
scp index.html server.py requirements_web.txt start.sh .env.example \
    user@your-server-ip:/var/www/yourfate.xyz/
```

## 2. 配置环境变量

```bash
cd /var/www/yourfate.xyz
cp .env.example .env
nano .env   # 填入真实密钥
```

需要填入的内容：
- **Stripe**: `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`
- **连连跨境**: `LIANLIAN_MERCHANT_ID`, `LIANLIAN_AUTH_TOKEN`, `LIANLIAN_RSA_PRIVATE_KEY`, `LIANLIAN_RSA_PUBLIC_KEY`
- **域名**: `DOMAIN=https://yourfate.xyz`

## 3. 安装依赖 & 启动

```bash
# Python 版本 >= 3.10
python3 --version

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements_web.txt

# 启动（开发测试）
bash start.sh

# 或生产模式（gunicorn）
gunicorn --bind 127.0.0.1:5000 --workers 2 --timeout 120 server:app
```

## 4. 配置 HTTPS & NGINX

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请证书（确保域名 DNS 已指向服务器 IP）
sudo certbot --nginx -d yourfate.xyz -d www.yourfate.xyz

# 使用项目中的 NGINX 配置
sudo cp yourfate.nginx.conf /etc/nginx/sites-available/yourfate.xyz
sudo ln -sf /etc/nginx/sites-available/yourfate.xyz /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## 5. 设置开机自启 (systemd)

```bash
sudo tee /etc/systemd/system/yourfate.service << 'EOF'
[Unit]
Description=yourfate.xyz - Zi Wei Dou Shu Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/yourfate.xyz
EnvironmentFile=/var/www/yourfate.xyz/.env
ExecStart=/var/www/yourfate.xyz/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 --timeout 120 server:app
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now yourfate
```

## 6. 验证

```bash
# 检查服务状态
sudo systemctl status yourfate
curl http://127.0.0.1:5000/config | python3 -m json.tool

# 访问网站
curl -I https://yourfate.xyz
```

## 7. Stripe & 连连 Webhook 配置

| 平台 | Webhook URL |
|------|------------|
| Stripe | `https://yourfate.xyz/webhook/stripe` |
| 连连跨境 | `https://yourfate.xyz/webhook/lianlian` |

在对应的商户后台填入以上地址。
