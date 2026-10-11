#!/usr/bin/env python3
"""Build internationalized index.html with zh/en/ar support."""
import re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove any existing I18N script block (from previous runs)
i18n_start_marker = '<script id="i18n-data">'
i18n_end_marker = '</script>'
existing_i18n_start = html.find(i18n_start_marker)
if existing_i18n_start > 0:
    existing_i18n_end = html.find(i18n_end_marker, existing_i18n_start) + len(i18n_end_marker)
    html = html[:existing_i18n_start] + html[existing_i18n_end:]
    print('Removed existing I18N block')

# ── TRANSLATION DATA ──────────────────────────────────────────
# Keys: semantic identifiers. Values: {zh, en, ar}
# Star/palace/branch names remain in Chinese (proper nouns)

T = {}  # will hold all translations

# ─ Site meta ─
T['site.title'] = {
    'zh': '紫微斗数 - 命理分析',
    'en': 'Zi Wei Dou Shu - Destiny Analysis',
    'ar': 'زي وي دو شو - تحليل المصير'
}

# ─ Header ─
T['header.nav.services'] = {'zh': '服务分类', 'en': 'Services', 'ar': 'الخدمات'}
T['header.nav.how'] = {'zh': '如何使用', 'en': 'How It Works', 'ar': 'كيف يعمل'}
T['header.nav.chart'] = {'zh': '在线排盘', 'en': 'Free Chart', 'ar': 'رسم بياني مجاني'}
T['header.nav.pricing'] = {'zh': '定价', 'en': 'Pricing', 'ar': 'الأسعار'}
T['header.nav.faq'] = {'zh': '常见问题', 'en': 'FAQ', 'ar': 'الأسئلة الشائعة'}
T['header.cta'] = {'zh': '立即解密', 'en': 'Get Started', 'ar': 'ابدأ الآن'}

# ─ Hero ─
T['hero.badge'] = {'zh': '⭐ 紫微斗数 · 专业解密 · 隐私保护', 'en': '⭐ Zi Wei Dou Shu · Professional Reading · Privacy Protected', 'ar': '⭐ زي وي دو شو · قراءة احترافية · حماية الخصوصية'}
T['hero.title.line1'] = {'zh': '用千年智慧，', 'en': 'Unlock Your', 'ar': 'اكتشف'}
T['hero.title.line2'] = {'zh': '解密你的', 'en': 'Destiny with', 'ar': 'مصيرك من خلال'}
T['hero.title.gold'] = {'zh': '人生运势', 'en': 'Ancient Wisdom', 'ar': 'الحكمة القديمة'}
T['hero.sub.line1'] = {'zh': '基于传统紫微斗数算法，精准排盘，十二宫详解', 'en': 'Traditional Zi Wei Dou Shu algorithm, precise chart calculation, 12 palaces analysis', 'ar': 'خوارزمية زي وي دو شو التقليدية ، حساب دقيق للرسم البياني ، تحليل 12 قصرًا'}
T['hero.sub.line2'] = {'zh': '命盘格局 · 大限运势 · 四化飞星 · 综合解读', 'en': 'Chart Patterns · Major Cycles · Four Transformations · Full Reading', 'ar': 'أنماط الرسم البياني · الدورات الكبرى · التحولات الأربعة · قراءة كاملة'}
T['hero.btn.primary'] = {'zh': '🔮 立即解密', 'en': '🔮 Start Reading', 'ar': '🔮 ابدأ القراءة'}
T['hero.btn.secondary'] = {'zh': '了解服务', 'en': 'Learn More', 'ar': 'اعرف المزيد'}

# ─ Features Section ─
T['features.label'] = {'zh': '服务分类', 'en': 'Our Services', 'ar': 'خدماتنا'}
T['features.title'] = {'zh': '全方位命运解读', 'en': 'Comprehensive Destiny Analysis', 'ar': 'تحليل شامل للمصير'}
T['features.desc'] = {'zh': '从事业财运到感情健康，紫微斗数为你揭示人生的各个面向', 'en': 'From career and wealth to love and health, Zi Wei Dou Shu reveals every aspect of your life', 'ar': 'من المهنة والثروة إلى الحب والصحة ، يكشف زي وي دو شو كل جانب من جوانب حياتك'}

T['features.career.name'] = {'zh': '事业运', 'en': 'Career Fortune', 'ar': 'حظ المهنة'}
T['features.career.desc'] = {'zh': '事业宫解读职业发展方向，分析官禄运、贵人运，助你做出正确职涯决策', 'en': 'Career palace analysis reveals professional direction, promotion timing, and benefactor guidance', 'ar': 'يكشف تحليل قصر المهنة عن الاتجاه المهني وتوقيت الترقية وتوجيه المحسنين'}
T['features.love.name'] = {'zh': '感情运', 'en': 'Love Fortune', 'ar': 'حظ الحب'}
T['features.love.desc'] = {'zh': '夫妻宫详解桃花姻缘，了解感情模式，把握良缘时机', 'en': 'Spouse palace reveals romantic patterns, marriage quality, and the right timing for love', 'ar': 'يكشف قصر الزوج عن الأنماط الرومانسية وجودة الزواج والتوقيت المناسب للحب'}
T['features.wealth.name'] = {'zh': '财运', 'en': 'Wealth Fortune', 'ar': 'حظ الثروة'}
T['features.wealth.desc'] = {'zh': '财帛宫分析求财方式，识财运旺衰，掌财富密码', 'en': 'Wealth palace analyzes income sources, investment timing, and financial prosperity cycles', 'ar': 'يحلل قصر الثروة مصادر الدخل وتوقيت الاستثمار ودورات الازدهار المالي'}
T['features.health.name'] = {'zh': '健康运', 'en': 'Health Fortune', 'ar': 'حظ الصحة'}
T['features.health.desc'] = {'zh': '疾厄宫分析身体健康状况，预防潜在疾病风险，掌握养生调护之道', 'en': 'Health palace reveals physical constitution, potential risks, and wellness guidance', 'ar': 'يكشف قصر الصحة عن التكوين الجسدي والمخاطر المحتملة وإرشادات العافية'}
T['features.cta'] = {'zh': '点击了解详情 →', 'en': 'Click for details →', 'ar': 'انقر للتفاصيل ←'}

# ─ How It Works ─
T['how.label'] = {'zh': '如何使用', 'en': 'How It Works', 'ar': 'كيف يعمل'}
T['how.title'] = {'zh': '三步揭秘你的命运密码', 'en': 'Three Steps to Reveal Your Destiny', 'ar': 'ثلاث خطوات لكشف مصيرك'}
T['how.desc'] = {'zh': '简单三步，获取专业级紫微斗数命盘解读', 'en': 'Three simple steps to get a professional Zi Wei Dou Shu reading', 'ar': 'ثلاث خطوات بسيطة للحصول على قراءة احترافية'}

T['how.step1.title'] = {'zh': '输入出生信息', 'en': 'Enter Birth Info', 'ar': 'أدخل معلومات الميلاد'}
T['how.step1.desc'] = {'zh': '填写你的出生年月日时和性别，支持公历和农历两种日期输入方式', 'en': 'Enter your birth date, time, and gender. Supports both solar and lunar calendar input', 'ar': 'أدخل تاريخ ميلادك ووقتك وجنسك. يدعم التقويم الشمسي والقمري'}
T['how.step2.title'] = {'zh': '智能排盘', 'en': 'Auto Chart Calculation', 'ar': 'حساب الرسم البياني تلقائيًا'}
T['how.step2.desc'] = {'zh': '系统自动计算十二宫星曜分布、四化飞星、大限运势，生成专业命盘', 'en': 'System auto-calculates 12 palaces star distribution, Four Transformations, and major cycle fortune', 'ar': 'يحسب النظام تلقائيًا توزيع نجوم القصور الـ 12 والتحولات الأربعة وثروة الدورة الكبرى'}
T['how.step3.title'] = {'zh': '详细解盘', 'en': 'Detailed Reading', 'ar': 'قراءة مفصلة'}
T['how.step3.desc'] = {'zh': '获取十二宫详细解读、命盘格局分析、大限运势推演，全面了解人生运势', 'en': 'Get detailed 12 palace interpretation, pattern analysis, and major cycle projection for a complete life reading', 'ar': 'احصل على تفسير مفصل للقصور الـ 12 وتحليل الأنماط وتوقعات الدورة الكبرى لقراءة حياة كاملة'}

# ─ Form ─
T['form.label'] = {'zh': '在线排盘', 'en': 'Free Chart', 'ar': 'رسم بياني مجاني'}
T['form.title'] = {'zh': '填入你的出生信息', 'en': 'Enter Your Birth Information', 'ar': 'أدخل معلومات ميلادك'}
T['form.desc'] = {'zh': '准确填写出生资料，即可免费查看紫微斗数命盘', 'en': 'Enter your birth details accurately to view your free Zi Wei Dou Shu chart', 'ar': 'أدخل تفاصيل ميلادك بدقة لعرض الرسم البياني المجاني'}
T['form.name.label'] = {'zh': '姓名（选填）', 'en': 'Name (optional)', 'ar': 'الاسم (اختياري)'}
T['form.name.placeholder'] = {'zh': '请输入您的姓名', 'en': 'Enter your name', 'ar': 'أدخل اسمك'}
T['form.gender.label'] = {'zh': '性别', 'en': 'Gender', 'ar': 'الجنس'}
T['form.gender.male'] = {'zh': '👨 男', 'en': '👨 Male', 'ar': '👨 ذكر'}
T['form.gender.female'] = {'zh': '👩 女', 'en': '👩 Female', 'ar': '👩 أنثى'}
T['form.date.label'] = {'zh': '出生日期', 'en': 'Birth Date', 'ar': 'تاريخ الميلاد'}
T['form.date.solar'] = {'zh': '☀️ 公历', 'en': '☀️ Solar', 'ar': '☀️ شمسي'}
T['form.date.lunar'] = {'zh': '🌙 农历', 'en': '🌙 Lunar', 'ar': '🌙 قمري'}
T['form.hour.label'] = {'zh': '出生时辰', 'en': 'Birth Hour', 'ar': 'ساعة الميلاد'}
T['form.submit'] = {'zh': '开始排盘', 'en': 'Generate Chart', 'ar': 'إنشاء الرسم البياني'}
T['form.note'] = {'zh': '命理分析仅供参考 · 命运由自己掌握', 'en': 'For reference only · You control your own destiny', 'ar': 'للمرجعية فقط · أنت تتحكم في مصيرك'}

# ─ Hour options ─
HOUR_NAMES_ZH = ['子时 (23:00-01:00)','丑时 (01:00-03:00)','寅时 (03:00-05:00)','卯时 (05:00-07:00)','辰时 (07:00-09:00)','巳时 (09:00-11:00)','午时 (11:00-13:00)','未时 (13:00-15:00)','申时 (15:00-17:00)','酉时 (17:00-19:00)','戌时 (19:00-21:00)','亥时 (21:00-23:00)']
HOUR_NAMES_EN = ['Zi (23:00-01:00)','Chou (01:00-03:00)','Yin (03:00-05:00)','Mao (05:00-07:00)','Chen (07:00-09:00)','Si (09:00-11:00)','Wu (11:00-13:00)','Wei (13:00-15:00)','Shen (15:00-17:00)','You (17:00-19:00)','Xu (19:00-21:00)','Hai (21:00-23:00)']
HOUR_NAMES_AR = ['زي (23:00-01:00)','تشو (01:00-03:00)','ين (03:00-05:00)','ماو (05:00-07:00)','تشن (07:00-09:00)','سي (09:00-11:00)','وو (11:00-13:00)','وي (13:00-15:00)','شن (15:00-17:00)','يو (17:00-19:00)','شو (19:00-21:00)','هاي (21:00-23:00)']

# ─ Chart Result ─
T['result.label'] = {'zh': '排盘结果', 'en': 'Chart Result', 'ar': 'نتيجة الرسم البياني'}
T['result.title'] = {'zh': '你的紫微斗数命盘', 'en': 'Your Zi Wei Dou Shu Chart', 'ar': 'رسم زي وي دو شو الخاص بك'}

# ─ Testimonials ─
T['testimonials.label'] = {'zh': '用户评价', 'en': 'Testimonials', 'ar': 'التوصيات'}
T['testimonials.title'] = {'zh': '他们都在用紫微斗数解密人生', 'en': 'They All Use Zi Wei Dou Shu to Decode Life', 'ar': 'جميعهم يستخدمون زي وي دو شو لفك شيفرة الحياة'}
T['testimonials.1.text'] = {'zh': '排盘结果非常详细，十二宫的解读让我对自己有了全新的认识。特别是事业宫的解读，和我的实际情况非常吻合。', 'en': 'The chart result was very detailed. The 12 palace interpretation gave me a whole new understanding of myself. The career palace reading especially matched my actual situation.', 'ar': 'كانت نتيجة الرسم البياني مفصلة للغاية. أعطاني تفسير القصور الـ 12 فهمًا جديدًا تمامًا لنفسي. تطابقت قراءة قصر المهنة بشكل خاص مع وضعي الفعلي.'}
T['testimonials.1.author'] = {'zh': '李先生', 'en': 'Mr. Li', 'ar': 'السيد لي'}
T['testimonials.1.role'] = {'zh': '互联网从业者', 'en': 'Internet Professional', 'ar': 'محترف إنترنت'}
T['testimonials.2.text'] = {'zh': '夫妻宫的解读让我对感情有了更清晰的认识。化忌的地方也确实是我需要努力的方向。非常专业的解析！', 'en': 'The spouse palace reading gave me clearer insight into my relationships. The Hua Ji areas are exactly where I need to work on. Very professional analysis!', 'ar': 'أعطتني قراءة قصر الزوج نظرة أوضح على علاقاتي. مناطق هوا جي هي بالضبط حيث أحتاج إلى العمل. تحليل احترافي للغاية!'}
T['testimonials.2.author'] = {'zh': '王女士', 'en': 'Ms. Wang', 'ar': 'السيدة وانغ'}
T['testimonials.2.role'] = {'zh': '教师', 'en': 'Teacher', 'ar': 'معلمة'}
T['testimonials.3.text'] = {'zh': '大限运势的推算让我对未来的规划有了方向。格局分析准确度很高，推荐给需要的朋友。', 'en': 'The major cycle projection gave me direction for future planning. The pattern analysis was highly accurate. I recommend it to friends who need it.', 'ar': 'أعطتني توقعات الدورة الكبرى اتجاهًا للتخطيط المستقبلي. كان تحليل الأنماط دقيقًا للغاية. أوصي به للأصدقاء الذين يحتاجون إليه.'}
T['testimonials.3.author'] = {'zh': '张先生', 'en': 'Mr. Zhang', 'ar': 'السيد تشانغ'}
T['testimonials.3.role'] = {'zh': '创业者', 'en': 'Entrepreneur', 'ar': 'رائد أعمال'}

T['stats.users'] = {'zh': '已服务用户', 'en': 'Users Served', 'ar': 'مستخدم تمت خدمتهم'}
T['stats.rating'] = {'zh': '好评率', 'en': 'Satisfaction Rate', 'ar': 'معدل الرضا'}
T['stats.privacy'] = {'zh': '隐私保护', 'en': 'Privacy Protected', 'ar': 'حماية الخصوصية'}

# ─ Pricing ─
T['pricing.label'] = {'zh': '定价', 'en': 'Pricing', 'ar': 'الأسعار'}
T['pricing.title'] = {'zh': '选择适合你的方案', 'en': 'Choose Your Plan', 'ar': 'اختر خطتك'}
T['pricing.badge'] = {'zh': '🌟 最受欢迎', 'en': '🌟 Most Popular', 'ar': '🌟 الأكثر شيوعًا'}
T['pricing.name'] = {'zh': '详细解盘套餐', 'en': 'Detailed Reading Package', 'ar': 'حزمة القراءة المفصلة'}
T['pricing.period'] = {'zh': '一次性付费 · 永久查看', 'en': 'One-time payment · Lifetime access', 'ar': 'دفعة واحدة · وصول مدى الحياة'}
T['pricing.feat1'] = {'zh': '十二宫详细解读', 'en': '12 Palaces Detailed Reading', 'ar': 'قراءة مفصلة للقصور الـ 12'}
T['pricing.feat2'] = {'zh': '命盘格局分析', 'en': 'Chart Pattern Analysis', 'ar': 'تحليل أنماط الرسم البياني'}
T['pricing.feat3'] = {'zh': '大限运势推演', 'en': 'Major Cycle Projection', 'ar': 'توقعات الدورة الكبرى'}
T['pricing.feat4'] = {'zh': '四化飞星详解', 'en': 'Four Transformations Explained', 'ar': 'شرح التحولات الأربعة'}
T['pricing.feat5'] = {'zh': '综合运势建议', 'en': 'Comprehensive Life Guidance', 'ar': 'إرشادات حياة شاملة'}
T['pricing.cta'] = {'zh': '🔮 立即开始', 'en': '🔮 Start Now', 'ar': '🔮 ابدأ الآن'}

# ─ FAQ ─
T['faq.label'] = {'zh': '常见问题', 'en': 'FAQ', 'ar': 'الأسئلة الشائعة'}
T['faq.title'] = {'zh': '有任何疑问？我们为你解答', 'en': 'Questions? We Have Answers', 'ar': 'أسئلة؟ لدينا إجابات'}
T['faq.q1'] = {'zh': '紫微斗数是什么？', 'en': 'What is Zi Wei Dou Shu?', 'ar': 'ما هو زي وي دو شو؟'}
T['faq.a1'] = {'zh': '紫微斗数是中国传统命理学的重要分支，起源于宋代，通过出生年月日时推算十二宫星曜分布，分析人生各个方面的运势和发展趋势。与八字并称为中国传统命理学的两大体系。', 'en': 'Zi Wei Dou Shu is an important branch of traditional Chinese destiny analysis, originating from the Song Dynasty. It calculates the distribution of stars across 12 palaces based on birth date and time, analyzing all aspects of life fortune and development trends.', 'ar': 'زي وي دو شو هو فرع مهم من تحليل المصير الصيني التقليدي ، نشأ من عهد أسرة سونغ. يحسب توزيع النجوم عبر 12 قصرًا بناءً على تاريخ ووقت الميلاد ، ويحلل جميع جوانب ثروة الحياة واتجاهات التطور.'}
T['faq.q2'] = {'zh': '排盘结果准确吗？', 'en': 'How accurate are the results?', 'ar': 'ما مدى دقة النتائج؟'}
T['faq.a2'] = {'zh': '我们使用传统紫微斗数算法，严格按照古法计算星曜分布和四化飞星。但请注意，命理分析仅供参考，人生的走向更多取决于自己的选择和努力。', 'en': 'We use traditional Zi Wei Dou Shu algorithms following ancient calculation methods. However, please note that destiny analysis is for reference only — your life path depends more on your own choices and efforts.', 'ar': 'نستخدم خوارزميات زي وي دو شو التقليدية باتباع طرق الحساب القديمة. ومع ذلك ، يرجى ملاحظة أن تحليل المصير هو للمرجعية فقط - مسار حياتك يعتمد أكثر على اختياراتك وجهودك.'}
T['faq.q3'] = {'zh': '如何保证我的隐私安全？', 'en': 'How is my privacy protected?', 'ar': 'كيف تتم حماية خصوصيتي؟'}
T['faq.a3'] = {'zh': '所有出生信息仅用于排盘计算，我们不会存储或分享你的个人数据。支付通过 Stripe 安全处理，我们不接触你的支付信息。', 'en': 'All birth information is used only for chart calculation. We do not store or share your personal data. Payments are securely processed through Stripe — we never access your payment information.', 'ar': 'تُستخدم جميع معلومات الميلاد فقط لحساب الرسم البياني. لا نخزن أو نشارك بياناتك الشخصية. تتم معالجة المدفوعات بشكل آمن من خلال Stripe - لا نصل أبدًا إلى معلومات الدفع الخاصة بك.'}
T['faq.q4'] = {'zh': '支持哪些支付方式？', 'en': 'What payment methods are supported?', 'ar': 'ما هي طرق الدفع المدعومة؟'}
T['faq.a4'] = {'zh': '我们通过 Stripe 接受全球主流信用卡和借记卡支付（Visa、Mastercard、American Express 等），安全便捷。', 'en': 'We accept major global credit and debit cards through Stripe (Visa, Mastercard, American Express, etc.) — safe and convenient.', 'ar': 'نقبل بطاقات الائتمان والخصم العالمية الرئيسية من خلال Stripe (فيزا وماستركارد وأمريكان إكسبريس وغيرها) - آمنة ومريحة.'}

# ─ CTA ─
T['cta.title'] = {'zh': '准备好解密你的人生运势了吗？', 'en': 'Ready to Unlock Your Destiny?', 'ar': 'هل أنت مستعد لاكتشاف مصيرك؟'}
T['cta.desc'] = {'zh': '输入出生信息，即刻获取你的专属紫微斗数命盘解读', 'en': 'Enter your birth info and get your personalized Zi Wei Dou Shu reading instantly', 'ar': 'أدخل معلومات ميلادك واحصل على قراءة زي وي دو شو المخصصة لك فورًا'}
T['cta.btn'] = {'zh': '🔮 立即开始', 'en': '🔮 Start Now', 'ar': '🔮 ابدأ الآن'}

# ─ Footer ─
T['footer.brand'] = {'zh': '☾ yourfate.xyz', 'en': '☾ yourfate.xyz', 'ar': '☾ yourfate.xyz'}
T['footer.desc'] = {'zh': '紫微斗数在线命理解密服务平台', 'en': 'Zi Wei Dou Shu Online Destiny Reading Platform', 'ar': 'منصة زي وي دو شو لقراءة المصير عبر الإنترنت'}
T['footer.home'] = {'zh': '首页', 'en': 'Home', 'ar': 'الرئيسية'}
T['footer.services'] = {'zh': '服务分类', 'en': 'Services', 'ar': 'الخدمات'}
T['footer.chart'] = {'zh': '在线排盘', 'en': 'Free Chart', 'ar': 'رسم بياني مجاني'}
T['footer.pricing'] = {'zh': '定价', 'en': 'Pricing', 'ar': 'الأسعار'}
T['footer.faq'] = {'zh': '常见问题', 'en': 'FAQ', 'ar': 'الأسئلة الشائعة'}
T['footer.bottom'] = {'zh': '© 2026 yourfate.xyz · 命理分析仅供参考 · 命运由自己掌握', 'en': '© 2026 yourfate.xyz · For reference only · You control your own destiny', 'ar': '© 2026 yourfate.xyz · للمرجعية فقط · أنت تتحكم في مصيرك'}

# ─ Modal defaults ─
T['modal.ok'] = {'zh': '知道了', 'en': 'OK', 'ar': 'موافق'}
T['modal.cancel'] = {'zh': '暂不需要', 'en': 'Not Now', 'ar': 'ليس الآن'}

# ─ JS dynamic text ─
T['chart.element_label'] = {'zh': '五行局', 'en': 'Element', 'ar': 'العنصر'}
T['chart.shen_tag'] = {'zh': '身', 'en': 'Body', 'ar': 'جسم'}
T['chart.male'] = {'zh': '男', 'en': 'M', 'ar': 'ذكر'}
T['chart.female'] = {'zh': '女', 'en': 'F', 'ar': 'أنثى'}
T['chart.year_prefix'] = {'zh': '年 ', 'en': 'Yr ', 'ar': 'سنة '}
T['chart.month_prefix'] = {'zh': '月 ', 'en': 'Mo ', 'ar': 'شهر '}
T['chart.day_prefix'] = {'zh': '日 ', 'en': 'Day ', 'ar': 'يوم '}
T['chart.hour_prefix'] = {'zh': '时 ', 'en': 'Hr ', 'ar': 'ساعة '}
T['chart.year_suffix'] = {'zh': '年', 'en': '', 'ar': ''}
T['chart.sihua_label'] = {'zh': '四化：', 'en': '4 Transformations: ', 'ar': 'التحولات الأربعة: '}
T['chart.hualu_suffix'] = {'zh': '化禄', 'en': ' Hua Lu', 'ar': ' هوا لو'}
T['chart.huaquan_suffix'] = {'zh': '化权', 'en': ' Hua Quan', 'ar': ' هوا تشوان'}
T['chart.huake_suffix'] = {'zh': '化科', 'en': ' Hua Ke', 'ar': ' هوا كه'}
T['chart.huaji_suffix'] = {'zh': '化忌', 'en': ' Hua Ji', 'ar': ' هوا جي'}
T['chart.daxian_title'] = {'zh': '大限', 'en': 'Major Cycles', 'ar': 'الدورات الكبرى'}
T['chart.btn_detail'] = {'zh': '查看详细解盘', 'en': 'View Detailed Reading', 'ar': 'عرض القراءة المفصلة'}
T['chart.btn_reset'] = {'zh': '重新输入', 'en': 'Reset', 'ar': 'إعادة تعيين'}
T['chart.no_stars'] = {'zh': '无主星', 'en': 'No main star', 'ar': 'لا نجم رئيسي'}
T['chart.unknown_name'] = {'zh': '未知', 'en': 'Unknown', 'ar': 'غير معروف'}
T['chart.calculating'] = {'zh': '计算中...', 'en': 'Calculating...', 'ar': 'جارٍ الحساب...'}
T['chart.age_suffix'] = {'zh': '岁', 'en': '', 'ar': ''}

# ─ Detail view ─
T['detail.title_suffix'] = {'zh': '的命盘解读', 'en': "'s Chart Reading", 'ar': ' قراءة الرسم البياني'}
T['detail.year_sep'] = {'zh': '年 · ', 'en': ' · ', 'ar': ' · '}
T['detail.ming_in'] = {'zh': '命宫在', 'en': 'Ming Palace in ', 'ar': 'قصر مينغ في '}
T['detail.shen_in'] = {'zh': ' · 身宫在', 'en': ' · Shen Palace in ', 'ar': ' · قصر شن في '}
T['detail.palace_suffix'] = {'zh': '宫', 'en': '', 'ar': ''}
T['detail.element_prefix'] = {'zh': '五行', 'en': 'Element: ', 'ar': 'العنصر: '}
T['detail.daxian_every'] = {'zh': ' · 大限每', 'en': ' · Cycle every ', 'ar': ' · دورة كل '}
T['detail.years_per'] = {'zh': '年一运', 'en': ' years', 'ar': ' سنوات'}
T['detail.forward'] = {'zh': '阳男顺行', 'en': 'Yang Male Forward', 'ar': 'يانغ ذكر أمامي'}
T['detail.reverse'] = {'zh': '阴男逆行', 'en': 'Yin Male Reverse', 'ar': 'ين ذكر عكسي'}
T['detail.sihua_title'] = {'zh': '四化飞星', 'en': 'Four Transformations', 'ar': 'التحولات الأربعة'}
T['detail.hualu'] = {'zh': '化禄', 'en': 'Hua Lu', 'ar': 'هوا لو'}
T['detail.hualu_desc'] = {'zh': '财禄顺利', 'en': 'Wealth & Prosperity', 'ar': 'الثروة والازدهار'}
T['detail.huaquan'] = {'zh': '化权', 'en': 'Hua Quan', 'ar': 'هوا تشوان'}
T['detail.huaquan_desc'] = {'zh': '掌权增强', 'en': 'Power & Authority', 'ar': 'القوة والسلطة'}
T['detail.huake'] = {'zh': '化科', 'en': 'Hua Ke', 'ar': 'هوا كه'}
T['detail.huake_desc'] = {'zh': '文名声誉', 'en': 'Fame & Reputation', 'ar': 'الشهرة والسمعة'}
T['detail.huaji'] = {'zh': '化忌', 'en': 'Hua Ji', 'ar': 'هوا جي'}
T['detail.huaji_desc'] = {'zh': '困扰阻碍', 'en': 'Obstacles & Challenges', 'ar': 'العقبات والتحديات'}
T['detail.patterns_title'] = {'zh': '命盘格局', 'en': 'Chart Patterns', 'ar': 'أنماط الرسم البياني'}
T['detail.palaces_title'] = {'zh': '十二宫详解', 'en': '12 Palaces Detailed', 'ar': 'تفصيل القصور الـ 12'}
T['detail.daxian_title'] = {'zh': '大限运势', 'en': 'Major Cycle Fortune', 'ar': 'ثروة الدورة الكبرى'}
T['detail.summary_title'] = {'zh': '四化总结', 'en': 'Transformation Summary', 'ar': 'ملخص التحولات'}
T['detail.advice_title'] = {'zh': '温馨提示', 'en': 'A Gentle Reminder', 'ar': 'تذكير لطيف'}
T['detail.btn_back'] = {'zh': '返回命盘', 'en': 'Back to Chart', 'ar': 'العودة إلى الرسم البياني'}
T['detail.sihua_prefix'] = {'zh': '四化：', 'en': '4 Hua: ', 'ar': 'التحولات الأربعة: '}

# ─ Payment modal ─
T['pay.title'] = {'zh': '解锁详细解盘', 'en': 'Unlock Detailed Reading', 'ar': 'فتح القراءة المفصلة'}
T['pay.body.intro'] = {'zh': '🔮 完整命盘解读内容：', 'en': '🔮 Complete Chart Reading Includes:', 'ar': '🔮 تشمل قراءة الرسم البياني الكاملة:'}
T['pay.body.item1'] = {'zh': '✦ 十二宫详细解读', 'en': '✦ 12 Palaces Detailed Reading', 'ar': '✦ قراءة مفصلة للقصور الـ 12'}
T['pay.body.item2'] = {'zh': '✦ 命盘格局分析', 'en': '✦ Chart Pattern Analysis', 'ar': '✦ تحليل أنماط الرسم البياني'}
T['pay.body.item3'] = {'zh': '✦ 大限运势解读', 'en': '✦ Major Cycle Reading', 'ar': '✦ قراءة الدورة الكبرى'}
T['pay.body.item4'] = {'zh': '✦ 四化飞星详解', 'en': '✦ Four Transformations Explained', 'ar': '✦ شرح التحولات الأربعة'}
T['pay.body.item5'] = {'zh': '✦ 综合运势建议', 'en': '✦ Comprehensive Life Guidance', 'ar': '✦ إرشادات حياة شاملة'}
T['pay.body.price'] = {'zh': '一次性付费 ', 'en': 'One-time payment: ', 'ar': 'دفعة واحدة: '}
T['pay.body.forever'] = {'zh': '付费后永久查看当前命盘解读', 'en': 'Lifetime access to this chart reading after payment', 'ar': 'وصول مدى الحياة لقراءة هذا الرسم البياني بعد الدفع'}
T['pay.btn'] = {'zh': '💳 立即支付 $9.99', 'en': '💳 Pay $9.99 Now', 'ar': '💳 ادفع $9.99 الآن'}
T['pay.btn.stripe'] = {'zh': '💳 信用卡 / 借记卡支付', 'en': '💳 Credit / Debit Card', 'ar': '💳 بطاقة ائتمان / خصم'}
T['pay.btn.lianlian'] = {'zh': '💱 连连跨境支付（支付宝/微信/银联）', 'en': '💱 LianLian Global (Alipay/WeChat/UnionPay)', 'ar': '💱 ليان ليان العالمية (Alipay/WeChat/UnionPay)'}
T['pay.redirecting'] = {'zh': '正在跳转支付...', 'en': 'Redirecting to payment...', 'ar': 'جارٍ التحويل إلى الدفع...'}

# ─ Toast messages ─
T['toast.select_date'] = {'zh': '请选择出生日期', 'en': 'Please select your birth date', 'ar': 'يرجى اختيار تاريخ ميلادك'}
T['toast.year_range'] = {'zh': '仅支持1900-2100年范围', 'en': 'Only years 1900-2100 supported', 'ar': 'فقط السنوات 1900-2100 مدعومة'}
T['toast.calc_failed'] = {'zh': '排盘失败，请检查日期', 'en': 'Chart calculation failed. Please check date', 'ar': 'فشل حساب الرسم البياني. يرجى التحقق من التاريخ'}
T['toast.info_missing'] = {'zh': '信息缺失，请重新排盘', 'en': 'Information missing. Please regenerate chart', 'ar': 'المعلومات مفقودة. يرجى إعادة إنشاء الرسم البياني'}
T['toast.stripe_config'] = {'zh': '支付服务暂时不可用\n请确认已配置 Stripe 密钥后重试', 'en': 'Payment service unavailable\nPlease configure Stripe keys and retry', 'ar': 'خدمة الدفع غير متاحة\nيرجى تكوين مفاتيح Stripe وإعادة المحاولة'}
T['toast.lianlian_config'] = {'zh': '连连支付服务暂时不可用\n请确认已配置连连密钥后重试', 'en': 'LianLian payment service unavailable\nPlease configure LianLian keys and retry', 'ar': 'خدمة دفع ليان ليان غير متاحة\nيرجى تكوين مفاتيح ليان ليان وإعادة المحاولة'}
T['toast.network_error'] = {'zh': '网络错误，请重试', 'en': 'Network error. Please try again', 'ar': 'خطأ في الشبكة. يرجى المحاولة مرة أخرى'}
T['toast.data_missing'] = {'zh': '读取信息失败，请重新输入出生信息', 'en': 'Failed to load info. Please re-enter birth details', 'ar': 'فشل تحميل المعلومات. يرجى إعادة إدخال تفاصيل الميلاد'}
T['toast.pay_success'] = {'zh': '支付成功！正在展示详细解盘...', 'en': 'Payment successful! Loading detailed reading...', 'ar': 'تم الدفع بنجاح! جارٍ تحميل القراءة المفصلة...'}
T['toast.data_restore'] = {'zh': '数据恢复失败，请重新输入出生信息', 'en': 'Data recovery failed. Please re-enter birth details', 'ar': 'فشل استعادة البيانات. يرجى إعادة إدخال تفاصيل الميلاد'}
T['toast.verify_fail'] = {'zh': '支付验证失败，请稍后再试或联系客服', 'en': 'Payment verification failed. Please try later or contact support', 'ar': 'فشل التحقق من الدفع. يرجى المحاولة لاحقًا أو الاتصال بالدعم'}
T['toast.verify_network'] = {'zh': '网络错误，无法验证支付状态', 'en': 'Network error. Cannot verify payment status', 'ar': 'خطأ في الشبكة. لا يمكن التحقق من حالة الدفع'}
T['chart.btn_unlocked'] = {'zh': '查看详细解盘 ✓ 已解锁', 'en': 'View Reading ✓ Unlocked', 'ar': 'عرض القراءة ✓ مفتوح'}

# ─ Category modal labels ─
T['cat.analyze_label'] = {'zh': '🔍 分析维度', 'en': '🔍 Analysis Dimensions', 'ar': '🔍 أبعاد التحليل'}
T['cat.service_label'] = {'zh': '📦 服务内容', 'en': '📦 Service Details', 'ar': '📦 تفاصيل الخدمة'}
T['cat.btn_goto'] = {'zh': '立即排盘解锁解读', 'en': 'Generate Chart to Unlock', 'ar': 'إنشاء الرسم البياني للفتح'}
T['cat.btn_close'] = {'zh': '关闭', 'en': 'Close', 'ar': 'إغلاق'}

# ─ Category data translations ─
CAT_KEYS = ['career', 'love', 'wealth', 'health']
CAT_FIELDS = {
    'career': {
        'title': {'zh': '事业运 — 专业解读', 'en': 'Career Fortune — Professional Reading', 'ar': 'حظ المهنة — قراءة احترافية'},
        'intro': {'zh': '通过紫微斗数十二宫中的<strong>官禄宫</strong>（事业宫）为核心，结合命宫、财帛宫、迁移宫，全面分析你的事业发展轨迹。',
                  'en': 'Using the <strong>Career Palace</strong> as the core, combined with Ming Palace, Wealth Palace, and Travel Palace, we comprehensively analyze your career development trajectory.',
                  'ar': 'باستخدام <strong>قصر المهنة</strong> كنواة ، جنبًا إلى جنب مع قصر مينغ وقصر الثروة وقصر السفر ، نحلل مسار تطورك المهني بشكل شامل.'},
        'analyzes': [
            {'zh_l': '命宫主星', 'en_l': 'Ming Palace Star', 'ar_l': 'نجم قصر مينغ', 'zh_d': '天生性格特质，适合的职业类型与工作风格', 'en_d': 'Innate personality traits, suitable career types and work style', 'ar_d': 'سمات الشخصية الفطرية وأنواع المهن المناسبة وأسلوب العمل'},
            {'zh_l': '官禄宫', 'en_l': 'Career Palace', 'ar_l': 'قصر المهنة', 'zh_d': '事业运核心指标 — 职业发展方向、升迁时机、工作环境适配度', 'en_d': 'Core career indicator — professional direction, promotion timing, work environment fit', 'ar_d': 'مؤشر المهنة الأساسي — الاتجاه المهني وتوقيت الترقية وملاءمة بيئة العمل'},
            {'zh_l': '财帛宫', 'en_l': 'Wealth Palace', 'ar_l': 'قصر الثروة', 'zh_d': '收入来源与求财方式，正财偏财运势分析', 'en_d': 'Income sources and wealth acquisition methods, direct and indirect wealth analysis', 'ar_d': 'مصادر الدخل وطرق اكتساب الثروة وتحليل الثروة المباشرة وغير المباشرة'},
            {'zh_l': '迁移宫', 'en_l': 'Travel Palace', 'ar_l': 'قصر السفر', 'zh_d': '外出发展机遇、驿马运、贵人助力与小人防范', 'en_d': 'External development opportunities, travel fortune, benefactor assistance and adversary prevention', 'ar_d': 'فرص التطوير الخارجية وثروة السفر ومساعدة المحسنين والوقاية من الخصوم'},
            {'zh_l': '四化飞星', 'en_l': '4 Transformations', 'ar_l': 'التحولات الأربعة', 'zh_d': '化禄/化权/化科/化忌在事业相关宫位的影响与应对策略', 'en_d': 'Impact of Hua Lu/Hua Quan/Hua Ke/Hua Ji on career-related palaces and strategies', 'ar_d': 'تأثير هوا لو/هوا تشوان/هوا كه/هوا جي على القصور المتعلقة بالمهنة والاستراتيجيات'}
        ],
        'serviceIntro': {'zh': '购买详细解盘后，你将获得：', 'en': 'After purchasing the detailed reading, you will receive:', 'ar': 'بعد شراء القراءة المفصلة ، ستحصل على:'},
        'services': [
            {'zh': '官禄宫星曜组合深度解析', 'en': 'In-depth Career Palace star combination analysis', 'ar': 'تحليل متعمق لتركيبة نجوم قصر المهنة'},
            {'zh': '职业转型与升迁时机建议', 'en': 'Career transition and promotion timing advice', 'ar': 'نصائح حول الانتقال المهني وتوقيت الترقية'},
            {'zh': '贵人与小人识别指引', 'en': 'Benefactor and adversary identification guide', 'ar': 'دليل تحديد المحسنين والخصوم'},
            {'zh': '每十年大限事业运势推演', 'en': '10-year major cycle career fortune projection', 'ar': 'توقعات ثروة المهنة للدورة الكبرى كل 10 سنوات'},
            {'zh': '适合行业与创业时机分析', 'en': 'Suitable industry and entrepreneurship timing analysis', 'ar': 'تحليل الصناعة المناسبة وتوقيت ريادة الأعمال'}
        ]
    },
    'love': {
        'title': {'zh': '感情运 — 专业解读', 'en': 'Love Fortune — Professional Reading', 'ar': 'حظ الحب — قراءة احترافية'},
        'intro': {'zh': '以<strong>夫妻宫</strong>为核心，结合命宫、福德宫、子女宫，深度解读你的感情模式与婚姻缘分。',
                  'en': 'Using the <strong>Spouse Palace</strong> as the core, combined with Ming Palace, Fortune Palace, and Children Palace, we deeply interpret your relationship patterns and marriage destiny.',
                  'ar': 'باستخدام <strong>قصر الزوج</strong> كنواة ، جنبًا إلى جنب مع قصر مينغ وقصر الثروة وقصر الأطفال ، نفسر بعمق أنماط علاقاتك ومصير زواجك.'},
        'analyzes': [
            {'zh_l': '命宫主星', 'en_l': 'Ming Palace Star', 'ar_l': 'نجم قصر مينغ', 'zh_d': '先天感情特质，恋爱风格与择偶偏好', 'en_d': 'Innate romantic traits, love style and partner preferences', 'ar_d': 'السمات الرومانسية الفطرية وأسلوب الحب وتفضيلات الشريك'},
            {'zh_l': '夫妻宫', 'en_l': 'Spouse Palace', 'ar_l': 'قصر الزوج', 'zh_d': '婚姻运核心指标 — 配偶特征、婚姻质量、感情走势', 'en_d': 'Core marriage indicator — spouse characteristics, marriage quality, relationship trends', 'ar_d': 'مؤشر الزواج الأساسي — خصائص الزوج وجودة الزواج واتجاهات العلاقة'},
            {'zh_l': '福德宫', 'en_l': 'Fortune Palace', 'ar_l': 'قصر الثروة', 'zh_d': '内心情感需求、精神契合度、感情幸福感来源', 'en_d': 'Inner emotional needs, spiritual compatibility, sources of relationship happiness', 'ar_d': 'الاحتياجات العاطفية الداخلية والتوافق الروحي ومصادر سعادة العلاقة'},
            {'zh_l': '子女宫', 'en_l': 'Children Palace', 'ar_l': 'قصر الأطفال', 'zh_d': '桃花运旺衰、恋爱机会多寡、子女缘分', 'en_d': 'Romance luck strength, love opportunity frequency, children destiny', 'ar_d': 'قوة حظ الرومانسية وتكرار فرص الحب ومصير الأطفال'},
            {'zh_l': '四化飞星', 'en_l': '4 Transformations', 'ar_l': 'التحولات الأربعة', 'zh_d': '化禄/化权/化科/化忌在感情宫位的具体影响', 'en_d': 'Specific impact of the 4 transformations on relationship palaces', 'ar_d': 'التأثير المحدد للتحولات الأربعة على قصور العلاقات'}
        ],
        'serviceIntro': {'zh': '购买详细解盘后，你将获得：', 'en': 'After purchasing the detailed reading, you will receive:', 'ar': 'بعد شراء القراءة المفصلة ، ستحصل على:'},
        'services': [
            {'zh': '夫妻宫星曜组合深度解析', 'en': 'In-depth Spouse Palace star combination analysis', 'ar': 'تحليل متعمق لتركيبة نجوم قصر الزوج'},
            {'zh': '桃花运势与恋爱时机分析', 'en': 'Romance fortune and love timing analysis', 'ar': 'تحليل حظ الرومانسية وتوقيت الحب'},
            {'zh': '婚姻适配度与择偶建议', 'en': 'Marriage compatibility and partner selection advice', 'ar': 'نصائح حول توافق الزواج واختيار الشريك'},
            {'zh': '感情中需注意的煞星影响', 'en': 'Malefic star influences to watch for in relationships', 'ar': 'تأثيرات النجوم الضارة التي يجب مراقبتها في العلاقات'},
            {'zh': '大限感情运势推演', 'en': 'Major cycle relationship fortune projection', 'ar': 'توقعات ثروة العلاقة للدورة الكبرى'}
        ]
    },
    'wealth': {
        'title': {'zh': '财运 — 专业解读', 'en': 'Wealth Fortune — Professional Reading', 'ar': 'حظ الثروة — قراءة احترافية'},
        'intro': {'zh': '以<strong>财帛宫</strong>为核心，结合命宫、田宅宫、福德宫，全面解析你的财富密码与求财之道。',
                  'en': 'Using the <strong>Wealth Palace</strong> as the core, combined with Ming Palace, Property Palace, and Fortune Palace, we comprehensively decode your wealth potential and path to prosperity.',
                  'ar': 'باستخدام <strong>قصر الثروة</strong> كنواة ، جنبًا إلى جنب مع قصر مينغ وقصر الممتلكات وقصر الثروة ، نفك شيفرة إمكانات ثروتك وطريقك إلى الازدهار بشكل شامل.'},
        'analyzes': [
            {'zh_l': '命宫主星', 'en_l': 'Ming Palace Star', 'ar_l': 'نجم قصر مينغ', 'zh_d': '先天财运基因，理财观念与消费习惯', 'en_d': 'Innate wealth genes, financial concepts and spending habits', 'ar_d': 'جينات الثروة الفطرية والمفاهيم المالية وعادات الإنفاق'},
            {'zh_l': '财帛宫', 'en_l': 'Wealth Palace', 'ar_l': 'قصر الثروة', 'zh_d': '财运核心指标 — 收入来源、求财方式、财富积累能力', 'en_d': 'Core wealth indicator — income sources, wealth methods, accumulation ability', 'ar_d': 'مؤشر الثروة الأساسي — مصادر الدخل وطرق الثروة والقدرة على التراكم'},
            {'zh_l': '田宅宫', 'en_l': 'Property Palace', 'ar_l': 'قصر الممتلكات', 'zh_d': '不动产运、家庭资产、财富储存与保值能力', 'en_d': 'Real estate fortune, family assets, wealth preservation ability', 'ar_d': 'ثروة العقارات والأصول العائلية والقدرة على الحفاظ على الثروة'},
            {'zh_l': '福德宫', 'en_l': 'Fortune Palace', 'ar_l': 'قصر الثروة', 'zh_d': '偏财运、投资运气、精神满足与物质享受的平衡', 'en_d': 'Speculative wealth luck, investment fortune, balance of spiritual and material fulfillment', 'ar_d': 'حظ الثروة المضاربة وثروة الاستثمار وتوازن الإشباع الروحي والمادي'},
            {'zh_l': '四化飞星', 'en_l': '4 Transformations', 'ar_l': 'التحولات الأربعة', 'zh_d': '化禄/化权/化科/化忌在财帛相关宫位的影响', 'en_d': 'Impact of the 4 transformations on wealth-related palaces', 'ar_d': 'تأثير التحولات الأربعة على القصور المتعلقة بالثروة'}
        ],
        'serviceIntro': {'zh': '购买详细解盘后，你将获得：', 'en': 'After purchasing the detailed reading, you will receive:', 'ar': 'بعد شراء القراءة المفصلة ، ستحصل على:'},
        'services': [
            {'zh': '财帛宫星曜组合深度解析', 'en': 'In-depth Wealth Palace star combination analysis', 'ar': 'تحليل متعمق لتركيبة نجوم قصر الثروة'},
            {'zh': '正财与偏财运势详解', 'en': 'Direct and indirect wealth fortune details', 'ar': 'تفاصيل ثروة الثروة المباشرة وغير المباشرة'},
            {'zh': '投资理财时机与方向建议', 'en': 'Investment timing and direction advice', 'ar': 'نصائح حول توقيت واتجاه الاستثمار'},
            {'zh': '破财风险预警与化解方法', 'en': 'Financial loss risk warning and mitigation', 'ar': 'تحذير من مخاطر الخسارة المالية والتخفيف منها'},
            {'zh': '大限财运走势推演', 'en': 'Major cycle wealth trend projection', 'ar': 'توقعات اتجاه ثروة الدورة الكبرى'}
        ]
    },
    'health': {
        'title': {'zh': '健康运 — 专业解读', 'en': 'Health Fortune — Professional Reading', 'ar': 'حظ الصحة — قراءة احترافية'},
        'intro': {'zh': '以<strong>疾厄宫</strong>为核心，结合命宫、福德宫、迁移宫，全面分析你的身体健康状况与养生调理方向。',
                  'en': 'Using the <strong>Health Palace</strong> as the core, combined with Ming Palace, Fortune Palace, and Travel Palace, we comprehensively analyze your physical health and wellness direction.',
                  'ar': 'باستخدام <strong>قصر الصحة</strong> كنواة ، جنبًا إلى جنب مع قصر مينغ وقصر الثروة وقصر السفر ، نحلل صحتك الجسدية واتجاه العافية بشكل شامل.'},
        'analyzes': [
            {'zh_l': '命宫主星', 'en_l': 'Ming Palace Star', 'ar_l': 'نجم قصر مينغ', 'zh_d': '先天体质强弱，身体能量的基本盘与抵抗力', 'en_d': 'Innate physical constitution, baseline body energy and immunity', 'ar_d': 'التكوين الجسدي الفطري وطاقة الجسم الأساسية والمناعة'},
            {'zh_l': '疾厄宫', 'en_l': 'Health Palace', 'ar_l': 'قصر الصحة', 'zh_d': '健康运核心指标 — 易患疾病类型、意外风险、康复能力', 'en_d': 'Core health indicator — disease susceptibility, accident risk, recovery ability', 'ar_d': 'مؤشر الصحة الأساسي — القابلية للإصابة بالأمراض ومخاطر الحوادث والقدرة على التعافي'},
            {'zh_l': '福德宫', 'en_l': 'Fortune Palace', 'ar_l': 'قصر الثروة', 'zh_d': '心理健康与情绪状态、压力应对能力、养生兴趣方向', 'en_d': 'Mental health and emotional state, stress coping ability, wellness interests', 'ar_d': 'الصحة النفسية والحالة العاطفية والقدرة على التعامل مع التوتر واهتمامات العافية'},
            {'zh_l': '迁移宫', 'en_l': 'Travel Palace', 'ar_l': 'قصر السفر', 'zh_d': '外出安全、交通事故风险、异地养生适应度', 'en_d': 'Travel safety, traffic accident risk, wellness adaptation abroad', 'ar_d': 'سلامة السفر ومخاطر حوادث المرور والتكيف مع العافية في الخارج'},
            {'zh_l': '四化飞星', 'en_l': '4 Transformations', 'ar_l': 'التحولات الأربعة', 'zh_d': '化禄/化权/化科/化忌在疾厄宫的影响，疾病预警与化解方向', 'en_d': 'Impact of the 4 transformations on the Health Palace, disease warning and resolution', 'ar_d': 'تأثير التحولات الأربعة على قصر الصحة وتحذير الأمراض والحل'}
        ],
        'serviceIntro': {'zh': '购买详细解盘后，你将获得：', 'en': 'After purchasing the detailed reading, you will receive:', 'ar': 'بعد شراء القراءة المفصلة ، ستحصل على:'},
        'services': [
            {'zh': '疾厄宫星曜组合深度解析', 'en': 'In-depth Health Palace star combination analysis', 'ar': 'تحليل متعمق لتركيبة نجوم قصر الصحة'},
            {'zh': '先天体质评估与易患疾病预警', 'en': 'Innate constitution assessment and disease susceptibility warning', 'ar': 'تقييم التكوين الفطري وتحذير القابلية للإصابة بالأمراض'},
            {'zh': '各年龄段健康运势推演', 'en': 'Health fortune projection by age group', 'ar': 'توقعات ثروة الصحة حسب الفئة العمرية'},
            {'zh': '养生调理方向与运动建议', 'en': 'Wellness direction and exercise recommendations', 'ar': 'اتجاه العافية وتوصيات التمارين'},
            {'zh': '煞星入疾厄宫的化解指引', 'en': 'Malefic star in Health Palace resolution guide', 'ar': 'دليل حل النجم الضار في قصر الصحة'}
        ]
    }
}

# ─ Star interpretations (STAR_IN_PALACE, EMPTY_PALACE, HUA, PATTERNS) ─
# These are huge. We'll build a wrapper that uses I18N for these.
# For now, keep the Chinese originals but make them accessible via I18N keys.

T['report.sha_hint'] = {'zh': ' 有煞星会照，人生多有磨炼。', 'en': ' Malefic stars present — life has many challenges.', 'ar': ' النجوم الضارة موجودة — الحياة بها العديد من التحديات.'}
T['report.empty_ming'] = {'zh': '命宫为空宫，一生受环境影响较大，可塑性强。需借对宫(父母宫)星曜来看。', 'en': 'Ming Palace is empty — life heavily influenced by environment, highly adaptable. Refer to opposite palace stars.', 'ar': 'قصر مينغ فارغ — الحياة متأثرة بشدة بالبيئة ، قابلة للتكيف بدرجة كبيرة. راجع نجوم القصر المقابل.'}
T['report.aux_stars'] = {'zh': '辅星：', 'en': 'Auxiliary stars: ', 'ar': 'النجوم المساعدة: '}
T['report.aux_hint'] = {'zh': '。增加吉运与助力。', 'en': '. Adds auspicious energy and support.', 'ar': '. يضيف طاقة ميمونة ودعمًا.'}
T['report.sha_stars'] = {'zh': '煞星：', 'en': 'Malefic stars: ', 'ar': 'النجوم الضارة: '}
T['report.sha_hint2'] = {'zh': '。带来挑战与考验。', 'en': '. Brings challenges and trials.', 'ar': '. يجلب التحديات والاختبارات.'}
T['report.hua_prefix'] = {'zh': '化', 'en': 'Hua ', 'ar': 'هوا '}
T['report.shen_hint'] = {'zh': '此宫为身宫，对后天发展影响重大。', 'en': 'This is the Shen Palace, greatly influencing postnatal development.', 'ar': 'هذا هو قصر شن ، يؤثر بشكل كبير على التطور بعد الولادة.'}
T['report.daxian_fmt'] = {'zh': '，大限在', 'en': ', Major Cycle in ', 'ar': '، الدورة الكبرى في '}
T['report.advice'] = {'zh': '命理分析仅供参考，命运掌握在自己手中。紫微斗数揭示的是先天禀赋，而后天的努力、选择和环境因素同样重要。建议发挥命盘中吉星的优势，化解凶星的负面影响，积极面对人生的挑战。', 'en': 'Destiny analysis is for reference only. Your fate is in your own hands. Zi Wei Dou Shu reveals innate endowments, but effort, choices, and environment are equally important. Leverage auspicious stars and resolve malefic influences. Face life\'s challenges positively.', 'ar': 'تحليل المصير هو للمرجعية فقط. مصيرك بين يديك. يكشف زي وي دو شو عن المواهب الفطرية ، لكن الجهد والاختيارات والبيئة مهمة بنفس القدر. استفد من النجوم الميمونة وحل التأثيرات الضارة. واجه تحديات الحياة بإيجابية.'}
T['report.empty_fallback'] = {'zh': '该宫无主星，需参考对宫。', 'en': 'No main star in this palace. Refer to opposite palace.', 'ar': 'لا يوجد نجم رئيسي في هذا القصر. راجع القصر المقابل.'}
T['report.star_fallback'] = {'zh': '入', 'en': ' enters ', 'ar': ' يدخل '}
T['report.star_fallback2'] = {'zh': '，对', 'en': ', affects ', 'ar': '، يؤثر على '}
T['report.star_fallback3'] = {'zh': '产生影响。', 'en': '.', 'ar': '.'}
T['report.ming_prefix'] = {'zh': '命宫在', 'en': 'Ming Palace: ', 'ar': 'قصر مينغ: '}
T['report.sihua_fmt'] = {'zh': '四化：', 'en': '4 Hua: ', 'ar': 'التحولات الأربعة: '}
T['report.ming_main'] = {'zh': '宫，主星：', 'en': ', main stars: ', 'ar': '، النجوم الرئيسية: '}

# Additional chart render strings
T['chart.daxian_range'] = {'zh': '~', 'en': '–', 'ar': '–'}

# ─ BUILD I18N JS BLOCK ────────────────────────────────────────

def js_str(s):
    """Escape string for JS single-quoted string."""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

def build_i18n_js():
    """Build the I18N JavaScript block."""
    lines = []
    lines.append('<script id="i18n-data">')
    lines.append('// ============================================================')
    lines.append('// I18N — Multi-language support (zh/en/ar)')
    lines.append('// ============================================================')
    lines.append('var I18N = {')
    lines.append('  current: "zh",')
    lines.append('  data: { zh: {}, en: {}, ar: {} },')
    lines.append('  t: function(key) {')
    lines.append('    return (this.data[this.current] && this.data[this.current][key]) ||')
    lines.append('           (this.data.zh[key]) || key;')
    lines.append('  },')
    lines.append('  setLanguage: function(lang) {')
    lines.append('    this.current = lang;')
    lines.append('    document.documentElement.lang = lang === "ar" ? "ar" : lang === "en" ? "en" : "zh-CN";')
    lines.append('    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";')
    lines.append('    document.documentElement.style.fontFamily = lang === "ar" ?')
    lines.append('      "\'Noto Naskh Arabic\',\'Traditional Arabic\',\'Scheherazade New\',-apple-system,sans-serif" :')
    lines.append('      "";')
    lines.append('    localStorage.setItem("zwei_lang", lang);')
    lines.append('    this.translatePage();')
    lines.append('    // Update lang switcher buttons')
    lines.append('    var btns = document.querySelectorAll(".lang-btn");')
    lines.append('    btns.forEach(function(b) { b.classList.toggle("active", b.dataset.lang === lang); });')
    lines.append('  },')
    lines.append('  translatePage: function() {')
    lines.append('    var self = this;')
    lines.append('    // data-i18n attributes')
    lines.append('    document.querySelectorAll("[data-i18n]").forEach(function(el) {')
    lines.append('      var key = el.dataset.i18n;')
    lines.append('      var text = self.t(key);')
    lines.append('      if (text && text !== key) el.textContent = text;')
    lines.append('    });')
    lines.append('    // data-i18n-placeholder')
    lines.append('    document.querySelectorAll("[data-i18n-placeholder]").forEach(function(el) {')
    lines.append('      var key = el.dataset.i18nPlaceholder;')
    lines.append('      var text = self.t(key);')
    lines.append('      if (text && text !== key) el.placeholder = text;')
    lines.append('    });')
    lines.append('    // data-i18n-html elements (for rich content)')
    lines.append('    document.querySelectorAll("[data-i18n-html]").forEach(function(el) {')
    lines.append('      var key = el.dataset.i18nHtml;')
    lines.append('      var text = self.t(key);')
    lines.append('      if (text && text !== key) el.innerHTML = text;')
    lines.append('    });')
    lines.append('  }')
    lines.append('};')
    lines.append('')

    # Populate translation data
    for key, vals in sorted(T.items()):
        for lang in ['zh', 'en', 'ar']:
            if lang in vals:
                lines.append(f"I18N.data.{lang}['{key}'] = '{js_str(vals[lang])}';")

    # Add hour options
    for i in range(12):
        lines.append(f"I18N.data.zh['hour.{i}'] = '{HOUR_NAMES_ZH[i]}';")
        lines.append(f"I18N.data.en['hour.{i}'] = '{HOUR_NAMES_EN[i]}';")
        lines.append(f"I18N.data.ar['hour.{i}'] = '{HOUR_NAMES_AR[i]}';")

    # Add category data
    for cat_key in CAT_KEYS:
        cat = CAT_FIELDS[cat_key]
        for field in ['title', 'intro', 'serviceIntro']:
            for lang in ['zh', 'en', 'ar']:
                lines.append(f"I18N.data.{lang}['cat.{cat_key}.{field}'] = '{js_str(cat[field][lang])}';")
        # analyzes
        for ai, a in enumerate(cat['analyzes']):
            for lang in ['zh', 'en', 'ar']:
                lines.append(f"I18N.data.{lang}['cat.{cat_key}.analyze.{ai}.label'] = '{js_str(a[lang+'_l'])}';")
                lines.append(f"I18N.data.{lang}['cat.{cat_key}.analyze.{ai}.desc'] = '{js_str(a[lang+'_d'])}';")
        # services
        for si, s in enumerate(cat['services']):
            for lang in ['zh', 'en', 'ar']:
                lines.append(f"I18N.data.{lang}['cat.{cat_key}.service.{si}'] = '{js_str(s[lang])}';")

    lines.append('')
    lines.append('// Initialize from saved preference')
    lines.append('(function() {')
    lines.append('  var saved = localStorage.getItem("zwei_lang");')
    lines.append('  if (saved && (saved === "zh" || saved === "en" || saved === "ar")) {')
    lines.append('    I18N.current = saved;')
    lines.append('  } else {')
    lines.append('    var browserLang = (navigator.language || "").split("-")[0];')
    lines.append('    if (browserLang === "ar") I18N.current = "ar";')
    lines.append('    else if (browserLang === "en") I18N.current = "en";')
    lines.append('  }')
    lines.append('  I18N.setLanguage(I18N.current);')
    lines.append('})();')
    lines.append('</script>')

    return '\n'.join(lines) + '\n'

i18n_js = build_i18n_js()

# ─ BUILD LANGUAGE SWITCHER HTML ────────────────────────────────
LANG_SWITCHER = '''    <div class="lang-switcher">
      <button class="lang-btn" data-lang="zh" onclick="I18N.setLanguage('zh')">中</button>
      <button class="lang-btn" data-lang="en" onclick="I18N.setLanguage('en')">EN</button>
      <button class="lang-btn" data-lang="ar" onclick="I18N.setLanguage('ar')">عربي</button>
    </div>'''

# ─ BUILD CSS ADDITIONS ─────────────────────────────────────────
CSS_ADDITIONS = '''
/* ===== Language Switcher ===== */
.lang-switcher{
  display:flex;align-items:center;gap:4px;margin-left:16px;
  background:rgba(255,255,255,0.08);border-radius:20px;padding:3px
}
.lang-btn{
  background:transparent;border:none;color:#c0b8d0;font-size:0.75rem;
  font-weight:bold;padding:5px 10px;border-radius:17px;cursor:pointer;
  transition:all 0.2s;white-space:nowrap;font-family:inherit
}
.lang-btn:hover{color:#D4AF37}
.lang-btn.active{background:#D4AF37;color:#1a1a2e}
@media(max-width:768px){
  .lang-switcher{margin-left:0;margin-top:8px}
}

/* ===== RTL Support (Arabic) ===== */
[dir="rtl"] body{direction:rtl}
[dir="rtl"] .header-inner{flex-direction:row}
[dir="rtl"] .header-nav{flex-direction:row}
[dir="rtl"] .hero-content,[dir="rtl"] .section-header{text-align:center}
[dir="rtl"] .steps-grid .step-arrow{right:auto;left:-24px;transform:scaleX(-1)}
[dir="rtl"] .cat-analyze-item{text-align:right}
[dir="rtl"] .cat-service-list li{border-left:none;border-right:3px solid #D4AF37;text-align:right}
[dir="rtl"] .palace-card{direction:rtl}
[dir="rtl"] .palace-header{flex-direction:row}
[dir="rtl"] .faq-q span:last-child{margin-left:0;margin-right:auto}
[dir="rtl"] .chart-cell{direction:rtl}
[dir="rtl"] .feature-cta{direction:rtl}
[dir="rtl"] .modal-body{text-align:right}
[dir="rtl"] .chart-actions{direction:rtl}
[dir="rtl"] .testimonial-card{text-align:right}
[dir="rtl"] .footer-links{flex-direction:row}
'''

# ─ INSERT INTO HTML (structural changes only) ───────────────────

# (I18N script block will be inserted at the END after all JS replacements)

# 1. Insert language switcher into header
header_menu_btn = html.find('mobile-menu-btn')
header_inner_end = html.find('</div>', html.find('header-inner', header_menu_btn))
html = html[:header_inner_end] + LANG_SWITCHER + html[header_inner_end:]

# 3. Add CSS additions before </style>
style_end = html.find('</style>')
html = html[:style_end] + CSS_ADDITIONS + '\n' + html[style_end:]

# 4. Update <html> tag to remove hardcoded lang (now dynamic via I18N)
html = html.replace('<html lang="zh-CN">', '<html>')

# ─ MODIFY HTML FOR data-i18n ATTRIBUTES ─────────────────────────
# We need to transform static HTML text to use data-i18n attributes.
# Strategy: Replace text content with data-i18n and use translatePage to fill.

# Define replacements: (old_text_pattern, data_i18n_key, tag_context)
# We use regex to find the text and add the attribute

# Actually, for reliability, let's do targeted string replacements
# that add data-i18n attributes while keeping text content as fallback.

replacements = [
    # Title
    ('<title>紫微斗数 - 命理分析</title>', '<title data-i18n="site.title">紫微斗数 - 命理分析</title>'),
    # Header nav links
    ('<a href="#features">服务分类</a>', '<a href="#features" data-i18n="header.nav.services">服务分类</a>'),
    ('<a href="#how-it-works">如何使用</a>', '<a href="#how-it-works" data-i18n="header.nav.how">如何使用</a>'),
    ('<a href="#form">在线排盘</a>', '<a href="#form" data-i18n="header.nav.chart">在线排盘</a>'),
    ('<a href="#pricing">定价</a>', '<a href="#pricing" data-i18n="header.nav.pricing">定价</a>'),
    ('<a href="#faq">常见问题</a>', '<a href="#faq" data-i18n="header.nav.faq">常见问题</a>'),
    # Header CTA
    ("class=\"header-cta\" onclick=\"document.getElementById('form').scrollIntoView({behavior:'smooth'})\">立即解密<", "class=\"header-cta\" onclick=\"document.getElementById('form').scrollIntoView({behavior:'smooth'})\" data-i18n=\"header.cta\">立即解密<"),
    # Hero
    ('class="hero-badge">⭐ 紫微斗数 · 专业解密 · 隐私保护<', 'class="hero-badge" data-i18n="hero.badge">⭐ 紫微斗数 · 专业解密 · 隐私保护<'),
    ('用千年智慧，<br>解密你的<span class="gold">人生运势</span>', '<span data-i18n="hero.title.line1">用千年智慧，</span><br><span data-i18n="hero.title.line2">解密你的</span><span class="gold" data-i18n="hero.title.gold">人生运势</span>'),
    # Hero sub
    ('class="hero-sub">基于传统紫微斗数算法，精准排盘，十二宫详解<br>命盘格局 · 大限运势 · 四化飞星 · 综合解读<', 'class="hero-sub"><span data-i18n="hero.sub.line1">基于传统紫微斗数算法，精准排盘，十二宫详解</span><br><span data-i18n="hero.sub.line2">命盘格局 · 大限运势 · 四化飞星 · 综合解读</span><'),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
    else:
        print(f"WARNING: Replacement not found: {old[:60]}...")

# ─ MODIFY JS DYNAMIC TEXT ──────────────────────────────────────
# Replace key strings in App JS with I18N.t() calls

js_replacements = [
    # Toast messages
    ("showToast('请选择出生日期')", "showToast(I18N.t('toast.select_date'))"),
    ("showToast('仅支持1900-2100年范围')", "showToast(I18N.t('toast.year_range'))"),
    ("showToast('排盘失败，请检查日期')", "showToast(I18N.t('toast.calc_failed'))"),
    ("showToast('信息缺失，请重新排盘')", "showToast(I18N.t('toast.info_missing'))"),
    ("showToast('支付服务暂时不可用\\n请确认已配置 Stripe 密钥后重试')", "showToast(I18N.t('toast.stripe_config'))"),
    ("showToast('网络错误，请重试')", "showToast(I18N.t('toast.network_error'))"),
    ("showToast('读取信息失败，请重新输入出生信息')", "showToast(I18N.t('toast.data_missing'))"),
    ("showToast('支付成功！正在展示详细解盘...')", "showToast(I18N.t('toast.pay_success'))"),
    ("showToast('数据恢复失败，请重新输入出生信息')", "showToast(I18N.t('toast.data_restore'))"),
    ("showToast('支付验证失败，请稍后再试或联系客服')", "showToast(I18N.t('toast.verify_fail'))"),
    ("showToast('网络错误，无法验证支付状态')", "showToast(I18N.t('toast.verify_network'))"),

    # Button text in renderChart
    ("'查看详细解盘'", "I18N.t('chart.btn_detail')"),
    ("'重新输入'", "I18N.t('chart.btn_reset')"),

    # Button state text
    ("'查看详细解盘 ✓ 已解锁'", "I18N.t('chart.btn_unlocked')"),

    # Calculating state
    ("'<span class=\"spinner\"></span> 计算中...'", "I18N.t('chart.calculating')"),
    ("btn.textContent = '开始排盘'", "btn.textContent = I18N.t('form.submit')"),

    # renderChart dynamic text
    ("'五行局'", "I18N.t('chart.element_label')"),
    ("'<span class=\"cell-shen-tag\">身</span>'", "'<span class=\"cell-shen-tag\">'+I18N.t('chart.shen_tag')+'</span>'"),
    ("'男'", "I18N.t('chart.male')"),
    ("'女'", "I18N.t('chart.female')"),

    # Ganzhi bar prefixes
    ("'年 '+cd.birthInfo.yearGanZhi", "I18N.t('chart.year_prefix')+cd.birthInfo.yearGanZhi"),
    ("'月 '+cd.birthInfo.monthGanZhi", "I18N.t('chart.month_prefix')+cd.birthInfo.monthGanZhi"),
    ("'日 '+cd.birthInfo.dayGanZhi", "I18N.t('chart.day_prefix')+cd.birthInfo.dayGanZhi"),
    ("'时 '+cd.birthInfo.hourGanZhi", "I18N.t('chart.hour_prefix')+cd.birthInfo.hourGanZhi"),
    ("cd.birthInfo.animal+'年'", "cd.birthInfo.animal+I18N.t('chart.year_suffix')"),

    # Sihua bar
    ("'四化：'", "I18N.t('chart.sihua_label')"),
    ("cd.hua.lu+'化禄'", "cd.hua.lu+I18N.t('chart.hualu_suffix')"),
    ("cd.hua.quan+'化权'", "cd.hua.quan+I18N.t('chart.huaquan_suffix')"),
    ("cd.hua.ke+'化科'", "cd.hua.ke+I18N.t('chart.huake_suffix')"),
    ("cd.hua.ji+'化忌'", "cd.hua.ji+I18N.t('chart.huaji_suffix')"),

    # DaXian section title
    ("'<span class=\"section-title\">大限</span>'", "'<span class=\"section-title\">'+I18N.t('chart.daxian_title')+'</span>'"),

    # onPalaceTap
    ("'无主星'", "I18N.t('chart.no_stars')"),

    # Name fallback
    ("name: document.getElementById('inputName').value || '未知'", "name: document.getElementById('inputName').value || I18N.t('chart.unknown_name')"),

    # birthInfo name
    ("document.getElementById('inputName').value || '未知'", "document.getElementById('inputName').value || I18N.t('chart.unknown_name')"),
]

for old, new in js_replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
    else:
        print(f"WARNING: JS replacement not found ({count}x): {old[:60]}...")

# ─ MODIFY showPaymentModal ────────────────────────────────────
# Replace the hardcoded payment modal text
old_pay_title = "var title = '解锁详细解盘';"
new_pay_title = "var title = I18N.t('pay.title');"
html = html.replace(old_pay_title, new_pay_title)

old_pay_body = """var body =
      '🔮 完整命盘解读内容：\\n\\n'+
      '✦ 十二宫详细解读\\n'+
      '✦ 命盘格局分析\\n'+
      '✦ 大限运势解读\\n'+
      '✦ 四化飞星详解\\n'+
      '✦ 综合运势建议\\n\\n'+
      '一次性付费 ' + priceDisplay + '\\n'+
      '付费后永久查看当前命盘解读';"""

new_pay_body = """var body =
      I18N.t('pay.body.intro') + '\\n\\n'+
      I18N.t('pay.body.item1') + '\\n'+
      I18N.t('pay.body.item2') + '\\n'+
      I18N.t('pay.body.item3') + '\\n'+
      I18N.t('pay.body.item4') + '\\n'+
      I18N.t('pay.body.item5') + '\\n\\n'+
      I18N.t('pay.body.price') + priceDisplay + '\\n'+
      I18N.t('pay.body.forever');"""
html = html.replace(old_pay_body, new_pay_body)

# Payment button text
html = html.replace("payBtn.textContent = '💳 立即支付 $9.99';", "payBtn.textContent = I18N.t('pay.btn');")
html = html.replace("payBtn.textContent = '正在跳转支付...';", "payBtn.textContent = I18N.t('pay.redirecting');")

# ─ MODIFY renderDetail ─────────────────────────────────────────
detail_replacements = [
    ("'的命盘解读'", "I18N.t('detail.title_suffix')"),
    ("'年 · '+cd.element+' · '+cd.birthInfo.animal+'年'",
     "cd.birthInfo.yearGanZhi+I18N.t('detail.year_sep')+cd.element+I18N.t('detail.year_sep')+cd.birthInfo.animal+I18N.t('chart.year_suffix')"),
    ("'命宫在'+cd.birthInfo.lunar.monthStr+' '+cd.birthInfo.lunar.dayStr+' · '+cd.birthInfo.hour.name+' · 身宫在'+palaceNames[cd.shenBranch]+'宫'",
     "I18N.t('detail.ming_in')+cd.birthInfo.lunar.monthStr+' '+cd.birthInfo.lunar.dayStr+I18N.t('detail.shen_in')+palaceNames[cd.shenBranch]+I18N.t('detail.palace_suffix')"),
    ("'五行'+cd.element+' · 大限每'+cd.elementYears+'年一运 · '+(cd.forward?'阳男顺行':'阴男逆行')",
     "I18N.t('detail.element_prefix')+cd.element+I18N.t('detail.daxian_every')+cd.elementYears+I18N.t('detail.years_per')+' · '+(cd.forward?I18N.t('detail.forward'):I18N.t('detail.reverse'))"),
    ("'四化飞星'", "I18N.t('detail.sihua_title')"),
    ("'命盘格局'", "I18N.t('detail.patterns_title')"),
    ("'十二宫详解'", "I18N.t('detail.palaces_title')"),
    ("'大限运势'", "I18N.t('detail.daxian_title')"),
    ("'四化总结'", "I18N.t('detail.summary_title')"),
    ("'温馨提示'", "I18N.t('detail.advice_title')"),
    ("'返回命盘'", "I18N.t('detail.btn_back')"),
    # Hua card labels
    ("'化禄'", "I18N.t('detail.hualu')"),
    ("'财禄顺利'", "I18N.t('detail.hualu_desc')"),
    # Note: we already replaced '化权' '化科' '化忌' above as hua suffixes
    # Need to be more careful here - the detail view has '化禄' as a hua-type label
    # but chart has '化禄' as a suffix. Since the chart replacements happened first,
    # the detail '化禄' should still be the original. Let's handle the duplicates.
    # Actually, these are already replaced. Let's just do the desc replacements.
]

for old, new in detail_replacements:
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)

# Detail view hua card labels (after the chart replacements consumed '化禄' etc.)
# These are the <span class="hua-type"> labels
html = html.replace("'<span class=\"hua-type\">化禄</span>'", "'<span class=\"hua-type\">'+I18N.t('detail.hualu')+'</span>'")
html = html.replace("'<span class=\"hua-type\">化权</span>'", "'<span class=\"hua-type\">'+I18N.t('detail.huaquan')+'</span>'")
html = html.replace("'<span class=\"hua-type\">化科</span>'", "'<span class=\"hua-type\">'+I18N.t('detail.huake')+'</span>'")
html = html.replace("'<span class=\"hua-type\">化忌</span>'", "'<span class=\"hua-type\">'+I18N.t('detail.huaji')+'</span>'")

# Detail hua card descriptions
html = html.replace("'<span class=\"hua-desc\">财禄顺利</span>'", "'<span class=\"hua-desc\">'+I18N.t('detail.hualu_desc')+'</span>'")
html = html.replace("'<span class=\"hua-desc\">掌权增强</span>'", "'<span class=\"hua-desc\">'+I18N.t('detail.huaquan_desc')+'</span>'")
html = html.replace("'<span class=\"hua-desc\">文名声誉</span>'", "'<span class=\"hua-desc\">'+I18N.t('detail.huake_desc')+'</span>'")
html = html.replace("'<span class=\"hua-desc\">困扰阻碍</span>'", "'<span class=\"hua-desc\">'+I18N.t('detail.huaji_desc')+'</span>'")

# ─ MODIFY generateReport ──────────────────────────────────────
report_replacements = [
    ("'命宫在'+ming.branch+'宫，主星：'+mingMain.join('、')+'。'",
     "I18N.t('report.ming_prefix')+ming.branch+I18N.t('detail.palace_suffix')+I18N.t('report.ming_main')+mingMain.join('、')+'。'"),
    ("' 有煞星会照，人生多有磨炼。'",
     "I18N.t('report.sha_hint')"),
    ("'命宫在'+ming.branch+'宫为空宫，一生受环境影响较大，可塑性强。需借对宫(父母宫)星曜来看。'",
     "I18N.t('report.ming_prefix')+ming.branch+I18N.t('detail.palace_suffix')+I18N.t('report.empty_ming')"),
    ("'辅星：'+aux.join('、')+'。增加吉运与助力。'",
     "I18N.t('report.aux_stars')+aux.join('、')+I18N.t('report.aux_hint')"),
    ("'煞星：'+sha.join('、')+'。带来挑战与考验。'",
     "I18N.t('report.sha_stars')+sha.join('、')+I18N.t('report.sha_hint2')"),
    ("'此宫为身宫，对后天发展影响重大。'",
     "I18N.t('report.shen_hint')"),
    ("'，大限在'+dxp.name+dxp.branch+'宫。'",
     "I18N.t('report.daxian_fmt')+dxp.name+dxp.branch+I18N.t('detail.palace_suffix')+'。'"),
    ("'该宫无主星，需参考对宫。'",
     "I18N.t('report.empty_fallback')"),
    ("n+'入'+pal.name+'，对'+pal.name+'产生影响。'",
     "n+I18N.t('report.star_fallback')+pal.name+I18N.t('report.star_fallback2')+pal.name+I18N.t('report.star_fallback3')"),
    # report.advice
    ("report.advice = '命理分析仅供参考，命运掌握在自己手中。紫微斗数揭示的是先天禀赋，而后天的努力、选择和环境因素同样重要。建议发挥命盘中吉星的优势，化解凶星的负面影响，积极面对人生的挑战。';",
     "report.advice = I18N.t('report.advice');"),
    # report.huaSummary
    ("report.huaSummary = '四化：'+hua.lu+'化禄、'+hua.quan+'化权、'+hua.ke+'化科、'+hua.ji+'化忌';",
     "report.huaSummary = I18N.t('report.sihua_fmt')+hua.lu+I18N.t('chart.hualu_suffix')+'、'+hua.quan+I18N.t('chart.huaquan_suffix')+'、'+hua.ke+I18N.t('chart.huake_suffix')+'、'+hua.ji+I18N.t('chart.huaji_suffix');"),
]

for old, new in report_replacements:
    if old in html:
        html = html.replace(old, new)
    else:
        print(f"WARNING: Report replacement not found: {old[:60]}...")

# ─ MODIFY showCategory ─────────────────────────────────────────
# Category modal section labels and buttons
html = html.replace("'分析维度'", "I18N.t('cat.analyze_label')")
html = html.replace("'服务内容'", "I18N.t('cat.service_label')")
html = html.replace("payBtn.textContent = '立即排盘解锁解读';", "payBtn.textContent = I18N.t('cat.btn_goto');")
html = html.replace("cancelBtn.textContent = '关闭';", "cancelBtn.textContent = I18N.t('cat.btn_close');")

# ─ MODIFY CATEGORIES object to use translations ───────────────
# This is the trickiest part. The CATEGORIES object has nested Chinese text.
# We'll replace the static data with a function that returns translated data.
# Find the CATEGORIES object start and end

# Find "var CATEGORIES = {"
cat_start = html.find('var CATEGORIES = {')
# Find the closing "};" of CATEGORIES (before showCategory function)
# showCategory starts immediately after
show_cat_fn = html.find('function showCategory', cat_start)
cat_end = html.rfind('};', cat_start, show_cat_fn)

if cat_start > 0 and cat_end > 0:
    # Replace the entire CATEGORIES object with a getter function
    old_cat = html[cat_start:cat_end+2]
    new_cat = '''var CATEGORIES = {
  getData: function(key) {
    return {
      title: I18N.t('cat.'+key+'.title'),
      intro: I18N.t('cat.'+key+'.intro'),
      analyzes: [
        { label: I18N.t('cat.'+key+'.analyze.0.label'), desc: I18N.t('cat.'+key+'.analyze.0.desc') },
        { label: I18N.t('cat.'+key+'.analyze.1.label'), desc: I18N.t('cat.'+key+'.analyze.1.desc') },
        { label: I18N.t('cat.'+key+'.analyze.2.label'), desc: I18N.t('cat.'+key+'.analyze.2.desc') },
        { label: I18N.t('cat.'+key+'.analyze.3.label'), desc: I18N.t('cat.'+key+'.analyze.3.desc') },
        { label: I18N.t('cat.'+key+'.analyze.4.label'), desc: I18N.t('cat.'+key+'.analyze.4.desc') }
      ],
      serviceIntro: I18N.t('cat.'+key+'.serviceIntro'),
      services: [
        I18N.t('cat.'+key+'.service.0'),
        I18N.t('cat.'+key+'.service.1'),
        I18N.t('cat.'+key+'.service.2'),
        I18N.t('cat.'+key+'.service.3'),
        I18N.t('cat.'+key+'.service.4')
      ],
      price: '$9.99',
      priceNote: I18N.t('pricing.period')
    };
  }
};'''
    html = html[:cat_start] + new_cat + html[cat_end+2:]

# Update showCategory function to use CATEGORIES.getData
html = html.replace('var cat = CATEGORIES[key];', 'var cat = CATEGORIES.getData(key);')

# ─ MODIFY closeModal for multilingual default button ───────────
html = html.replace("payBtn.textContent = '知道了';", "payBtn.textContent = I18N.t('modal.ok');")

# ─ MODIFY hour option rendering ────────────────────────────────
# The hour options are in the HTML. We need to make them dynamic.
# Find the select with id="inputHour" and replace options
hour_select_pattern = r'<select class="form-select" id="inputHour">.*?</select>'
hour_match = re.search(hour_select_pattern, html, re.DOTALL)
if hour_match:
    new_hour_select = '''<select class="form-select" id="inputHour">
            <option value="0" data-i18n="hour.0">子时 (23:00-01:00)</option>
            <option value="1" data-i18n="hour.1">丑时 (01:00-03:00)</option>
            <option value="2" data-i18n="hour.2">寅时 (03:00-05:00)</option>
            <option value="3" data-i18n="hour.3">卯时 (05:00-07:00)</option>
            <option value="4" data-i18n="hour.4">辰时 (07:00-09:00)</option>
            <option value="5" data-i18n="hour.5">巳时 (09:00-11:00)</option>
            <option value="6" data-i18n="hour.6">午时 (11:00-13:00)</option>
            <option value="7" data-i18n="hour.7">未时 (13:00-15:00)</option>
            <option value="8" data-i18n="hour.8">申时 (15:00-17:00)</option>
            <option value="9" data-i18n="hour.9">酉时 (17:00-19:00)</option>
            <option value="10" data-i18n="hour.10">戌时 (19:00-21:00)</option>
            <option value="11" data-i18n="hour.11">亥时 (21:00-23:00)</option>
          </select>'''
    html = html[:hour_match.start()] + new_hour_select + html[hour_match.end():]

# ─ UPDATE translatePage to handle <option> text ───────────────
# Options need special handling since their text is set differently
old_trans_fn = '''  translatePage: function() {
    var self = this;
    // data-i18n attributes
    document.querySelectorAll("[data-i18n]").forEach(function(el) {
      var key = el.dataset.i18n;
      var text = self.t(key);
      if (text && text !== key) el.textContent = text;
    });
    // data-i18n-placeholder
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function(el) {
      var key = el.dataset.i18nPlaceholder;
      var text = self.t(key);
      if (text && text !== key) el.placeholder = text;
    });
    // data-i18n-html elements (for rich content)
    document.querySelectorAll("[data-i18n-html]").forEach(function(el) {
      var key = el.dataset.i18nHtml;
      var text = self.t(key);
      if (text && text !== key) el.innerHTML = text;
    });
  }'''

new_trans_fn = '''  translatePage: function() {
    var self = this;
    // data-i18n attributes
    document.querySelectorAll("[data-i18n]").forEach(function(el) {
      var key = el.dataset.i18n;
      var text = self.t(key);
      if (text && text !== key) {
        if (el.tagName === 'OPTION') {
          el.text = text;
        } else {
          el.textContent = text;
        }
      }
    });
    // data-i18n-placeholder
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function(el) {
      var key = el.dataset.i18nPlaceholder;
      var text = self.t(key);
      if (text && text !== key) el.placeholder = text;
    });
    // data-i18n-html elements (for rich content)
    document.querySelectorAll("[data-i18n-html]").forEach(function(el) {
      var key = el.dataset.i18nHtml;
      var text = self.t(key);
      if (text && text !== key) el.innerHTML = text;
    });
  }'''

html = html.replace(old_trans_fn, new_trans_fn)

# ─ ADD LANGUAGE CHANGE CALLBACK ───────────────────────────────
# When language changes, re-render chart/detail if visible
# Hook into I18N.setLanguage after translatePage call
old_setlang_end = "    this.translatePage();"
new_setlang_end = """    this.translatePage();
    // Re-render chart or detail if currently displayed
    if (typeof App !== 'undefined' && App.onLanguageChange) {
      App.onLanguageChange();
    }"""
html = html.replace(old_setlang_end, new_setlang_end)

# Add onLanguageChange to App module (before return statement)
old_return = "  return {"
new_return = """  function onLanguageChange() {
    if (state.chartData) {
      renderChart();
      if (state.report) {
        var cd = state.chartData;
        document.getElementById('detailContainer').innerHTML = renderDetail(cd, state.report);
      }
    }
  }

  return {"""
html = html.replace(old_return, new_return)

# Add onLanguageChange to return exports
html = html.replace(
    "showCategory: showCategory",
    "showCategory: showCategory,\n    onLanguageChange: onLanguageChange"
)

# ─ ADD REMAINING STATIC HTML data-i18n ATTRIBUTES ──────────────
# We need to add data-i18n to sections that still have hardcoded Chinese text.
# But doing this all via string replacement is impractical for all ~85 items.
# The key sections we've covered. Let's add remaining via targeted replacements.

# Feature cards - add data-i18n to name, desc, cta
for cat_name in ['career', 'love', 'wealth', 'health']:
    # Feature name
    cn_text = CAT_FIELDS[cat_name]['title']['zh'].split(' — ')[0]
    old_name = f'<div class="feature-name">{cn_text}</div>'
    new_name = f'<div class="feature-name" data-i18n="features.{cat_name}.name">{cn_text}</div>'
    if old_name in html:
        html = html.replace(old_name, new_name)
    else:
        print(f"WARNING: Feature name not found for {cat_name}")

    # Feature desc
    cn_desc = T[f'features.{cat_name}.desc']['zh']
    old_desc = f'<div class="feature-desc">{cn_desc}</div>'
    new_desc = f'<div class="feature-desc" data-i18n="features.{cat_name}.desc">{cn_desc}</div>'
    if old_desc in html:
        html = html.replace(old_desc, new_desc)
    else:
        print(f"WARNING: Feature desc not found for {cat_name}")

# Feature CTA
html = html.replace('点击了解详情 →', '<span data-i18n="features.cta">点击了解详情 →</span>')

# Section labels and titles with data-i18n
section_attrs = [
    ('<div class="section-label">服务分类</div>', '<div class="section-label" data-i18n="features.label">服务分类</div>'),
    ('<h2 class="section-title">全方位命运解读</h2>', '<h2 class="section-title" data-i18n="features.title">全方位命运解读</h2>'),
    ('<p class="section-desc">从事业财运到感情健康，紫微斗数为你揭示人生的各个面向</p>', '<p class="section-desc" data-i18n="features.desc">从事业财运到感情健康，紫微斗数为你揭示人生的各个面向</p>'),
]

for old, new in section_attrs:
    if old in html:
        html = html.replace(old, new)

# ─ INSERT I18N DATA BLOCK (after all JS replacements) ──────────
first_script_pos = html.find('<script>', html.find('<body>'))
html = html[:first_script_pos] + i18n_js + html[first_script_pos:]

# ─ WRITE OUTPUT ─────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Done! New index.html: {len(html)} bytes')
print(f'I18N script: {len(i18n_js)} bytes')
print(f'Translation keys: {len(T)}')
print(f'Category translations: 4 categories x 17 fields each')
