"""
yourfate.xyz — Vercel Serverless Backend (Flask WSGI)
======================================================
Single function handling all API + webhook routes via vercel.json rewrites:

  GET  /config                    → payment config for frontend
  GET  /api/verify-payment        → check if a reading is paid
  POST /api/create-lianlian-order → create LianLian Global payment order
  POST /webhook/stripe            → Stripe Payment Link confirmation
  POST /webhook/lianlian          → LianLian Global payment notification

Storage: Vercel KV (Upstash Redis) — keys: pay:<reading_id>
Env vars (set in Vercel dashboard):
  STRIPE_PAYMENT_LINK    Stripe hosted payment link
  STRIPE_WEBHOOK_SECRET  whsec_... (webhook signature verification)
  DOMAIN                 https://yourfate.xyz
  KV_REST_API_URL / KV_REST_API_TOKEN              auto-injected by Vercel KV
  UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN  auto-injected by Upstash Redis
                                                   (either pair works — same backend)
  LIANLIAN_MERCHANT_ID / LIANLIAN_AUTH_TOKEN / LIANLIAN_RSA_PRIVATE_KEY /
  LIANLIAN_RSA_PUBLIC_KEY / LIANLIAN_API_BASE  (LianLian Global, optional)
"""

import base64
import json
import os
import time
import uuid
import requests

from flask import Flask, request, jsonify

import stripe

# ── Configuration ──────────────────────────────────────────────

STRIPE_PAYMENT_LINK = os.environ.get(
    "STRIPE_PAYMENT_LINK", "https://buy.stripe.com/eVq5kDgDY8et2Um2h3g3600"
)
STRIPE_WEBHOOK_SECRET = os.environ.get(
    "STRIPE_WEBHOOK_SECRET", "whsec_placeholder_replace_me"
)
DOMAIN = os.environ.get("DOMAIN", "https://yourfate.xyz")

LIANLIAN_MERCHANT_ID = os.environ.get("LIANLIAN_MERCHANT_ID", "placeholder_merchant_id")
LIANLIAN_AUTH_TOKEN = os.environ.get("LIANLIAN_AUTH_TOKEN", "placeholder_auth_token")
LIANLIAN_RSA_PRIVATE_KEY = os.environ.get("LIANLIAN_RSA_PRIVATE_KEY", "")
LIANLIAN_RSA_PUBLIC_KEY = os.environ.get("LIANLIAN_RSA_PUBLIC_KEY", "")
LIANLIAN_API_BASE = os.environ.get("LIANLIAN_API_BASE", "https://api.lianlianglobal.com")

PAY_TTL_SECONDS = 90 * 24 * 3600  # 90 days retention for payment records

app = Flask(__name__)


# ── Storage: Vercel KV (Upstash Redis) ─────────────────────────

# Supports both naming conventions:
#  - Vercel KV storage: KV_REST_API_URL / KV_REST_API_TOKEN
#  - Upstash Redis marketplace integration: UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN
KV_REST_API_URL = os.environ.get("KV_REST_API_URL") or os.environ.get("UPSTASH_REDIS_REST_URL", "")
KV_REST_API_TOKEN = os.environ.get("KV_REST_API_TOKEN") or os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")

_redis = None


def kv():
    """Lazy-init the Upstash Redis client. Returns None if KV not configured."""
    global _redis
    if _redis is None:
        try:
            if KV_REST_API_URL and KV_REST_API_TOKEN:
                from upstash_redis import Redis
                _redis = Redis(url=KV_REST_API_URL, token=KV_REST_API_TOKEN)
            else:
                app.logger.warning("Vercel KV not configured — payment records unavailable")
                _redis = False
        except Exception as e:
            app.logger.error(f"KV init error: {e}")
            _redis = False
    return _redis if _redis is not False else None


def _pay_key(reading_id):
    return f"pay:{reading_id}"


def kv_get_payment(reading_id):
    r = kv()
    if not r:
        return None
    try:
        raw = r.get(_pay_key(reading_id))
        if not raw:
            return None
        return json.loads(raw) if isinstance(raw, str) else raw
    except Exception as e:
        app.logger.error(f"KV get error: {e}")
        return None


def kv_set_payment(reading_id, data):
    r = kv()
    if not r:
        return False
    try:
        r.set(_pay_key(reading_id), json.dumps(data, ensure_ascii=False), ex=PAY_TTL_SECONDS)
        return True
    except Exception as e:
        app.logger.error(f"KV set error: {e}")
        return False


def mark_paid(reading_id, gateway="stripe"):
    """Mark a reading as paid (creates the record if missing)."""
    now = int(time.time())
    record = kv_get_payment(reading_id) or {}
    record.update({
        "status": "paid",
        "gateway": gateway,
        "paid_at": now,
        "created_at": record.get("created_at", now),
    })
    kv_set_payment(reading_id, record)


# ── LianLian Global: RSA Signing Helpers ───────────────────────

def _lianlian_private_key():
    if not LIANLIAN_RSA_PRIVATE_KEY:
        return None
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        from cryptography.hazmat.backends import default_backend
        return load_pem_private_key(
            LIANLIAN_RSA_PRIVATE_KEY.encode(), password=None, backend=default_backend()
        )
    except Exception as e:
        app.logger.error(f"Failed to load LianLian RSA private key: {e}")
        return None


def _lianlian_public_key():
    if not LIANLIAN_RSA_PUBLIC_KEY:
        return None
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.backends import default_backend
        return load_pem_public_key(
            LIANLIAN_RSA_PUBLIC_KEY.encode(), backend=default_backend()
        )
    except Exception as e:
        app.logger.error(f"Failed to load LianLian RSA public key: {e}")
        return None


def generate_lianlian_signature(method, uri, request_body="", query_string=""):
    """
    LLPAY-Signature: t=<epoch>,v=BASE64(SHA256WithRSA(payload, private_key))
    payload: METHOD&URI&EPOCH&BODY&QUERY_STRING
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    private_key = _lianlian_private_key()
    if private_key is None:
        return None, None

    epoch = str(int(time.time()))
    payload = f"{method}&{uri}&{epoch}&{request_body}&{query_string}"
    signature = private_key.sign(
        payload.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
    )
    return epoch, base64.b64encode(signature).decode()


def verify_lianlian_signature(epoch, sig_b64, response_body=""):
    """Verify LianLian's callback signature using their RSA public key."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.exceptions import InvalidSignature

    public_key = _lianlian_public_key()
    if public_key is None:
        app.logger.warning("No LianLian public key configured, skipping verification")
        return True

    try:
        public_key.verify(
            base64.b64decode(sig_b64),
            f"{epoch}&{response_body}".encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        app.logger.error("LianLian signature verification FAILED")
        return False


def _lianlian_auth_headers(method, uri, request_body="", query_string=""):
    auth_b64 = base64.b64encode(
        f"{LIANLIAN_MERCHANT_ID}:{LIANLIAN_AUTH_TOKEN}".encode()
    ).decode()
    epoch, sig = generate_lianlian_signature(method, uri, request_body, query_string)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}",
    }
    if epoch and sig:
        headers["LLPAY-Signature"] = f"t={epoch},v={sig}"
    return headers


def query_lianlian_order(order_id):
    if "placeholder" in LIANLIAN_MERCHANT_ID:
        return None
    try:
        uri = f"/v1/payments/{order_id}"
        resp = requests.get(
            f"{LIANLIAN_API_BASE}{uri}",
            headers=_lianlian_auth_headers("GET", uri),
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json().get("status")
    except Exception as e:
        app.logger.error(f"LianLian query error: {e}")
    return None


# ── Routes: Frontend page ──────────────────────────────────────
# The whole site is a single index.html embedded into this function
# (Vercel's Python pipeline does not copy root static files into the
# deployment output, so Flask must serve the page itself).

try:
    from embedded_html import INDEX_HTML
except ImportError:  # embedded module missing (e.g. not regenerated)
    INDEX_HTML = "<h1>Site not built</h1><p>Run python tools/embed_html.py</p>"


@app.route("/")
@app.route("/index.html")
def index_page():
    resp = app.response_class(INDEX_HTML, mimetype="text/html; charset=utf-8")
    resp.headers["Cache-Control"] = "public, max-age=300"
    return resp


@app.route("/robots.txt")
def robots_txt():
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Sitemap: {}/sitemap.xml\n".format(DOMAIN)
    )
    return app.response_class(body, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        "  <url>\n"
        "    <loc>{}/</loc>\n"
        '    <xhtml:link rel="alternate" hreflang="ja" href="{}/?lang=ja"/>\n'
        '    <xhtml:link rel="alternate" hreflang="zh" href="{}/?lang=zh"/>\n'
        '    <xhtml:link rel="alternate" hreflang="en" href="{}/?lang=en"/>\n'
        '    <xhtml:link rel="alternate" hreflang="ar" href="{}/?lang=ar"/>\n'
        '    <xhtml:link rel="alternate" hreflang="x-default" href="{}/"/>\n'
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>1.0</priority>\n"
        "  </url>\n"
        "</urlset>\n".format(*([DOMAIN] * 7))
    )
    resp = app.response_class(xml, mimetype="application/xml")
    resp.headers["Cache-Control"] = "public, max-age=3600"
    return resp


# ── Routes: Config ─────────────────────────────────────────────

@app.route("/config")
def config():
    """Expose payment gateway configuration to the frontend."""
    return jsonify({
        "stripePaymentLink": STRIPE_PAYMENT_LINK,
        "domain": DOMAIN,
        "gateways": {
            "stripe": bool(STRIPE_PAYMENT_LINK),
            "lianlian": not LIANLIAN_MERCHANT_ID.startswith("placeholder"),
        }
    })


# ── Routes: Payment Status ─────────────────────────────────────

@app.route("/api/verify-payment")
def verify_payment():
    """
    Check if a reading has been paid for.
    Query params: reading_id
    Returns: { paid: true/false }
    """
    reading_id = request.args.get("reading_id")
    if not reading_id:
        return jsonify({"paid": False, "error": "missing reading_id"}), 400

    record = kv_get_payment(reading_id)

    if record and record.get("status") == "paid":
        return jsonify({"paid": True})

    # If pending, double-check with LianLian in case its webhook hasn't fired yet
    if record and record.get("gateway") == "lianlian":
        order_id = record.get("lianlian_order_id")
        if order_id:
            try:
                if query_lianlian_order(order_id) == "SUCCEEDED":
                    mark_paid(reading_id, "lianlian")
                    return jsonify({"paid": True})
            except Exception:
                pass

    return jsonify({"paid": False})


# ── Routes: LianLian Order Creation ────────────────────────────

@app.route("/api/create-lianlian-order", methods=["POST"])
def create_lianlian_order():
    """
    Create a LianLian Global payment order (Cashier mode).
    SHA256WithRSA signing per LianLian API spec.
    Request body: { reading_id, birth_info, return_url }
    Returns: { url: lianlian_cashier_url }
    """
    try:
        data = request.get_json()
        reading_id = data.get("reading_id")
        return_url = data.get(
            "return_url", f"{DOMAIN}/?reading_id={reading_id}&paid=true"
        )

        if not reading_id:
            return jsonify({"error": "缺少 reading_id"}), 400

        try:
            uuid.UUID(reading_id)
        except (ValueError, AttributeError):
            return jsonify({"error": "无效的 reading_id"}), 400

        if "placeholder" in LIANLIAN_MERCHANT_ID:
            return jsonify({
                "error": "连连支付尚未配置\n请设置 LIANLIAN_MERCHANT_ID, LIANLIAN_AUTH_TOKEN, LIANLIAN_RSA_PRIVATE_KEY 后重试"
            }), 500

        lianlian_order_id = f"ZWD{reading_id.replace('-', '')[:20]}"

        payload = {
            "merchant_id": LIANLIAN_MERCHANT_ID,
            "order_id": lianlian_order_id,
            "amount": "9.99",
            "currency": "USD",
            "order_desc": "紫微斗数详细解盘",
            "return_url": return_url,
            "notification_url": f"{DOMAIN}/webhook/lianlian",
        }

        request_body = json.dumps(payload, separators=(",", ":"))
        headers = _lianlian_auth_headers("POST", "/v1/cashier/createpay", request_body)

        resp = requests.post(
            f"{LIANLIAN_API_BASE}/v1/cashier/createpay",
            data=request_body,
            headers=headers,
            timeout=15,
        )

        if resp.status_code == 200:
            result = resp.json()
            payment_url = result.get("payment_url") or result.get("cashier_url")
            if payment_url:
                now = int(time.time())
                kv_set_payment(reading_id, {
                    "status": "pending",
                    "gateway": "lianlian",
                    "lianlian_order_id": lianlian_order_id,
                    "created_at": now,
                })
                # Store order→reading mapping so the webhook can resolve it
                r = kv()
                if r:
                    try:
                        r.set(f"lianlian:{lianlian_order_id}", reading_id, ex=PAY_TTL_SECONDS)
                    except Exception as e:
                        app.logger.error(f"KV mapping set error: {e}")
                return jsonify({"url": payment_url})
            else:
                app.logger.error(f"LianLian: no payment_url in response: {result}")
                return jsonify({"error": "创建支付失败，请稍后再试"}), 500
        else:
            app.logger.error(f"LianLian API error: {resp.status_code} {resp.text}")
            return jsonify({"error": "支付服务暂时不可用，请稍后再试"}), 500

    except requests.exceptions.RequestException as e:
        app.logger.error(f"LianLian request error: {e}")
        return jsonify({"error": "支付服务网络错误，请稍后再试"}), 500
    except Exception as e:
        app.logger.error(f"LianLian unexpected error: {e}")
        return jsonify({"error": "服务器错误，请重试"}), 500


# ── Routes: Webhooks ───────────────────────────────────────────

@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """
    Stripe Payment Link confirmation.
    reading_id is passed as client_reference_id in the payment link URL:
      https://buy.stripe.com/xxx?client_reference_id=<reading_id>
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        app.logger.error("Invalid Stripe webhook payload")
        return jsonify({"error": "invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        app.logger.error("Invalid Stripe webhook signature")
        return jsonify({"error": "invalid signature"}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        reading_id = session.get("client_reference_id") or (
            session.get("metadata") or {}
        ).get("reading_id")
        if reading_id:
            mark_paid(reading_id, "stripe")
            app.logger.info(f"Payment confirmed for reading_id={reading_id}")

    return jsonify({"status": "ok"})


@app.route("/webhook/lianlian", methods=["POST"])
def lianlian_webhook():
    """
    LianLian Global payment notification.
    Signature: LLPAY-Signature: t=<epoch>,v=<base64_rsa_signature>
    Must return HTTP 200 to acknowledge.
    """
    try:
        raw_body = request.get_data(as_text=True)
        data = request.get_json()
        if not data:
            app.logger.error("LianLian webhook: empty body")
            return jsonify({"status": "error", "message": "empty body"}), 400

        app.logger.info(f"LianLian webhook received: {raw_body}")

        # Verify signature using LianLian's RSA public key
        sig_header = request.headers.get("LLPAY-Signature", "")
        if sig_header and LIANLIAN_RSA_PUBLIC_KEY:
            try:
                t_val = sig_header.split("t=")[1].split(",")[0]
                v_val = sig_header.split("v=")[1]
                if not verify_lianlian_signature(t_val, v_val, raw_body):
                    app.logger.error("LianLian webhook: invalid signature")
                    return jsonify({"status": "error", "message": "invalid signature"}), 403
            except (IndexError, ValueError) as e:
                app.logger.error(f"LianLian webhook: failed to parse signature: {e}")

        order_id = data.get("order_id") or data.get("out_trade_no")
        payment_status = data.get("status") or data.get("trade_status")

        if payment_status in ("SUCCEEDED", "PS", "TRADE_SUCCESS", "SUCCESS"):
            # Find reading_id by lianlian_order_id — scan is impractical in KV,
            # so the create step stores order→reading mapping instead.
            reading_id = None
            r = kv()
            if r:
                try:
                    reading_id = r.get(f"lianlian:{order_id}")
                except Exception:
                    reading_id = None
            if reading_id:
                mark_paid(reading_id, "lianlian")
                app.logger.info(f"LianLian payment confirmed: order={order_id}")
            else:
                app.logger.warning(f"LianLian webhook: unknown order_id={order_id}")

        return jsonify({"status": "ok"})

    except Exception as e:
        app.logger.error(f"LianLian webhook error: {e}")
        return jsonify({"status": "ok"})
