"""
紫微斗数解密服务 — Web Server
==============================
Flask backend for yourfate.xyz
- Serves the Zi Wei Dou Shu SPA (index.html)
- Stripe Payment Link (hosted checkout, no API keys needed)
- LianLian Global (连连跨境) payment integration (SHA256WithRSA signing)
- SQLite payment tracking
- Webhook handlers for both gateways

Setup:
  1. Set environment variables:
     STRIPE_PAYMENT_LINK=https://buy.stripe.com/xxx
     STRIPE_WEBHOOK_SECRET=whsec_xxx     (webhook verification only)
     LianLian Global:
       LIANLIAN_MERCHANT_ID=xxx          (商户号, also developerId)
       LIANLIAN_AUTH_TOKEN=xxx           (masterToken for Basic auth)
       LIANLIAN_RSA_PRIVATE_KEY=xxx      (RSA私钥 PEM格式, 用于签名)
       LIANLIAN_RSA_PUBLIC_KEY=xxx       (连连RSA公钥 PEM格式, 用于验签回调)
       LIANLIAN_API_BASE=https://api.lianlianglobal.com
  2. pip install flask stripe python-dotenv requests cryptography
  3. python server.py

Stripe Dashboard: https://dashboard.stripe.com/
LianLian Global: https://docs.lianlianglobal.com.cn/
"""

import base64
import json
import os
import sqlite3
import time
import uuid
import requests
from datetime import datetime

from flask import Flask, request, jsonify, send_file, redirect
import stripe

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Configuration ──────────────────────────────────────────────

STRIPE_PAYMENT_LINK = os.environ.get(
    "STRIPE_PAYMENT_LINK", "https://buy.stripe.com/eVq5kDgDY8et2Um2h3g3600"
)
STRIPE_WEBHOOK_SECRET = os.environ.get(
    "STRIPE_WEBHOOK_SECRET", "whsec_placeholder_replace_me"
)
LIANLIAN_MERCHANT_ID = os.environ.get(
    "LIANLIAN_MERCHANT_ID", "placeholder_merchant_id"
)
LIANLIAN_AUTH_TOKEN = os.environ.get(
    "LIANLIAN_AUTH_TOKEN", "placeholder_auth_token"
)
LIANLIAN_RSA_PRIVATE_KEY = os.environ.get(
    "LIANLIAN_RSA_PRIVATE_KEY", ""
)
LIANLIAN_RSA_PUBLIC_KEY = os.environ.get(
    "LIANLIAN_RSA_PUBLIC_KEY", ""
)
# LianLian Global API endpoints
LIANLIAN_API_BASE = os.environ.get(
    "LIANLIAN_API_BASE", "https://api.lianlianglobal.com"
)
DOMAIN = os.environ.get("DOMAIN", "https://yourfate.xyz")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "payments.db")

# Note: no stripe.api_key needed — we use hosted Payment Links only.
# The stripe library is used solely for webhook signature verification.

app = Flask(__name__, static_folder=".", static_url_path="")


# ── Database ────────────────────────────────────────────────────

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reading_id TEXT UNIQUE NOT NULL,
                stripe_session_id TEXT UNIQUE,
                lianlian_order_id TEXT UNIQUE,
                payment_gateway TEXT DEFAULT 'stripe',
                status TEXT DEFAULT 'pending',
                birth_info TEXT,
                created_at INTEGER,
                paid_at INTEGER
            )"""
        )
        # Add columns if they don't exist (migration for existing DB)
        for col, col_type in [
            ("lianlian_order_id", "TEXT UNIQUE"),
            ("payment_gateway", "TEXT DEFAULT 'stripe'"),
        ]:
            try:
                conn.execute(f"ALTER TABLE payments ADD COLUMN {col} {col_type}")
            except sqlite3.OperationalError:
                pass  # Column already exists
        conn.commit()


def get_payment(reading_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT * FROM payments WHERE reading_id = ?", (reading_id,)
        ).fetchone()
    return row


def mark_paid(reading_id, gateway="stripe"):
    """
    Mark a reading as paid. Creates the record if it doesn't exist yet
    (Payment Link webhook can arrive before any local record is created).
    """
    with sqlite3.connect(DB_PATH) as conn:
        now = int(time.time())
        conn.execute(
            """INSERT INTO payments (reading_id, payment_gateway, status, created_at, paid_at)
               VALUES (?, ?, 'paid', ?, ?)
               ON CONFLICT(reading_id) DO UPDATE SET
               status = 'paid',
               paid_at = excluded.paid_at""",
            (reading_id, gateway, now, now),
        )
        conn.commit()


# ── Routes: Static ──────────────────────────────────────────────

@app.route("/")
def index():
    return send_file("index.html")


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


# ── Routes: API ─────────────────────────────────────────────────

@app.route("/api/verify-payment", methods=["GET"])
def verify_payment():
    """
    Check if a reading has been paid for.
    Query params: reading_id
    Returns: { paid: true/false }
    """
    reading_id = request.args.get("reading_id")
    if not reading_id:
        return jsonify({"paid": False, "error": "缺少 reading_id"}), 400

    row = get_payment(reading_id)

    if row and row[3] == "paid":  # status column
        return jsonify({"paid": True})

    # If pending, double-check with the payment gateway in case webhook hasn't fired yet
    if row:
        gateway = row[4] if len(row) > 4 else "stripe"  # payment_gateway column
        session_id = row[2]  # stripe_session_id or lianlian_order_id
        if session_id and gateway == "lianlian":
            try:
                # Query LianLian for order status
                status = query_lianlian_order(session_id)
                if status == "SUCCEEDED":
                    mark_paid(reading_id)
                    return jsonify({"paid": True})
            except Exception:
                pass

    return jsonify({"paid": False})


# ── LianLian Global: RSA Signing Helpers ────────────────────────

def _lianlian_private_key():
    """Load the merchant RSA private key (PEM format)."""
    if not LIANLIAN_RSA_PRIVATE_KEY:
        return None
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        from cryptography.hazmat.backends import default_backend
        key = load_pem_private_key(
            LIANLIAN_RSA_PRIVATE_KEY.encode(),
            password=None,
            backend=default_backend()
        )
        return key
    except Exception as e:
        app.logger.error(f"Failed to load LianLian RSA private key: {e}")
        return None


def _lianlian_public_key():
    """Load LianLian's RSA public key (PEM format) for verifying callbacks."""
    if not LIANLIAN_RSA_PUBLIC_KEY:
        return None
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.backends import default_backend
        key = load_pem_public_key(
            LIANLIAN_RSA_PUBLIC_KEY.encode(),
            backend=default_backend()
        )
        return key
    except Exception as e:
        app.logger.error(f"Failed to load LianLian RSA public key: {e}")
        return None


def generate_lianlian_signature(method, uri, request_body="", query_string=""):
    """
    Generate LLPAY-Signature header value.

    Payload: METHOD&URI&EPOCH&BODY&QUERY_STRING
    Signature: BASE64(SHA256WithRSA.sign(payload, rsa_private_key))
    Header:   t=<epoch>,v=<signature>
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    private_key = _lianlian_private_key()
    if private_key is None:
        return None, None

    epoch = str(int(time.time()))
    payload = f"{method}&{uri}&{epoch}&{request_body}&{query_string}"

    signature = private_key.sign(
        payload.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    sig_b64 = base64.b64encode(signature).decode()

    return epoch, sig_b64


def verify_lianlian_signature(epoch, sig_b64, response_body=""):
    """
    Verify LianLian's response/callback signature using their RSA public key.
    Payload: epoch&response_body
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.exceptions import InvalidSignature

    public_key = _lianlian_public_key()
    if public_key is None:
        app.logger.warning("No LianLian public key configured, skipping signature verification")
        return True

    payload = f"{epoch}&{response_body}"
    try:
        public_key.verify(
            base64.b64decode(sig_b64),
            payload.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        app.logger.error("LianLian signature verification FAILED")
        return False


def _lianlian_auth_headers(method, uri, request_body="", query_string=""):
    """
    Build standard LianLian Global request headers:
      - Authorization: Basic base64(merchantId:authToken)
      - LLPAY-Signature: t=<epoch>,v=<base64_rsa_signature>
      - Content-Type: application/json
    """
    auth_raw = f"{LIANLIAN_MERCHANT_ID}:{LIANLIAN_AUTH_TOKEN}"
    auth_b64 = base64.b64encode(auth_raw.encode()).decode()

    epoch, sig = generate_lianlian_signature(method, uri, request_body, query_string)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}",
    }
    if epoch and sig:
        headers["LLPAY-Signature"] = f"t={epoch},v={sig}"

    return headers


def upsert_lianlian_payment(reading_id, lianlian_order_id, birth_info):
    """Save or update a LianLian payment record."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO payments (reading_id, lianlian_order_id, payment_gateway, status, birth_info, created_at)
               VALUES (?, ?, 'lianlian', 'pending', ?, ?)
               ON CONFLICT(reading_id) DO UPDATE SET
               lianlian_order_id = excluded.lianlian_order_id,
               payment_gateway = 'lianlian',
               status = 'pending',
               birth_info = excluded.birth_info,
               created_at = excluded.created_at""",
            (reading_id, lianlian_order_id, json.dumps(birth_info), int(time.time())),
        )
        conn.commit()


def query_lianlian_order(order_id):
    """Query LianLian for an order's payment status.
    Returns status string or None on failure.
    """
    if "placeholder" in LIANLIAN_MERCHANT_ID:
        return None
    try:
        uri = f"/v1/payments/{order_id}"
        headers = _lianlian_auth_headers("GET", uri)
        resp = requests.get(
            f"{LIANLIAN_API_BASE}{uri}",
            headers=headers,
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("status")
    except Exception as e:
        app.logger.error(f"LianLian query error: {e}")
    return None


@app.route("/api/create-lianlian-order", methods=["POST"])
def create_lianlian_order():
    """
    Create a LianLian Global payment order (Cashier mode).
    Uses SHA256WithRSA signing per LianLian API spec.

    Request body: { reading_id, birth_info, return_url }
    Returns: { url: lianlian_cashier_url }
    """
    try:
        data = request.get_json()
        reading_id = data.get("reading_id")
        birth_info = data.get("birth_info", {})
        return_url = data.get("return_url", f"{DOMAIN}/?reading_id={reading_id}&paid=true")

        if not reading_id:
            return jsonify({"error": "缺少 reading_id"}), 400

        try:
            uuid.UUID(reading_id)
        except (ValueError, AttributeError):
            return jsonify({"error": "无效的 reading_id"}), 400

        # Handle placeholder keys gracefully
        if "placeholder" in LIANLIAN_MERCHANT_ID:
            return jsonify({
                "error": "连连支付尚未配置\n请设置 LIANLIAN_MERCHANT_ID, LIANLIAN_AUTH_TOKEN, LIANLIAN_RSA_PRIVATE_KEY 后重试"
            }), 500

        # Generate unique order ID for LianLian
        lianlian_order_id = f"ZWD{reading_id.replace('-', '')[:20]}"

        # Build LianLian payment request body
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

        # Call LianLian API — Cashier create payment
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
                # Save to database
                upsert_lianlian_payment(reading_id, lianlian_order_id, birth_info)
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


# ── Routes: Webhook ─────────────────────────────────────────────

@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """
    Stripe webhook endpoint. Handles checkout.session.completed events
    from Payment Links. Requires raw request body for signature verification.

    The reading_id is passed as client_reference_id in the payment link URL:
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
        return jsonify({"error": "无效的请求体"}), 400
    except stripe.error.SignatureVerificationError:
        app.logger.error("Invalid Stripe webhook signature")
        return jsonify({"error": "无效的签名"}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Payment Link passes client_reference_id from URL query param
        reading_id = session.get("client_reference_id") or (
            session.get("metadata", {}) or {}
        ).get("reading_id")
        if reading_id:
            mark_paid(reading_id)
            app.logger.info(f"Payment confirmed for reading_id={reading_id}")

    return jsonify({"status": "ok"})


@app.route("/webhook/lianlian", methods=["POST"])
def lianlian_webhook():
    """
    LianLian Global webhook/notify endpoint.
    Handles payment result notifications from LianLian.

    Signature format: LLPAY-Signature: t=<epoch>,v=<base64_rsa_signature>
    Verify using LianLian's RSA public key.
    Must return HTTP 200 to acknowledge receipt.
    """
    try:
        raw_body = request.get_data(as_text=True)
        data = request.get_json()
        if not data:
            app.logger.error("LianLian webhook: empty body")
            return jsonify({"status": "error", "message": "empty body"}), 400

        app.logger.info(f"LianLian webhook received: {raw_body}")

        # Verify LLPAY-Signature header using LianLian's RSA public key
        sig_header = request.headers.get("LLPAY-Signature", "")
        if sig_header and LIANLIAN_RSA_PUBLIC_KEY:
            try:
                # Parse t=<epoch>,v=<signature>
                t_val = sig_header.split("t=")[1].split(",")[0]
                v_val = sig_header.split("v=")[1]
                if not verify_lianlian_signature(t_val, v_val, raw_body):
                    app.logger.error("LianLian webhook: invalid signature")
                    return jsonify({"status": "error", "message": "invalid signature"}), 403
            except (IndexError, ValueError) as e:
                app.logger.error(f"LianLian webhook: failed to parse signature header: {e}")

        # Extract order info
        order_id = data.get("order_id") or data.get("out_trade_no")
        payment_status = data.get("status") or data.get("trade_status")

        # Map LianLian status to our status
        if payment_status in ("SUCCEEDED", "PS", "TRADE_SUCCESS", "SUCCESS"):
            # Find reading_id by lianlian_order_id
            with sqlite3.connect(DB_PATH) as conn:
                row = conn.execute(
                    "SELECT reading_id FROM payments WHERE lianlian_order_id = ?",
                    (order_id,),
                ).fetchone()
                if row:
                    mark_paid(row[0])
                    app.logger.info(f"LianLian payment confirmed: order={order_id}, reading={row[0]}")
                else:
                    app.logger.warning(f"LianLian webhook: unknown order_id={order_id}")

        return jsonify({"status": "ok"})

    except Exception as e:
        app.logger.error(f"LianLian webhook error: {e}")
        # Still return 200 to acknowledge receipt (LianLian retries on non-200)
        return jsonify({"status": "ok"})


# ── Main ────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()

    if "placeholder" in LIANLIAN_MERCHANT_ID:
        print("=" * 60)
        print("LianLian not configured yet — Stripe Payment Link still works.")
        print("  To enable LianLian Global (连连跨境) — SHA256WithRSA:")
        print("    export LIANLIAN_MERCHANT_ID=xxx")
        print("    export LIANLIAN_AUTH_TOKEN=xxx")
        print("    export LIANLIAN_RSA_PRIVATE_KEY=\"$(cat /path/to/merchant_private_key.pem)\"")
        print("    export LIANLIAN_RSA_PUBLIC_KEY=\"$(cat /path/to/lianlian_public_key.pem)\"")
        print("=" * 60)

    stripe_mode = "PAYMENT LINK: " + STRIPE_PAYMENT_LINK
    lianlian_configured = (
        not LIANLIAN_MERCHANT_ID.startswith("placeholder")
        and LIANLIAN_RSA_PRIVATE_KEY
        and LIANLIAN_AUTH_TOKEN
    )
    lianlian_mode = "CONFIGURED" if lianlian_configured else "PLACEHOLDER (not configured)"
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0" if os.environ.get("RENDER") else "127.0.0.1"
    print(f"Zi Wei Dou Shu Web Server starting...")
    print(f"  URL: http://{host}:{port}")
    print(f"  Domain: {DOMAIN}")
    print(f"  Stripe: {stripe_mode}")
    print(f"  LianLian: {lianlian_mode}")
    print(f"  Database: {DB_PATH}")

    app.run(host=host, port=port, debug=False)
