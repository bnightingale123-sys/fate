# -*- coding: utf-8 -*-
"""Upgrade index.html with high-converting CRO (Conversion Rate Optimization) elements:
1. CSS: countdown timer, trust badges, hook card, blur lock wrapper.
2. I18N: Japanese, Chinese, English, Arabic copy for all new components.
3. Hook card inside renderChart(): Highlights turning points, major cycle risks, soulmate timing, peak wealth.
4. Blur teaser in renderDetail(): For unpaid users, show teaser with blurred deep sections and unlock CTA.
5. High-converting modal in showPaymentDialog(): Timer, trust badges (Stripe, SSL, Visa/Mastercard/Amex/JCB), checkmarks.
6. Ritual animation in onSubmit(): 4-stage calculation steps.
7. Footer legal modals: Privacy policy and terms.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(ROOT, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------
# 1. Inject CSS before </style>
# -------------------------------------------------------------
css_addition = """
/* ===== High-Converting CRO Enhancements ===== */
.pay-timer-badge {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35);
  color: #f87171; padding: 6px 16px; border-radius: 20px; font-size: 0.82rem; font-weight: bold; margin-bottom: 14px;
}
.pay-timer-num { font-variant-numeric: tabular-nums; color: #fca5a5; font-size: 0.95rem; }

.modal-trust-row {
  display: flex; align-items: center; justify-content: center; gap: 14px; margin-top: 16px; padding-top: 14px;
  border-top: 1px solid rgba(255,255,255,0.08); flex-wrap: wrap;
}
.modal-trust-item {
  display: flex; align-items: center; gap: 5px; font-size: 0.74rem; color: #a09888;
}
.modal-trust-item .trust-dot { color: #10B981; font-weight: bold; font-size: 0.9rem; }
.card-logos {
  display: flex; gap: 6px; align-items: center; justify-content: center; margin-top: 10px; flex-wrap: wrap;
}
.card-badge {
  font-size: 0.65rem; font-weight: bold; padding: 2px 7px; border-radius: 4px;
  background: rgba(255,255,255,0.08); color: #d0c8b8; border: 1px solid rgba(255,255,255,0.14);
}

.pay-features-list {
  text-align: left; margin: 14px 0 16px; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;
}
.pay-features-list li {
  font-size: 0.82rem; color: #c0b8a8; display: flex; align-items: flex-start; gap: 8px; line-height: 1.5;
}
.pay-features-list li span.chk {
  color: #10B981; font-weight: bold; flex-shrink: 0;
}

/* Hook Card in Chart View */
.hook-card {
  margin-top: 24px; padding: 22px 20px;
  background: linear-gradient(135deg, rgba(45, 27, 78, 0.75) 0%, rgba(26, 16, 53, 0.9) 100%);
  border: 1.5px solid rgba(212, 175, 55, 0.45); border-radius: 16px; text-align: left; position: relative;
  box-shadow: 0 12px 32px rgba(0,0,0,0.45);
}
.hook-header {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;
}
.hook-title {
  font-size: 1.05rem; font-weight: bold; color: #D4AF37; display: flex; align-items: center; gap: 6px;
}
.hook-alert-tag {
  background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);
  font-size: 0.72rem; padding: 2px 10px; border-radius: 12px; font-weight: bold; animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
.hook-analysis-box {
  background: rgba(0, 0, 0, 0.3); border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;
  font-size: 0.83rem; color: #d0c8b8; line-height: 1.65; border-left: 3px solid #D4AF37;
}
.hook-locked-items {
  display: flex; flex-direction: column; gap: 8px; margin-bottom: 18px;
}
.hook-locked-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; border-radius: 8px; background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(212,175,55,0.3);
  font-size: 0.82rem; color: #b8b0a0;
}
.hook-locked-item .lock-icon {
  font-size: 0.85rem; color: #D4AF37; font-weight: bold; display: flex; align-items: center; gap: 4px;
}
.btn-unlock-gold {
  width: 100%; height: 54px;
  background: linear-gradient(135deg, #D4AF37 0%, #F59E0B 100%);
  color: #120a20; border: none; border-radius: 27px; font-size: 1.02rem; font-weight: bold;
  cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.35); transition: all 0.25s;
}
.btn-unlock-gold:hover {
  transform: translateY(-2px); box-shadow: 0 12px 30px rgba(212, 175, 55, 0.55); opacity: 0.95;
}
.hook-social-proof {
  text-align: center; font-size: 0.74rem; color: #8a7e6b; margin-top: 10px;
}

/* Detail View Blur Locked Overlay */
.blur-locked-wrapper {
  position: relative; margin-top: 24px; border-radius: 16px; overflow: hidden;
  border: 1px solid rgba(212,175,55,0.25);
}
.blur-locked-content {
  filter: blur(6px); opacity: 0.35; pointer-events: none; user-select: none;
  min-height: 480px;
}
.blur-overlay-banner {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center; background: radial-gradient(circle, rgba(18,10,36,0.92) 0%, rgba(10,10,26,0.98) 100%);
  padding: 24px 20px; text-align: center; z-index: 10;
}
.blur-lock-badge {
  width: 58px; height: 58px; border-radius: 50%; background: rgba(212,175,55,0.15);
  border: 1px solid rgba(212,175,55,0.35); display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; color: #D4AF37; margin-bottom: 14px;
}
.blur-lock-title {
  font-size: 1.25rem; font-weight: bold; color: #fff; margin-bottom: 8px;
}
.blur-lock-desc {
  font-size: 0.86rem; color: #c0b8a8; max-width: 480px; line-height: 1.6; margin-bottom: 18px;
}
.modal-price-tag {
  display: flex; align-items: baseline; justify-content: center; gap: 8px; margin: 10px 0 14px;
}
.modal-price-curr { font-size: 2.2rem; font-weight: bold; color: #D4AF37; }
.modal-price-orig { font-size: 1.1rem; color: #7a7060; text-decoration: line-through; }
"""

if "/* ===== High-Converting CRO Enhancements ===== */" not in content:
    content = content.replace("</style>", css_addition + "\n</style>", 1)

# -------------------------------------------------------------
# 2. Update Footer Links to include Privacy, Terms, Support
# -------------------------------------------------------------
footer_old = """      <a href="#features" data-i18n="header.nav.services">服务分类</a>
      <a href="#form" data-i18n="header.nav.chart">在线排盘</a>
      <a href="#pricing" data-i18n="header.nav.pricing">定价</a>
      <a href="#faq" data-i18n="header.nav.faq">常见问题</a>
    </div>"""

footer_new = """      <a href="#features" data-i18n="header.nav.services">服务分类</a>
      <a href="#form" data-i18n="header.nav.chart">在线排盘</a>
      <a href="#pricing" data-i18n="header.nav.pricing">定价</a>
      <a href="#faq" data-i18n="header.nav.faq">常见问题</a>
      <a href="javascript:void(0)" onclick="App.showPrivacyModal()" data-i18n="footer.privacy">プライバシーポリシー</a>
      <a href="javascript:void(0)" onclick="App.showTermsModal()" data-i18n="footer.terms">利用規約</a>
      <a href="mailto:support@yourfate.xyz" data-i18n="footer.contact">サポート</a>
    </div>"""

content = content.replace(footer_old, footer_new, 1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("CSS and footer updated successfully!")
