#!/usr/bin/env python3
"""Add data-i18n attributes to all remaining static HTML elements in index.html."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the body content (between <body> and first <script>)
body_start = html.find('<body>')
body_end_tag = html.find('>', body_start) + 1
first_script = html.find('<script>', body_end_tag)
body_content = html[body_end_tag:first_script]
prefix = html[:body_end_tag]
suffix = html[first_script:]

# ── Define all i18n mappings ──
# Format: (exact_string_in_html, data_i18n_key)
# We match text content and wrap it with data-i18n span or add attr to parent

mappings = [
    # ── How It Works section ──
    ('<div class="section-label">如何使用</div>', '<div class="section-label" data-i18n="how.label">如何使用</div>'),
    ('<h2 class="section-title">三步揭秘你的命运密码</h2>', '<h2 class="section-title" data-i18n="how.title">三步揭秘你的命运密码</h2>'),
    ('<p class="section-desc">简单三步，获取专业级紫微斗数命盘解读</p>', '<p class="section-desc" data-i18n="how.desc">简单三步，获取专业级紫微斗数命盘解读</p>'),
    ('<div class="step-title">输入出生信息</div>', '<div class="step-title" data-i18n="how.step1.title">输入出生信息</div>'),
    ('<div class="step-desc">填写你的出生年月日时和性别，支持公历和农历两种日期输入方式</div>', '<div class="step-desc" data-i18n="how.step1.desc">填写你的出生年月日时和性别，支持公历和农历两种日期输入方式</div>'),
    ('<div class="step-title">智能排盘</div>', '<div class="step-title" data-i18n="how.step2.title">智能排盘</div>'),
    ('<div class="step-desc">系统自动计算十二宫星曜分布、四化飞星、大限运势，生成专业命盘</div>', '<div class="step-desc" data-i18n="how.step2.desc">系统自动计算十二宫星曜分布、四化飞星、大限运势，生成专业命盘</div>'),
    ('<div class="step-title">详细解盘</div>', '<div class="step-title" data-i18n="how.step3.title">详细解盘</div>'),
    ('<div class="step-desc">获取十二宫详细解读、命盘格局分析、大限运势推演，全面了解人生运势</div>', '<div class="step-desc" data-i18n="how.step3.desc">获取十二宫详细解读、命盘格局分析、大限运势推演，全面了解人生运势</div>'),

    # ── Form section ──
    ('<div class="section-label">在线排盘</div>', '<div class="section-label" data-i18n="form.label">在线排盘</div>'),
    ('<h2 class="section-title">填入你的出生信息</h2>', '<h2 class="section-title" data-i18n="form.title">填入你的出生信息</h2>'),
    ('<p class="section-desc">准确填写出生资料，即可免费查看紫微斗数命盘</p>', '<p class="section-desc" data-i18n="form.desc">准确填写出生资料，即可免费查看紫微斗数命盘</p>'),
    # Form fields
    ('<label class="form-label">姓名（选填）</label>', '<label class="form-label" data-i18n="form.name.label">姓名（选填）</label>'),
    ('<input class="form-input" id="inputName" placeholder="请输入您的姓名" maxlength="20">', '<input class="form-input" id="inputName" data-i18n-placeholder="form.name.placeholder" placeholder="请输入您的姓名" maxlength="20">'),
    ('<label class="form-label">性别</label>', '<label class="form-label" data-i18n="form.gender.label">性别</label>'),
    ('<div class="radio-item active" data-gender="male" onclick="App.selectGender(this)">&#x1F468; 男</div>', '<div class="radio-item active" data-gender="male" onclick="App.selectGender(this)" data-i18n="form.gender.male">&#x1F468; 男</div>'),
    ('<div class="radio-item" data-gender="female" onclick="App.selectGender(this)">&#x1F469; 女</div>', '<div class="radio-item" data-gender="female" onclick="App.selectGender(this)" data-i18n="form.gender.female">&#x1F469; 女</div>'),
    ('<label class="form-label">出生日期</label>', '<label class="form-label" data-i18n="form.date.label">出生日期</label>'),
    ('<div class="date-tab active" data-type="solar" onclick="App.selectDateType(this)">&#x2600;&#xFE0F; 公历</div>', '<div class="date-tab active" data-type="solar" onclick="App.selectDateType(this)" data-i18n="form.date.solar">&#x2600;&#xFE0F; 公历</div>'),
    ('<div class="date-tab" data-type="lunar" onclick="App.selectDateType(this)">&#x1F319; 农历</div>', '<div class="date-tab" data-type="lunar" onclick="App.selectDateType(this)" data-i18n="form.date.lunar">&#x1F319; 农历</div>'),
    ('<label class="form-label">出生时辰</label>', '<label class="form-label" data-i18n="form.hour.label">出生时辰</label>'),
    # Submit button
    ('<button class="btn-submit" id="btnSubmit" onclick="App.onSubmit()">\n          开始排盘\n        </button>', '<button class="btn-submit" id="btnSubmit" onclick="App.onSubmit()" data-i18n="form.submit">\n          开始排盘\n        </button>'),
    # Form note
    ('<div class="form-note">命理分析仅供参考 · 命运由自己掌握</div>', '<div class="form-note" data-i18n="form.note">命理分析仅供参考 · 命运由自己掌握</div>'),

    # ── Chart Result ──
    ('<div class="section-label">排盘结果</div>', '<div class="section-label" data-i18n="result.label">排盘结果</div>'),
    ('<h2 class="section-title">你的紫微斗数命盘</h2>', '<h2 class="section-title" data-i18n="result.title">你的紫微斗数命盘</h2>'),

    # ── Testimonials ──
    ('<div class="section-label">用户评价</div>', '<div class="section-label" data-i18n="testimonials.label">用户评价</div>'),
    ('<h2 class="section-title">他们都在用紫微斗数解密人生</h2>', '<h2 class="section-title" data-i18n="testimonials.title">他们都在用紫微斗数解密人生</h2>'),
    # Stats
    ('<div class="stat-label">已服务用户</div>', '<div class="stat-label" data-i18n="stats.users">已服务用户</div>'),
    ('<div class="stat-label">好评率</div>', '<div class="stat-label" data-i18n="stats.rating">好评率</div>'),
    ('<div class="stat-label">隐私保护</div>', '<div class="stat-label" data-i18n="stats.privacy">隐私保护</div>'),

    # ── Pricing ──
    ('<div class="section-label">定价</div>', '<div class="section-label" data-i18n="pricing.label">定价</div>'),
    ('<h2 class="section-title">选择适合你的方案</h2>', '<h2 class="section-title" data-i18n="pricing.title">选择适合你的方案</h2>'),
    ('<div class="pricing-badge">&#x1F31F; 最受欢迎</div>', '<div class="pricing-badge" data-i18n="pricing.badge">&#x1F31F; 最受欢迎</div>'),
    ('<div class="pricing-name">详细解盘套餐</div>', '<div class="pricing-name" data-i18n="pricing.name">详细解盘套餐</div>'),
    ('<div class="pricing-period">一次性付费 · 永久查看</div>', '<div class="pricing-period" data-i18n="pricing.period">一次性付费 · 永久查看</div>'),

    # ── FAQ ──
    ('<div class="section-label">常见问题</div>', '<div class="section-label" data-i18n="faq.label">常见问题</div>'),
    ('<h2 class="section-title">有任何疑问？我们为你解答</h2>', '<h2 class="section-title" data-i18n="faq.title">有任何疑问？我们为你解答</h2>'),

    # ── CTA ──
    ('<h2 class="cta-title">准备好解密你的人生运势了吗？</h2>', '<h2 class="cta-title" data-i18n="cta.title">准备好解密你的人生运势了吗？</h2>'),
    ('<p class="cta-desc">输入出生信息，即刻获取你的专属紫微斗数命盘解读</p>', '<p class="cta-desc" data-i18n="cta.desc">输入出生信息，即刻获取你的专属紫微斗数命盘解读</p>'),

    # ── Footer ──
    ('<div class="footer-desc">紫微斗数在线命理解密服务平台</div>', '<div class="footer-desc" data-i18n="footer.desc">紫微斗数在线命理解密服务平台</div>'),
    # Note: footer nav links need separate handling since text is inside <a> tags

    # ── Modal defaults ──
    ('<button class="modal-btn" onclick="App.closeModal()">知道了</button>', '<button class="modal-btn" onclick="App.closeModal()" data-i18n="modal.ok">知道了</button>'),
    ('<button class="modal-btn-cancel" style="display:none;" onclick="App.closeModal()">暂不需要</button>', '<button class="modal-btn-cancel" style="display:none;" onclick="App.closeModal()" data-i18n="modal.cancel">暂不需要</button>'),
]

count = 0
for old, new in mappings:
    if old in body_content:
        body_content = body_content.replace(old, new)
        count += 1
    else:
        # Try to find something close
        # Strip whitespace variations
        old_compact = re.sub(r'\s+', ' ', old)
        print(f"NOT FOUND: {old[:80]}...")

print(f"Applied: {count}/{len(mappings)} replacements")

# ── Handle FAQ items with data-i18n ──
# FAQ Q and A pairs
faq_pairs = [
    ('q1', 'a1'),
    ('q2', 'a2'),
    ('q3', 'a3'),
    ('q4', 'a4'),
]

# Find all faq-q and faq-a elements
faq_pattern = r'<div class="faq-q">([^<]+)<span class="arrow-icon">'
faq_matches = list(re.finditer(faq_pattern, body_content))

if len(faq_matches) >= 4:
    for i, (qk, ak) in enumerate(faq_pairs):
        m = faq_matches[i]
        old_q = m.group(0)
        new_q = f'<div class="faq-q"><span data-i18n="faq.{qk}">{m.group(1)}</span><span class="arrow-icon">'
        body_content = body_content.replace(old_q, new_q)

# FAQ answers
faq_a_pattern = r'<div class="faq-a"><p>([^<]+)</p></div>'
faq_a_matches = list(re.finditer(faq_a_pattern, body_content))

if len(faq_a_matches) >= 4:
    for i, (qk, ak) in enumerate(faq_pairs):
        m = faq_a_matches[i]
        old_a = m.group(0)
        new_a = f'<div class="faq-a"><p data-i18n="faq.{ak}">{m.group(1)}</p></div>'
        body_content = body_content.replace(old_a, new_a)

# ── Hero title with data-i18n ──
# Already partially handled by build script, let's handle the buttons too
hero_btns_pattern = r'<button class="btn-gold" onclick="[^"]+">[^<]+</button>'
for m in re.finditer(hero_btns_pattern, body_content):
    btn = m.group(0)
    if '立即解密' in btn or 'Start Reading' in btn:
        new_btn = btn.replace('>', ' data-i18n="hero.btn.primary">', 1)
        body_content = body_content.replace(btn, new_btn)
    elif '了解服务' in btn or 'Learn More' in btn:
        new_btn = btn.replace('>', ' data-i18n="hero.btn.secondary">', 1)
        body_content = body_content.replace(btn, new_btn)

# ── Pricing features ──
pricing_feats = [
    ('<li><span class="check">&#x2713;</span> 十二宫详细解读</li>', 'pricing.feat1'),
    ('<li><span class="check">&#x2713;</span> 命盘格局分析</li>', 'pricing.feat2'),
    ('<li><span class="check">&#x2713;</span> 大限运势推演</li>', 'pricing.feat3'),
    ('<li><span class="check">&#x2713;</span> 四化飞星详解</li>', 'pricing.feat4'),
    ('<li><span class="check">&#x2713;</span> 综合运势建议</li>', 'pricing.feat5'),
]
for old_feat, key in pricing_feats:
    if old_feat in body_content:
        body_content = body_content.replace(old_feat, old_feat.replace('<li>', f'<li data-i18n="{key}">'))

# ── Testimonials text, author, role ──
testimonial_keys = ['testimonials.1.text', 'testimonials.1.author', 'testimonials.1.role',
                    'testimonials.2.text', 'testimonials.2.author', 'testimonials.2.role',
                    'testimonials.3.text', 'testimonials.3.author', 'testimonials.3.role']
testimonial_old_new = []
for tk in testimonial_keys:
    # Find the corresponding Chinese text
    with open('index.html', 'r', encoding='utf-8') as f:
        pass  # We'll hardcode the mappings

# Actually, let's use regex to find testimonial divs and add data-i18n
# Find all testimonial-text divs
tt_pattern = r'<div class="testimonial-text">([^<]+)</div>'
for i, m in enumerate(re.finditer(tt_pattern, body_content)):
    key = f'testimonials.{i+1}.text'
    old = m.group(0)
    new = f'<div class="testimonial-text" data-i18n="{key}">{m.group(1)}</div>'
    body_content = body_content.replace(old, new)

# Find all testimonial-author divs
ta_pattern = r'<div class="testimonial-author">([^<]+)</div>'
for i, m in enumerate(re.finditer(ta_pattern, body_content)):
    key = f'testimonials.{i+1}.author'
    old = m.group(0)
    new = f'<div class="testimonial-author" data-i18n="{key}">{m.group(1)}</div>'
    body_content = body_content.replace(old, new)

# Find all testimonial-role divs
tr_pattern = r'<div class="testimonial-role">([^<]+)</div>'
for i, m in enumerate(re.finditer(tr_pattern, body_content)):
    key = f'testimonials.{i+1}.role'
    old = m.group(0)
    new = f'<div class="testimonial-role" data-i18n="{key}">{m.group(1)}</div>'
    body_content = body_content.replace(old, new)

# ── Footer nav links ──
footer_links = [
    ('<a href="#home">首页</a>', 'footer.home'),
    ('<a href="#features">服务分类</a>', 'footer.services'),
    ('<a href="#form">在线排盘</a>', 'footer.chart'),
    ('<a href="#pricing">定价</a>', 'footer.pricing'),
    ('<a href="#faq">常见问题</a>', 'footer.faq'),
]
for old_link, key in footer_links:
    if old_link in body_content:
        body_content = body_content.replace(old_link, old_link.replace('<a ', f'<a data-i18n="{key}" '))

# ── Pricing CTA button ──
pricing_cta_old = '<button class="btn-gold" onclick="document.getElementById(\'form\').scrollIntoView({behavior:\'smooth\'})">&#x1F52E; 立即开始</button>'
pricing_cta_new = '<button class="btn-gold" onclick="document.getElementById(\'form\').scrollIntoView({behavior:\'smooth\'})" data-i18n="pricing.cta">&#x1F52E; 立即开始</button>'
# This appears twice (pricing + CTA section)
body_content = body_content.replace(pricing_cta_old, pricing_cta_new)

# CTA button (second occurrence)
cta_btn_old = '<button class="btn-gold" onclick="document.getElementById(\'form\').scrollIntoView({behavior:\'smooth\'})">&#x1F52E; 立即开始</button>'
cta_btn_new = '<button class="btn-gold" onclick="document.getElementById(\'form\').scrollIntoView({behavior:\'smooth\'})" data-i18n="cta.btn">&#x1F52E; 立即开始</button>'
body_content = body_content.replace(cta_btn_old, cta_btn_new)

# ── Footer bottom ──
import html as html_mod
footer_bottom_matches = list(re.finditer(r'<div class="footer-bottom">([^<]+)</div>', body_content))
if footer_bottom_matches:
    m = footer_bottom_matches[0]
    old = m.group(0)
    new = f'<div class="footer-bottom" data-i18n="footer.bottom">{html_mod.unescape(m.group(1))}</div>'
    body_content = body_content.replace(old, new)

# ── Hero badge ──
# Find the hero badge with emoji
hero_badge_pattern = r'<div class="hero-badge">[^<]+</div>'
for m in re.finditer(hero_badge_pattern, body_content):
    old = m.group(0)
    if 'data-i18n' not in old:
        new = old.replace('>', ' data-i18n="hero.badge">', 1)
        body_content = body_content.replace(old, new)

# ── Rebuild HTML ──
new_html = prefix + body_content + suffix

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# Count data-i18n attributes
attrs = re.findall(r'data-i18n=\"([^\"]+)\"', new_html)
print(f"\nTotal data-i18n attributes: {len(attrs)}")
print(f"Unique keys: {len(set(attrs))}")
print(f"Final file size: {len(new_html)} bytes")
