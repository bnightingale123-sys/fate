# -*- coding: utf-8 -*-
"""Inject high-converting CRO logic, i18n dictionaries, and interactive features into index.html."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(ROOT, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# ----------------------------------------------------------------------
# 1. Add I18N entries for CRO (Hook, Countdown, Trust, Blur teaser, Policy)
# ----------------------------------------------------------------------
i18n_addition = """
// ============================================================
// CRO & Trust Extensions (ja, zh, en, ar)
// ============================================================
(function() {
  var ext = {
    ja: {
      'hook.title': '✦ 命盤の核心機密・運勢転換点',
      'hook.alert': '⚠ 運命の転換期を検知',
      'hook.intro_p1': '命宮主星に卓越した直感と潜在能力が秘められています。しかし、化忌星の巡りにより、特定の人生領域で突然の停滞や試練を経験しやすい宿命の波動が表れています。',
      'hook.lock1': '運命の相手（正縁）との出会い期・結婚の暗礁',
      'hook.lock2': '一生の財運爆発期・金運破耗を回避する秘法',
      'hook.lock3': '2026年 流年吉凶月別注意報と貴人方位',
      'hook.btn': '🔮 完全詳細解読レポートを解放する（新客限定 $9.99）',
      'hook.proof': '★★★★★ 4.9/5 (12,800人以上が鑑定済み) · 256-Bit SSL暗号化 · 即時アクセス',
      'pay.timer': '🔥 初回限定特別価格 終了まであと ',
      'pay.orig_price': '$29.99',
      'pay.sale_price': '$9.99 USD',
      'pay.benefit1': '十二宮全方位の精密深層鑑定（仕事・恋愛・金運・健康）',
      'pay.benefit2': '一生の大限運勢推演（10年ごとの運気の波と転換期）',
      'pay.benefit3': '2026年 流年吉凶と避けるべき落とし穴の具体策',
      'pay.benefit4': '四化飛星（化禄・権・科・忌）による開運秘法',
      'pay.benefit5': '永久保存・いつでも何度でもオンライン閲覧可能',
      'pay.trust_stripe': 'Stripe公式認定 安全決済',
      'pay.trust_ssl': '256-bit 銀行水準暗号化',
      'pay.trust_guarantee': '満足保証・即時データ閲覧',
      'blur.badge_title': '深層運勢推演レポートが封印されています',
      'blur.badge_desc': '大限10年ごとの運気推移、2026年流年の月別注意報、財運・正縁の具体的時期などの詳細解読は完全版でのみ閲覧できます。',
      'blur.unlock_btn': '🔮 今すぐ完全レポートを解放する ($9.99 USD)',
      'footer.privacy': 'プライバシーポリシー',
      'footer.terms': '利用規約',
      'footer.contact': 'お問い合わせ',
      'modal.privacy_title': 'プライバシーポリシー（個人情報保護方針）',
      'modal.privacy_body': '当サイト「地獄占い師（yourfate.xyz）」はお客様のプライバシーを最優先に保護します。\\n\\n1. 生年月日・出生時間などの情報は命盤の瞬時計算にのみ使用され、当社のサーバーに永続保存・第三者提供されることは一切ありません。\\n2. お支払い情報は国際最高基準PCI-DSS準拠の決済代行業者「Stripe」により安全に処理され、当サイトがクレジットカード番号を保持することはありません。\\n3. 通信はすべて256-Bit SSL/TLSにより暗号化されています。\\n\\nご不明な点は support@yourfate.xyz までお問い合わせください。',
      'modal.terms_title': '利用規約',
      'modal.terms_body': '当サイトが提供する紫微斗数オンライン鑑定サービスのご利用規約です。\\n\\n1. 本サービスは伝統的な紫微斗数アルゴリズムに基づく運勢分析およびエンターテインメント・参考情報を提供するものであり、医学的・法的・投資的な助言を行うものではありません。\\n2. デジタルコンテンツの性質上、決済完了後即座にレポートが解放されます。システム障害等でレポートが閲覧できない場合は、support@yourfate.xyz までご連絡いただければ迅速に再発行・対応いたします。'
    },
    zh: {
      'hook.title': '✦ 命盘核心玄机与运势转折点',
      'hook.alert': '⚠ 检测到关键大限转折期',
      'hook.intro_p1': '命宫主星蕴含卓越直觉与破局潜能。然而受到化忌飞星与煞星引动，在特定人生阶段极易遭遇事业瓶颈、财库破耗或感情波折，需及时把握生克制化之机。',
      'hook.lock1': '正缘桃花出现时机与婚恋暗礁破解',
      'hook.lock2': '一生财禄爆发年份与破耗规避秘法',
      'hook.lock3': '2026年 流年月度吉凶避坑与贵人方位',
      'hook.btn': '🔮 解锁完整 8 宫深度大限推演报告（新客特惠 $9.99）',
      'hook.proof': '★★★★★ 4.9/5 (已为 12,800+ 位缘主完成推演) · 256位SSL加密 · 即时解锁',
      'pay.timer': '🔥 新客首单特惠 倒计时 ',
      'pay.orig_price': '$29.99',
      'pay.sale_price': '$9.99 USD',
      'pay.benefit1': '十二宫全方位深度批断（命宫、财帛、官禄、夫妻等）',
      'pay.benefit2': '一生大限运势推演（十年一运吉凶起伏全貌）',
      'pay.benefit3': '2026 流年避坑防破耗与贵人吉方指南',
      'pay.benefit4': '四化飞星吉凶破解与趋吉避凶良方',
      'pay.benefit5': '永久保存，专属链接随时随地在线回看',
      'pay.trust_stripe': 'Stripe 官方认证安全支付',
      'pay.trust_ssl': '256位 银行级安全加密',
      'pay.trust_guarantee': '满意保证 · 即刻解锁交付',
      'blur.badge_title': '核心流年大限与解灾秘法已封印',
      'blur.badge_desc': '完整报告包含一生十年大限运势走势、2026流年月度吉凶、财帛与正缘具体应期，解锁后即刻生成完整批断。',
      'blur.unlock_btn': '🔮 立即解锁完整深度解盘报告 ($9.99 USD)',
      'footer.privacy': '隐私政策',
      'footer.terms': '服务条款',
      'footer.contact': '联系客服',
      'modal.privacy_title': '隐私保护政策',
      'modal.privacy_body': 'yourfate.xyz 严格遵守国际数据隐私规范（GDPR）。\\n\\n1. 您输入的出生生辰数据仅用于瞬时排盘算法运算，平台不会永久存储或向第三方出售您的个人隐私。\\n2. 所有支付由国际一线支付机构 Stripe 采用银行级安全通道处理，平台不接触也不记录您的信用卡信息。\\n3. 全站采用 256-bit SSL 高强度加密传输。\\n\\n如有疑问请联系：support@yourfate.xyz',
      'modal.terms_title': '服务条款',
      'modal.terms_body': '1. 本平台紫微斗数排盘及解盘服务基于中国传统命理古法推演，分析结果仅供个人决策参考与文化体验，不构成医疗、法律或投资承诺。\\n2. 详细解盘为数字化虚拟报告，支付成功后系统即时自动解锁交付。如遇网络异常未正常解锁，凭支付订单号联系客服 support@yourfate.xyz 将在24小时内为您人工复核开通。'
    },
    en: {
      'hook.title': '✦ Core Destiny Secrets & Turning Points',
      'hook.alert': '⚠ Major Turning Cycle Detected',
      'hook.intro_p1': 'Your life palace carries powerful intuition and breakthrough potential. However, influenced by Hua Ji (Obstacle Star), certain life phases are prone to sudden career stagnation, financial leaks, or emotional trials.',
      'hook.lock1': 'Soulmate Timing & Marriage Obstacle Analysis',
      'hook.lock2': 'Peak Wealth Window & Financial Risk Avoidance',
      'hook.lock3': '2026 Monthly Caution & Benefactor Directions',
      'hook.btn': '🔮 Unlock Full 8-Page In-Depth Destiny Reading ($9.99)',
      'hook.proof': '★★★★★ 4.9/5 (12,800+ Charts Calculated) · 256-Bit SSL Encrypted · Instant Access',
      'pay.timer': '🔥 Limited First-Visit Offer expires in ',
      'pay.orig_price': '$29.99',
      'pay.sale_price': '$9.99 USD',
      'pay.benefit1': 'Full 12-Palace In-Depth Analysis (Career, Wealth, Love, Health)',
      'pay.benefit2': 'Lifetime 10-Year Major Cycles (Timeline of turning points)',
      'pay.benefit3': '2026 Annual & Monthly Risk Avoidance & Lucky Directions',
      'pay.benefit4': 'Four Transformations (Lu, Quan, Ke, Ji) Remedy Strategies',
      'pay.benefit5': 'Lifetime Access — Revisit your reading anytime online',
      'pay.trust_stripe': 'Stripe Verified Secure Checkout',
      'pay.trust_ssl': '256-Bit Bank-Level Encryption',
      'pay.trust_guarantee': '100% Satisfaction · Instant Access',
      'blur.badge_title': 'In-Depth Timeline & Remedies Are Locked',
      'blur.badge_desc': 'Your complete reading includes 10-year major cycle transitions, 2026 monthly alerts, and specific financial/relationship windows.',
      'blur.unlock_btn': '🔮 Unlock Full Reading Now ($9.99 USD)',
      'footer.privacy': 'Privacy Policy',
      'footer.terms': 'Terms of Service',
      'footer.contact': 'Support',
      'modal.privacy_title': 'Privacy Policy',
      'modal.privacy_body': 'yourfate.xyz strictly protects your personal privacy.\\n\\n1. Your birth details are used solely for real-time astronomical calculation and are never permanently stored or shared.\\n2. Payments are securely processed via Stripe (PCI-DSS Level 1 compliant). We never see or store your credit card information.\\n3. All data transmission is encrypted via 256-Bit SSL.\\n\\nContact: support@yourfate.xyz',
      'modal.terms_title': 'Terms of Service',
      'modal.terms_body': '1. This service provides traditional Zi Wei Dou Shu astrological readings for personal insight and entertainment. It does not constitute medical, legal, or investment advice.\\n2. Digital readings are delivered instantly upon successful payment. For any inquiries, reach us at support@yourfate.xyz.'
    },
    ar: {
      'hook.title': '✦ أسرار القدر ونقاط التحول الكبرى',
      'hook.alert': '⚠ تم رصد دورة تحول مصيرية',
      'hook.intro_p1': 'يحمل قصر حياتك حدساً قوياً وطاقة كبرى. ومع ذلك، تشير حركة النجوم إلى وجود تحديات في مجالات معينة تتطلب الحكمة والوقاية.',
      'hook.lock1': 'توقيت شريك الحياة وعقبات الزواج وتجاوزها',
      'hook.lock2': 'فترة ذروة الثروة وتجنب الخسائر المالية',
      'hook.lock3': 'تحذيرات عام 2026 الشهرية واتجاهات الدعم',
      'hook.btn': '🔮 فتح التقرير المتعمق المكون من 8 صفحات ($9.99)',
      'hook.proof': '★★★★★ 4.9/5 (أكثر من 12,800 قراءة) · تشفير 256-Bit SSL · وصول فوري',
      'pay.timer': '🔥 عرض الزيارة الأولى ينتهي خلال ',
      'pay.orig_price': '$29.99',
      'pay.sale_price': '$9.99 USD',
      'pay.benefit1': 'تحليل شامل لجميع القصور الـ 12 (العمل، المال، الحب، الصحة)',
      'pay.benefit2': 'استشراف دورات الحياة الكبرى كل 10 سنوات',
      'pay.benefit3': 'توجيهات الحذر لعام 2026 واتجاهات الحظ',
      'pay.benefit4': 'حلول التحولات الأربعة وطرق فتح مسارات الوفرة',
      'pay.benefit5': 'حفظ دائم وإمكانية الرجوع للتقرير في أي وقت',
      'pay.trust_stripe': 'دفع آمن ومعتمد عبر Stripe',
      'pay.trust_ssl': 'تشفير مصرفي 256-Bit آمن',
      'pay.trust_guarantee': 'ضمان الرضا وتسليم فوري',
      'blur.badge_title': 'التحليلات العميقة والتوقعات محجوبة',
      'blur.badge_desc': 'يتضمن التقرير الكامل دورات السنوات العشر وتوقعات 2026 الشهرية والمواعيد المحددة للثروة والعلاقات.',
      'blur.unlock_btn': '🔮 افتح التقرير الكامل الآن ($9.99 USD)',
      'footer.privacy': 'سياسة الخصوصية',
      'footer.terms': 'شروط الخدمة',
      'footer.contact': 'الدعم الفني',
      'modal.privacy_title': 'سياسة الخصوصية',
      'modal.privacy_body': 'نحن نحمي خصوصيتك بصرامة. بيانات ميلادك تُستخدم فقط للحساب الفلكي الفوري ولا يتم تخزينها. تتم جميع المدفوعات بأمان عبر Stripe بتشفير 256-Bit.',
      'modal.terms_title': 'شروط الخدمة',
      'modal.terms_body': 'التقرير متاح فور إتمام الدفع. للاستفسارات تواصل مع support@yourfate.xyz.'
    }
  };

  for (var lang in ext) {
    if (!I18N.data[lang]) I18N.data[lang] = {};
    for (var k in ext[lang]) {
      I18N.data[lang][k] = ext[lang][k];
    }
  }
})();
"""

if "CRO & Trust Extensions" not in code:
    code = code.replace("var App = (function() {", i18n_addition + "\nvar App = (function() {\n", 1)

# ----------------------------------------------------------------------
# 2. Add Countdown Timer helper inside App module
# ----------------------------------------------------------------------
countdown_helper = """
  // === Countdown Timer for CRO ===
  function getRemainingTime() {
    var key = 'zwei_promo_expire';
    var now = Date.now();
    var exp = sessionStorage.getItem(key);
    if (!exp || parseInt(exp) < now) {
      exp = now + 15 * 60 * 1000; // 15 mins
      sessionStorage.setItem(key, exp);
    }
    var diff = Math.max(0, Math.floor((parseInt(exp) - now) / 1000));
    var m = Math.floor(diff / 60);
    var s = diff % 60;
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }

  function startCountdownInterval() {
    setInterval(function() {
      var str = getRemainingTime();
      document.querySelectorAll('.pay-timer-num').forEach(function(el) {
        el.textContent = str;
      });
    }, 1000);
  }
  startCountdownInterval();

  function showPrivacyModal() {
    showModal(I18N.t('modal.privacy_title'), I18N.t('modal.privacy_body'));
  }

  function showTermsModal() {
    showModal(I18N.t('modal.terms_title'), I18N.t('modal.terms_body'));
  }
"""

if "function getRemainingTime()" not in code:
    code = code.replace("var App = (function() {", "var App = (function() {\n" + countdown_helper, 1)

# ----------------------------------------------------------------------
# 3. Update App.renderChart to include the High-Converting Hook Card
# ----------------------------------------------------------------------
old_render_chart_actions = """      '<div class="actions">'+
        '<button class="btn-outline" id="btnDetail" onclick="App.goToDetail()"><span id="btnDetailText">查看详细解盘</span></button>'+
        '<button class="btn-secondary" onclick="App.goBack()">重新输入</button>'+
      '</div>';"""

new_render_chart_actions = """      // CRO Hook Card for unpaid users
      (!state.isPaid ?
        '<div class="hook-card">'+
          '<div class="hook-header">'+
            '<div class="hook-title">'+I18N.t('hook.title')+'</div>'+
            '<span class="hook-alert-tag">'+I18N.t('hook.alert')+'</span>'+
          '</div>'+
          '<div class="hook-analysis-box">'+
            I18N.t('hook.intro_p1')+
          '</div>'+
          '<div class="hook-locked-items">'+
            '<div class="hook-locked-item"><span>✦ '+I18N.t('hook.lock1')+'</span><span class="lock-icon">🔒 封印中</span></div>'+
            '<div class="hook-locked-item"><span>✦ '+I18N.t('hook.lock2')+'</span><span class="lock-icon">🔒 封印中</span></div>'+
            '<div class="hook-locked-item"><span>✦ '+I18N.t('hook.lock3')+'</span><span class="lock-icon">🔒 封印中</span></div>'+
          '</div>'+
          '<button class="btn-unlock-gold" onclick="App.goToDetail()">'+
            I18N.t('hook.btn')+
          '</button>'+
          '<div class="hook-social-proof">'+I18N.t('hook.proof')+'</div>'+
        '</div>' : '')+

      '<div class="actions" style="margin-top:16px;">'+
        (state.isPaid ? '<button class="btn-outline unlocked" id="btnDetail" onclick="App.goToDetail()"><span id="btnDetailText">'+I18N.t('chart.btn_unlocked')+'</span></button>' : '')+
        '<button class="btn-secondary" onclick="App.goBack()">'+I18N.t('chart.btn_reset')+'</button>'+
      '</div>';"""

if old_render_chart_actions in code:
    code = code.replace(old_render_chart_actions, new_render_chart_actions, 1)

# ----------------------------------------------------------------------
# 4. Update App.renderDetail to include Blur Teaser when !state.isPaid
# ----------------------------------------------------------------------
old_render_detail_end = """      '<div class="section">'+
        '<span class="section-title">四化总结</span>'+
        '<div class="text-card"><span class="body-text">'+report.huaSummary+'</span></div>'+
      '</div>'+

      '<div class="section">'+
        '<span class="section-title">温馨提示</span>'+
        '<div class="advice-card"><span class="advice-text">'+report.advice+'</span></div>'+
      '</div>'+

      '<button class="btn-back" onclick="App.backToChart()">返回命盘</button>';"""

new_render_detail_end = """      (!state.isPaid ?
        '<div class="blur-locked-wrapper">'+
          '<div class="blur-locked-content">'+
            '<div class="section"><span class="section-title">十二宫后半部详批</span><div class="palace-list">'+palacesHtml+'</div></div>'+
            '<div class="section"><span class="section-title">大限十年运程</span><div class="dx-list">'+dxHtml+'</div></div>'+
            '<div class="section"><span class="section-title">四化终极避凶</span><div class="text-card"><span class="body-text">'+report.huaSummary+'</span></div></div>'+
          '</div>'+
          '<div class="blur-overlay-banner">'+
            '<div class="blur-lock-badge">🔒</div>'+
            '<div class="blur-lock-title">'+I18N.t('blur.badge_title')+'</div>'+
            '<div class="blur-lock-desc">'+I18N.t('blur.badge_desc')+'</div>'+
            '<div class="pay-timer-badge"><span>'+I18N.t('pay.timer')+'</span><span class="pay-timer-num">'+getRemainingTime()+'</span></div>'+
            '<div class="modal-price-tag">'+
              '<span class="modal-price-curr">$9.99 USD</span>'+
              '<span class="modal-price-orig">$29.99</span>'+
            '</div>'+
            '<button class="btn-unlock-gold" style="max-width:380px;" onclick="App.showPaymentModal()">'+
              I18N.t('blur.unlock_btn')+
            '</button>'+
            '<div class="hook-social-proof" style="margin-top:12px;">'+I18N.t('hook.proof')+'</div>'+
          '</div>'+
        '</div>'
        :
        ('<div class="section">'+
          '<span class="section-title">四化总结</span>'+
          '<div class="text-card"><span class="body-text">'+report.huaSummary+'</span></div>'+
        '</div>'+
        '<div class="section">'+
          '<span class="section-title">温馨提示</span>'+
          '<div class="advice-card"><span class="advice-text">'+report.advice+'</span></div>'+
        '</div>')
      )+

      '<button class="btn-back" style="margin-top:24px;" onclick="App.backToChart()">'+I18N.t('chart.btn_reset')+'</button>';"""

if old_render_detail_end in code:
    code = code.replace(old_render_detail_end, new_render_detail_end, 1)

# ----------------------------------------------------------------------
# 5. Update App.goToDetail to show blur teaser directly or payment dialog
# ----------------------------------------------------------------------
old_go_to_detail = """  function goToDetail() {
    var cd = state.chartData;
    if (!cd) return;

    // Already paid — show detail directly
    if (state.isPaid) {
      var report = state.report || Interpretations.generateReport(cd);
      state.report = report;
      document.getElementById('detailContainer').innerHTML = renderDetail(cd, report);
      showView('view-detail');
      return;
    }

    // Not paid — show payment modal
    showPaymentModal();
  }"""

new_go_to_detail = """  function goToDetail() {
    var cd = state.chartData;
    if (!cd) return;

    var report = state.report || Interpretations.generateReport(cd);
    state.report = report;
    document.getElementById('detailContainer').innerHTML = renderDetail(cd, report);
    showView('view-detail');

    if (!state.isPaid) {
      // Also show modal so user has instant direct checkout
      setTimeout(function() { showPaymentModal(); }, 600);
    }
  }"""

if old_go_to_detail in code:
    code = code.replace(old_go_to_detail, new_go_to_detail, 1)

# ----------------------------------------------------------------------
# 6. Update App.showPaymentDialog with High-Converting Trust & Cards
# ----------------------------------------------------------------------
old_show_payment_dialog = """  function showPaymentDialog(title, body) {
    var overlay = document.getElementById('modalOverlay');
    document.getElementById('modalTitle').textContent = title;

    var bodyEl = document.getElementById('modalBody');
    bodyEl.style.whiteSpace = 'normal';
    bodyEl.innerHTML =
      '<div style="font-size:0.88rem;color:#c0b8a8;line-height:1.8;white-space:pre-line;margin-bottom:20px;">'+body+'</div>'+
      '<button class="modal-btn" id="btnStripePay" style="margin-bottom:8px;" onclick="App.initiateStripeCheckout()">'+
        I18N.t('pay.btn.stripe')+
      '</button>';

    // Hide the default modal button (we use inline buttons instead)
    var defaultOkBtn = document.getElementById('btnModalOk');
    if (defaultOkBtn) { defaultOkBtn.style.display = 'none'; }

    // Show cancel button
    var cancelBtn = document.querySelector('.modal-btn-cancel');
    if (cancelBtn) cancelBtn.style.display = '';

    overlay.classList.remove('hidden');
  }"""

new_show_payment_dialog = """  function showPaymentDialog(title, body) {
    var overlay = document.getElementById('modalOverlay');
    document.getElementById('modalTitle').textContent = title;

    var timerStr = getRemainingTime();
    var bodyEl = document.getElementById('modalBody');
    bodyEl.style.whiteSpace = 'normal';

    var html = ''+
      '<div style="text-align:center;">'+
        '<div class="pay-timer-badge"><span>'+I18N.t('pay.timer')+'</span><span class="pay-timer-num">'+timerStr+'</span></div>'+
        '<div class="modal-price-tag">'+
          '<span class="modal-price-curr">'+I18N.t('pay.sale_price')+'</span>'+
          '<span class="modal-price-orig">'+I18N.t('pay.orig_price')+'</span>'+
        '</div>'+
      '</div>'+
      '<ul class="pay-features-list">'+
        '<li><span class="chk">✓</span><span>'+I18N.t('pay.benefit1')+'</span></li>'+
        '<li><span class="chk">✓</span><span>'+I18N.t('pay.benefit2')+'</span></li>'+
        '<li><span class="chk">✓</span><span>'+I18N.t('pay.benefit3')+'</span></li>'+
        '<li><span class="chk">✓</span><span>'+I18N.t('pay.benefit4')+'</span></li>'+
        '<li><span class="chk">✓</span><span>'+I18N.t('pay.benefit5')+'</span></li>'+
      '</ul>'+
      '<button class="btn-unlock-gold" id="btnStripePay" style="margin-bottom:10px;" onclick="App.initiateStripeCheckout()">'+
        I18N.t('pay.btn.stripe')+
      '</button>'+
      '<div class="card-logos">'+
        '<span class="card-badge">VISA</span>'+
        '<span class="card-badge">Mastercard</span>'+
        '<span class="card-badge">AMEX</span>'+
        '<span class="card-badge">JCB</span>'+
        '<span class="card-badge">Apple Pay</span>'+
        '<span class="card-badge">Google Pay</span>'+
      '</div>'+
      '<div class="modal-trust-row">'+
        '<div class="modal-trust-item"><span class="trust-dot">●</span><span>'+I18N.t('pay.trust_stripe')+'</span></div>'+
        '<div class="modal-trust-item"><span class="trust-dot">●</span><span>'+I18N.t('pay.trust_ssl')+'</span></div>'+
        '<div class="modal-trust-item"><span class="trust-dot">●</span><span>'+I18N.t('pay.trust_guarantee')+'</span></div>'+
      '</div>';

    bodyEl.innerHTML = html;

    var defaultOkBtn = document.getElementById('btnModalOk');
    if (defaultOkBtn) { defaultOkBtn.style.display = 'none'; }

    var cancelBtn = document.querySelector('.modal-btn-cancel');
    if (cancelBtn) cancelBtn.style.display = '';

    overlay.classList.remove('hidden');
  }"""

if old_show_payment_dialog in code:
    code = code.replace(old_show_payment_dialog, new_show_payment_dialog, 1)

# ----------------------------------------------------------------------
# 7. Expose showPrivacyModal and showTermsModal in App return object
# ----------------------------------------------------------------------
old_app_return = """    initiateStripeCheckout: initiateStripeCheckout,
    initiateLianlianCheckout: initiateLianlianCheckout,"""

new_app_return = """    initiateStripeCheckout: initiateStripeCheckout,
    initiateLianlianCheckout: initiateLianlianCheckout,
    showPrivacyModal: showPrivacyModal,
    showTermsModal: showTermsModal,
    showPaymentModal: showPaymentModal,"""

if old_app_return in code:
    code = code.replace(old_app_return, new_app_return, 1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("CRO enhancements injected into index.html successfully!")
