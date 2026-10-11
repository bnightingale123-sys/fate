# -*- coding: utf-8 -*-
"""Add Japanese (ja) translations to index.html.

Inserts I18N.data.ja lines for every existing key and registers ja
in the I18N data object. Branding "地狱占卜师" is used in site.title
and hero.badge.

Run once: python tools/add_ja.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")

# ── Japanese translations (279 keys) ───────────────────────────
JA = {
    # cat.*
    "cat.analyze_label": "🔍 分析ポイント",
    "cat.btn_close": "閉じる",
    "cat.btn_goto": "命盤を作成して鑑定をアンロック",
    "cat.service_label": "📦 サービス内容",
    # chart.*
    "chart.age_suffix": "歳",
    "chart.btn_detail": "詳細鑑定を見る",
    "chart.btn_reset": "再入力",
    "chart.btn_unlocked": "詳細鑑定を見る ✓ アンロック済み",
    "chart.calculating": "計算中...",
    "chart.daxian_range": "〜",
    "chart.daxian_title": "大限",
    "chart.day_prefix": "日 ",
    "chart.element_label": "五行局",
    "chart.female": "女",
    "chart.hour_prefix": "時 ",
    "chart.huaji_suffix": "化忌",
    "chart.huake_suffix": "化科",
    "chart.hualu_suffix": "化禄",
    "chart.huaquan_suffix": "化権",
    "chart.male": "男",
    "chart.month_prefix": "月 ",
    "chart.no_stars": "主星なし",
    "chart.shen_tag": "身",
    "chart.sihua_label": "四化：",
    "chart.unknown_name": "不明",
    "chart.year_prefix": "年 ",
    "chart.year_suffix": "年",
    # cta.*
    "cta.btn": "🔮 今すぐ始める",
    "cta.desc": "出生情報を入力すると、あなた専用の紫微斗数命盤鑑定をすぐに入手できます",
    "cta.title": "あなたの運勢を解読する準備はできましたか？",
    # detail.*
    "detail.advice_title": "ご注意",
    "detail.btn_back": "命盤に戻る",
    "detail.daxian_every": " · 大限は",
    "detail.daxian_title": "大限運勢",
    "detail.element_prefix": "五行",
    "detail.forward": "陽男は順行",
    "detail.huaji": "化忌",
    "detail.huaji_desc": "悩みと障壁",
    "detail.huake": "化科",
    "detail.huake_desc": "名声と評判",
    "detail.hualu": "化禄",
    "detail.hualu_desc": "財運と収入が順調",
    "detail.huaquan": "化権",
    "detail.huaquan_desc": "権力と統率力が向上",
    "detail.ming_in": "命宮は",
    "detail.palace_suffix": "宮",
    "detail.palaces_title": "十二宮の詳解",
    "detail.patterns_title": "命盤の格局",
    "detail.reverse": "陰男は逆行",
    "detail.shen_in": " · 身宮は",
    "detail.sihua_prefix": "四化：",
    "detail.sihua_title": "四化飛星",
    "detail.summary_title": "四化まとめ",
    "detail.title_suffix": "さんの命盤鑑定",
    "detail.year_sep": "年 · ",
    "detail.years_per": "年ごと",
    # faq.*
    "faq.a1": "紫微斗数は中国の伝統的な命理学の重要な分野で、宋代に起源を持ちます。生年月日と時刻から十二宮の星の配置を算出し、人生の各側面の運勢や発展傾向を分析します。八字（四柱推命）と並ぶ中国伝統命理学の二大体系の一つです。",
    "faq.a2": "伝統的な紫微斗数アルゴリズムを用い、古来の計算法に厳密に従って星の配置と四化飛星を算出しています。ただし、命理分析はあくまで参考情報であり、人生の行方はご自身の選択と努力に大きく左右されます。",
    "faq.a3": "出生情報は命盤の計算にのみ使用され、個人データの保存や共有は一切行いません。お支払いはStripeが安全に処理し、当サイトが決済情報に触れることはありません。",
    "faq.a4": "Stripeを通じて世界の主要なクレジットカード・デビットカード（Visa、Mastercard、American Expressなど）に対応しています。安全で便利です。",
    "faq.label": "よくある質問",
    "faq.q1": "紫微斗数とは？",
    "faq.q2": "結果は正確ですか？",
    "faq.q3": "プライバシーはどのように守られますか？",
    "faq.q4": "対応している決済方法は？",
    "faq.title": "ご質問はありますか？お答えします",
    # features.*
    "features.career.desc": "官禄宮から仕事の方向性、昇進運、貴人運を読み解き、キャリアの正しい決断をサポート",
    "features.career.name": "仕事運",
    "features.cta": "<span data-i18n=\"features.cta\">詳細はこちら →</span>",
    "features.desc": "仕事や金運から恋愛・健康まで、紫微斗数が人生のあらゆる側面を読み解きます",
    "features.health.desc": "疾厄宮から健康状態を分析し、病気のリスクを予防し、養生の道を身につける",
    "features.health.name": "健康運",
    "features.label": "サービス内容",
    "features.love.desc": "夫妻宮から出会いや恋愛パターン、結婚の縁を詳解し、良縁のタイミングを掴む",
    "features.love.name": "恋愛運",
    "features.title": "全方位の運命鑑定",
    "features.wealth.desc": "財帛宮からお金の稼ぎ方を分析し、金運の浮き沈みを見極め、富の暗号を掴む",
    "features.wealth.name": "金運",
    # footer.*
    "footer.bottom": "© 2026 yourfate.xyz · 命理分析は参考情報です · 運命は自分で切り開くもの",
    "footer.brand": "☾ yourfate.xyz",
    "footer.chart": "オンライン命盤",
    "footer.desc": "紫微斗数オンライン命理解読サービス",
    "footer.faq": "よくある質問",
    "footer.home": "ホーム",
    "footer.pricing": "料金",
    "footer.services": "サービス内容",
    # form.*
    "form.date.label": "生年月日",
    "form.date.lunar": "🌙 旧暦",
    "form.date.solar": "☀️ 西暦",
    "form.desc": "出生情報を正確に入力すると、無料で紫微斗数命盤を確認できます",
    "form.gender.female": "👩 女性",
    "form.gender.label": "性別",
    "form.gender.male": "👨 男性",
    "form.hour.label": "出生時刻",
    "form.label": "オンライン命盤",
    "form.name.label": "お名前（任意）",
    "form.name.placeholder": "お名前を入力してください",
    "form.note": "命理分析は参考情報です · 運命は自分で切り開くもの",
    "form.submit": "命盤を作成",
    "form.title": "あなたの出生情報を入力",
    # header.*
    "header.cta": "今すぐ解読",
    "header.nav.chart": "オンライン命盤",
    "header.nav.faq": "よくある質問",
    "header.nav.how": "ご利用方法",
    "header.nav.pricing": "料金",
    "header.nav.services": "サービス内容",
    # hero.*
    "hero.badge": "⭐ 紫微斗数 · 地狱占卜师 · プライバシー保護",
    "hero.btn.primary": "🔮 今すぐ解読",
    "hero.btn.secondary": "サービスを見る",
    "hero.sub.line1": "伝統的な紫微斗数アルゴリズムによる正確な命盤作成と十二宮の詳解",
    "hero.sub.line2": "命盤の格局 · 大限運勢 · 四化飛星 · 総合鑑定",
    "hero.title.gold": "運勢を解読",
    "hero.title.line1": "千年の知恵で、",
    "hero.title.line2": "あなたの",
    # how.*
    "how.desc": "簡単3ステップでプロ級の紫微斗数命盤鑑定を",
    "how.label": "ご利用方法",
    "how.step1.desc": "生年月日・時刻・性別を入力。西暦と旧暦の両方の入力方式に対応",
    "how.step1.title": "出生情報を入力",
    "how.step2.desc": "十二宮の星の配置、四化飛星、大限運勢をシステムが自動計算し、専門の命盤を生成",
    "how.step2.title": "自動で命盤作成",
    "how.step3.desc": "十二宮の詳細鑑定、命盤の格局分析、大限運勢の推演で、人生の運勢を全面的に把握",
    "how.step3.title": "詳細鑑定",
    "how.title": "3ステップで運命の暗号を解読",
    # modal.*
    "modal.cancel": "今は不要",
    "modal.ok": "OK",
    # pay.*
    "pay.body.forever": "お支払い後、この命盤鑑定をいつでも閲覧できます",
    "pay.body.intro": "🔮 完全な命盤鑑定の内容：",
    "pay.body.item1": "✦ 十二宮の詳細鑑定",
    "pay.body.item2": "✦ 命盤の格局分析",
    "pay.body.item3": "✦ 大限運勢の鑑定",
    "pay.body.item4": "✦ 四化飛星の詳解",
    "pay.body.item5": "✦ 総合運勢アドバイス",
    "pay.body.price": "一回限りのお支払い ",
    "pay.btn": "💳 今すぐ支払う $9.99",
    "pay.btn.stripe": "💳 Stripeで支払う",
    "pay.btn.lianlian": "💱 LianLian Global（Alipay/WeChat/銀聯）",
    "pay.redirecting": "決済ページへ移動中...",
    "pay.title": "詳細鑑定をアンロック",
    # pricing.*
    "pricing.badge": "🌟 一番人気",
    "pricing.cta": "🔮 今すぐ始める",
    "pricing.feat1": "十二宮の詳細鑑定",
    "pricing.feat2": "命盤の格局分析",
    "pricing.feat3": "大限運勢の推演",
    "pricing.feat4": "四化飛星の詳解",
    "pricing.feat5": "総合運勢アドバイス",
    "pricing.label": "料金",
    "pricing.name": "詳細鑑定プラン",
    "pricing.period": "一回限りのお支払い · 永久閲覧",
    "pricing.title": "あなたに合うプランを選択",
    # report.*
    "report.advice": "命理分析は参考情報です。運命は自分の手にあります。紫微斗数が示すのは先天的な資質であり、後天的な努力・選択・環境も同様に重要です。命盤の吉星の強みを活かし、凶星の悪影響を和らげ、人生の試練に積極的に向き合いましょう。",
    "report.aux_hint": "。吉運と助力を高めます。",
    "report.aux_stars": "輔星：",
    "report.daxian_fmt": "、大限は",
    "report.empty_fallback": "この宮に主星はなく、向かいの宮を参照します。",
    "report.empty_ming": "命宮が空宮で、人生は環境の影響を大きく受け、順応性に富みます。向かいの宮（父母宮）の星を参照します。",
    "report.hua_prefix": "化",
    "report.ming_main": "宮、主星：",
    "report.ming_prefix": "命宮は",
    "report.sha_hint": " 凶星が照合し、人生に多くの試練があります。",
    "report.sha_hint2": "。挑戦と試練をもたらします。",
    "report.sha_stars": "凶星：",
    "report.shen_hint": "この宮は身宮で、後天的な発展に大きな影響を与えます。",
    "report.sihua_fmt": "四化：",
    "report.star_fallback": "が入り",
    "report.star_fallback2": "、",
    "report.star_fallback3": "に影響を与えます。",
    # result.*
    "result.label": "命盤の結果",
    "result.title": "あなたの紫微斗数命盤",
    # site.*
    "site.title": "紫微斗数 - 地狱占卜师",
    # stats.*
    "stats.privacy": "プライバシー保護",
    "stats.rating": "満足度",
    "stats.users": "利用者数",
    # testimonials.*
    "testimonials.1.author": "李さん",
    "testimonials.1.role": "IT関連会社員",
    "testimonials.1.text": "命盤の結果は非常に詳しく、十二宮の鑑定で自分自身を新たに理解できました。特に仕事運の鑑定は実際の状況と非常に一致していました。",
    "testimonials.2.author": "王さん",
    "testimonials.2.role": "教師",
    "testimonials.2.text": "夫妻宮の鑑定で恋愛への理解が深まりました。化忌の箇所はまさに努力が必要な部分でした。とても専門的な分析です！",
    "testimonials.3.author": "張さん",
    "testimonials.3.role": "起業家",
    "testimonials.3.text": "大限運勢の推演で将来の計画に方向性が見えました。格局分析の精度は非常に高く、友人にもおすすめしたいです。",
    "testimonials.label": "利用者の声",
    "testimonials.title": "みんな紫微斗数で人生を解読しています",
    # toast.*
    "toast.calc_failed": "命盤の作成に失敗しました。日付を確認してください",
    "toast.data_missing": "情報の読み込みに失敗しました。出生情報を再入力してください",
    "toast.data_restore": "データ復元に失敗しました。出生情報を再入力してください",
    "toast.info_missing": "情報が不足しています。命盤を作り直してください",
    "toast.network_error": "ネットワークエラーです。再試行してください",
    "toast.pay_success": "支払い完了！詳細鑑定を表示しています...",
    "toast.select_date": "生年月日を選択してください",
    "toast.stripe_config": "決済サービスが一時的に利用できません\\nStripeの設定を確認して再試行してください",
    "toast.lianlian_config": "LianLian決済サービスが一時的に利用できません\\nLianLianの設定を確認して再試行してください",
    "toast.verify_fail": "支払い確認に失敗しました。後でもう一度お試しいただくか、サポートにお問い合わせください",
    "toast.verify_network": "ネットワークエラーにより支払い状況を確認できません",
    "toast.year_range": "1900年〜2100年の範囲のみ対応しています",
    # hour.*
    "hour.0": "子の刻 (23:00-01:00)",
    "hour.1": "丑の刻 (01:00-03:00)",
    "hour.2": "寅の刻 (03:00-05:00)",
    "hour.3": "卯の刻 (05:00-07:00)",
    "hour.4": "辰の刻 (07:00-09:00)",
    "hour.5": "巳の刻 (09:00-11:00)",
    "hour.6": "午の刻 (11:00-13:00)",
    "hour.7": "未の刻 (13:00-15:00)",
    "hour.8": "申の刻 (15:00-17:00)",
    "hour.9": "酉の刻 (17:00-19:00)",
    "hour.10": "戌の刻 (19:00-21:00)",
    "hour.11": "亥の刻 (21:00-23:00)",
    # cat.career.*
    "cat.career.title": "仕事運 — 専門鑑定",
    "cat.career.intro": "十二宮のうち<strong>官禄宮</strong>（仕事宮）を中心に、命宮・財帛宮・遷移宮を組み合わせて、あなたの仕事運の流れを総合的に分析します。",
    "cat.career.serviceIntro": "詳細鑑定をご購入後、以下の内容を入手できます：",
    "cat.career.analyze.0.label": "命宮の主星",
    "cat.career.analyze.0.desc": "生まれ持った性格の特徴、向いている職業のタイプと仕事のスタイル",
    "cat.career.analyze.1.label": "官禄宮",
    "cat.career.analyze.1.desc": "仕事運の核心指標 — キャリアの方向性、昇進のタイミング、職場環境との相性",
    "cat.career.analyze.2.label": "財帛宮",
    "cat.career.analyze.2.desc": "収入源とお金の稼ぎ方、本業収入と副収入の運勢分析",
    "cat.career.analyze.3.label": "遷移宮",
    "cat.career.analyze.3.desc": "外部での発展機会、出張・転居運、貴人の助けと妨害者の予防",
    "cat.career.analyze.4.label": "四化飛星",
    "cat.career.analyze.4.desc": "化禄・化権・化科・化忌が仕事関連の宮に与える影響と対策",
    "cat.career.service.0": "官禄宮の星の組み合わせの詳細分析",
    "cat.career.service.1": "キャリアチェンジと昇進タイミングのアドバイス",
    "cat.career.service.2": "貴人と妨害者を見分けるガイド",
    "cat.career.service.3": "10年ごとの大限仕事運の推演",
    "cat.career.service.4": "向いている業界と起業タイミングの分析",
    # cat.love.*
    "cat.love.title": "恋愛運 — 専門鑑定",
    "cat.love.intro": "<strong>夫妻宮</strong>を中心に、命宮・福德宮・子女宮を組み合わせて、あなたの恋愛パターンと結婚の縁を深く読み解きます。",
    "cat.love.serviceIntro": "詳細鑑定をご購入後、以下の内容を入手できます：",
    "cat.love.analyze.0.label": "命宮の主星",
    "cat.love.analyze.0.desc": "生まれ持った恋愛の性質、恋愛スタイルとパートナーの好み",
    "cat.love.analyze.1.label": "夫妻宮",
    "cat.love.analyze.1.desc": "結婚運の核心指標 — 配偶者の特徴、結婚生活の質、関係の行方",
    "cat.love.analyze.2.label": "福德宮",
    "cat.love.analyze.2.desc": "心の奥の感情ニーズ、精神的な相性、幸せの源泉",
    "cat.love.analyze.3.label": "子女宮",
    "cat.love.analyze.3.desc": "出会い運の強弱、恋愛チャンスの多さ、子宝の縁",
    "cat.love.analyze.4.label": "四化飛星",
    "cat.love.analyze.4.desc": "化禄・化権・化科・化忌が恋愛関連の宮に与える具体的な影響",
    "cat.love.service.0": "夫妻宮の星の組み合わせの詳細分析",
    "cat.love.service.1": "出会い運と恋愛のタイミング分析",
    "cat.love.service.2": "結婚の相性とパートナー選びのアドバイス",
    "cat.love.service.3": "恋愛で注意すべき凶星の影響",
    "cat.love.service.4": "大限ごとの恋愛運の推演",
    # cat.wealth.*
    "cat.wealth.title": "金運 — 専門鑑定",
    "cat.wealth.intro": "<strong>財帛宮</strong>を中心に、命宮・田宅宮・福德宮を組み合わせて、あなたの富の暗号とお金の稼ぎ方を完全に解読します。",
    "cat.wealth.serviceIntro": "詳細鑑定をご購入後、以下の内容を入手できます：",
    "cat.wealth.analyze.0.label": "命宮の主星",
    "cat.wealth.analyze.0.desc": "生まれ持った金運の素質、お金の考え方と消費習慣",
    "cat.wealth.analyze.1.label": "財帛宮",
    "cat.wealth.analyze.1.desc": "金運の核心指標 — 収入源、お金の稼ぎ方、資産形成力",
    "cat.wealth.analyze.2.label": "田宅宮",
    "cat.wealth.analyze.2.desc": "不動産運、家庭の資産、財産の保存と価値維持の力",
    "cat.wealth.analyze.3.label": "福德宮",
    "cat.wealth.analyze.3.desc": "副収入運、投資運、精神的な満足と物質的な豊かさのバランス",
    "cat.wealth.analyze.4.label": "四化飛星",
    "cat.wealth.analyze.4.desc": "化禄・化権・化科・化忌が金運関連の宮に与える影響",
    "cat.wealth.service.0": "財帛宮の星の組み合わせの詳細分析",
    "cat.wealth.service.1": "本業収入と副収入の運勢の詳細",
    "cat.wealth.service.2": "投資・資産運用のタイミングと方向性のアドバイス",
    "cat.wealth.service.3": "お金のトラブルのリスク警告と対策",
    "cat.wealth.service.4": "大限ごとの金運の推移の推演",
    # cat.health.*
    "cat.health.title": "健康運 — 専門鑑定",
    "cat.health.intro": "<strong>疾厄宮</strong>を中心に、命宮・福德宮・遷移宮を組み合わせて、あなたの健康状態と養生の方向性を総合的に分析します。",
    "cat.health.serviceIntro": "詳細鑑定をご購入後、以下の内容を入手できます：",
    "cat.health.analyze.0.label": "命宮の主星",
    "cat.health.analyze.0.desc": "生まれ持った体質の強弱、身体エネルギーの基本盤と抵抗力",
    "cat.health.analyze.1.label": "疾厄宮",
    "cat.health.analyze.1.desc": "健康運の核心指標 — かかりやすい病気、事故リスク、回復力",
    "cat.health.analyze.2.label": "福德宮",
    "cat.health.analyze.2.desc": "心の健康と感情の状態、ストレス対応力、養生への関心の方向",
    "cat.health.analyze.3.label": "遷移宮",
    "cat.health.analyze.3.desc": "外出時の安全、交通事故リスク、環境の変化への適応力",
    "cat.health.analyze.4.label": "四化飛星",
    "cat.health.analyze.4.desc": "化禄・化権・化科・化忌が疾厄宮に与える影響、病気の警告と対策",
    "cat.health.service.0": "疾厄宮の星の組み合わせの詳細分析",
    "cat.health.service.1": "生まれ持った体質の評価とかかりやすい病気の警告",
    "cat.health.service.2": "年齢別の健康運の推演",
    "cat.health.service.3": "養生の方向性と運動のアドバイス",
    "cat.health.service.4": "凶星が疾厄宮に入る際の対策ガイド",
}

# ── Apply ──────────────────────────────────────────────────────
html = io.open(SRC, encoding="utf-8").read()

# 1) verify every key exists and dict covers all keys
pat = re.compile(r"^I18N\.data\.zh\['([^']+)'\] = ")
existing = set()
for line in html.splitlines():
    m = pat.match(line.strip())
    if m:
        existing.add(m.group(1))

missing_in_file = set(JA) - existing
missing_in_dict = existing - set(JA)
if missing_in_file:
    print("ERROR: keys not found in index.html:", missing_in_file)
    sys.exit(1)
if missing_in_dict:
    print("ERROR: existing keys without ja translation:", missing_in_dict)
    sys.exit(1)

# 2) build ja lines
lines = []
for key in sorted(JA.keys(), key=lambda k: html.index("I18N.data.zh['{}']".format(k))):
    # only escape single quotes — backslash-n stays as the JS \n escape
    val = JA[key].replace("'", "\\'")
    lines.append("I18N.data.ja['{}'] = '{}';".format(key, val))

# 3) insert after the LAST I18N.data line
last_data_line = None
for i, line in enumerate(html.splitlines(True)):
    if line.strip().startswith("I18N.data."):
        last_data_line = i
assert last_data_line is not None, "no I18N.data lines found"

parts = html.splitlines(True)
insert_at = last_data_line + 1
parts[insert_at:insert_at] = ["\n// ── Japanese (ja) ─────────────────────────────────────────────\n"] + [l + "\n" for l in lines]
html = "".join(parts)

# 4) register ja in the data object
old = "data: { zh: {}, en: {}, ar: {} },"
new = "data: { zh: {}, en: {}, ar: {}, ja: {} },"
assert html.count(old) == 1, "data object line not found"
html = html.replace(old, new)

io.open(SRC, "w", encoding="utf-8", newline="\n").write(html)
print("inserted {} ja translations".format(len(lines)))
