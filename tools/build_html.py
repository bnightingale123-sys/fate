"""Build the new index.html by replacing CSS and body HTML, keeping all JS intact."""
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    old = f.read()

# Find boundaries
style_start = old.find('<style>')
style_end = old.find('</style>') + len('</style>')
body_tag = old.find('<body>')
body_tag_end = old.find('>', body_tag) + 1
first_script = old.find('<script>', body_tag_end)

# New CSS (complete redesign matching the reference)
new_css = '''<style>
/* ===== Reset & Base ===== */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;scroll-behavior:smooth}
body{
  font-family:-apple-system,'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif;
  background:#0a0a1a;color:#e0d8c8;-webkit-font-smoothing:antialiased;line-height:1.6
}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:#0a0a1a}
::-webkit-scrollbar-thumb{background:#3a3a5a;border-radius:3px}
img{max-width:100%;height:auto}
a{color:inherit;text-decoration:none}
.container{max-width:1200px;margin:0 auto;padding:0 24px}

/* ===== Header ===== */
.site-header{
  position:sticky;top:0;z-index:100;
  background:#2D1B4E;color:#fff;
  padding:16px 0;box-shadow:0 4px 20px rgba(0,0,0,0.3)
}
.header-inner{display:flex;align-items:center;justify-content:space-between}
.header-logo{display:flex;align-items:center;gap:10px;font-size:1.25rem;font-weight:bold}
.header-logo .icon{color:#D4AF37;font-size:1.5rem}
.header-logo span{color:#D4AF37}
.header-nav{display:flex;align-items:center;gap:32px;font-size:0.9rem}
.header-nav a{transition:color 0.2s;color:#c0b8d0}
.header-nav a:hover{color:#D4AF37}
.header-cta{
  background:linear-gradient(135deg,#D4AF37,#C49F27);color:#1a1a2e;
  padding:10px 22px;border-radius:25px;font-weight:bold;font-size:0.85rem;
  transition:opacity 0.2s,transform 0.2s;border:none;cursor:pointer
}
.header-cta:hover{opacity:0.9;transform:translateY(-1px)}
.mobile-menu-btn{display:none;background:none;border:none;color:#fff;font-size:1.5rem;cursor:pointer}
@media(max-width:768px){
  .header-nav{display:none}
  .mobile-menu-btn{display:block}
}

/* ===== Hero ===== */
.hero-section{
  position:relative;min-height:85vh;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#1a1035 0%,#0d1b3e 40%,#1a0a2e 100%);
  overflow:hidden
}
.hero-bg{
  position:absolute;inset:0;opacity:0.15;
  background:
    radial-gradient(ellipse at 20% 50%,#D4AF37 0%,transparent 50%),
    radial-gradient(ellipse at 80% 50%,#6b4fa0 0%,transparent 50%)
}
.hero-content{position:relative;z-index:2;text-align:center;max-width:800px;padding:0 24px}
.hero-badge{
  display:inline-block;background:rgba(212,175,55,0.15);color:#D4AF37;
  padding:6px 20px;border-radius:20px;font-size:0.85rem;margin-bottom:24px;
  border:1px solid rgba(212,175,55,0.3)
}
.hero-title{font-size:2.8rem;font-weight:bold;color:#fff;line-height:1.25;margin-bottom:20px}
.hero-title .gold{color:#D4AF37}
.hero-sub{font-size:1.15rem;color:#a098b8;margin-bottom:36px;line-height:1.7}
.hero-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
.btn-gold{
  background:linear-gradient(135deg,#D4AF37,#C49F27);color:#1a1a2e;
  padding:14px 36px;border-radius:30px;font-weight:bold;font-size:1rem;
  transition:all 0.3s;display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer
}
.btn-gold:hover{opacity:0.9;transform:translateY(-2px);box-shadow:0 8px 24px rgba(212,175,55,0.3)}
.btn-outline-light{
  background:transparent;color:#D4AF37;border:2px solid #D4AF37;
  padding:14px 36px;border-radius:30px;font-weight:bold;font-size:1rem;
  transition:all 0.3s;cursor:pointer
}
.btn-outline-light:hover{background:rgba(212,175,55,0.1);transform:translateY(-2px)}
.hero-scroll{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);animation:bounce 2s infinite}
.hero-scroll span{font-size:1.5rem;color:#D4AF37}
@keyframes bounce{
  0%,100%{transform:translateX(-50%) translateY(0)}
  50%{transform:translateX(-50%) translateY(-10px)}
}
@media(max-width:768px){
  .hero-title{font-size:1.8rem}
  .hero-sub{font-size:1rem}
  .hero-section{min-height:75vh}
}

/* ===== Sections ===== */
.section{padding:80px 0}
.section-header{text-align:center;margin-bottom:56px}
.section-label{
  display:inline-block;color:#D4AF37;font-size:0.85rem;font-weight:bold;
  text-transform:uppercase;letter-spacing:2px;margin-bottom:12px
}
.section-title{font-size:2rem;font-weight:bold;color:#fff;margin-bottom:16px}
.section-desc{font-size:1rem;color:#9088a8;max-width:600px;margin:0 auto;line-height:1.7}
@media(max-width:768px){.section{padding:56px 0}.section-title{font-size:1.5rem}}

/* ===== Features ===== */
.features-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.feature-card{
  background:#1A1A2E;border-radius:16px;padding:32px 24px;text-align:center;
  border:1px solid #2a2a4a;transition:all 0.3s;cursor:default
}
.feature-card:hover{border-color:#D4AF37;transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,0.3)}
.feature-icon{font-size:2.5rem;margin-bottom:16px}
.feature-name{font-size:1.1rem;font-weight:bold;color:#D4AF37;margin-bottom:8px}
.feature-desc{font-size:0.85rem;color:#9088a8;line-height:1.6}
@media(max-width:768px){.features-grid{grid-template-columns:1fr 1fr;gap:16px}}
@media(max-width:480px){.features-grid{grid-template-columns:1fr}}

/* ===== How It Works ===== */
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.step-card{text-align:center;position:relative}
.step-num{
  width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,#D4AF37,#C49F27);
  color:#1a1a2e;font-size:1.5rem;font-weight:bold;
  display:flex;align-items:center;justify-content:center;margin:0 auto 20px
}
.step-title{font-size:1.1rem;font-weight:bold;color:#fff;margin-bottom:8px}
.step-desc{font-size:0.85rem;color:#9088a8;line-height:1.6}
.step-arrow{position:absolute;top:28px;right:-24px;color:#D4AF37;font-size:1.5rem}
@media(max-width:768px){
  .steps-grid{grid-template-columns:1fr;gap:24px}
  .step-arrow{display:none}
}

/* ===== Form Section ===== */
.form-section-wrapper{
  background:#1A1A2E;border-radius:20px;padding:48px;
  border:1px solid #2a2a4a
}
.form-section-wrapper .section-header{margin-bottom:32px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:700px;margin:0 auto}
.form-grid.full{grid-template-columns:1fr}
.form-group{margin-bottom:0}
.form-label{display:block;font-size:0.85rem;color:#c0b8a8;margin-bottom:8px;font-weight:500}
.form-input,.form-select{
  width:100%;height:48px;background:rgba(255,255,255,0.05);
  border:1px solid #3a3a5a;border-radius:10px;padding:0 16px;
  font-size:0.9rem;color:#e0d8c8;outline:none;transition:border-color 0.2s;font-family:inherit
}
.form-input:focus,.form-select:focus{border-color:#D4AF37}
.form-select{
  appearance:none;cursor:pointer;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%238a7e6b' viewBox='0 0 16 16'%3E%3Cpath d='M8 11L3 6h10z'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 16px center
}
.form-select option{background:#1a1a2e;color:#e0d8c8}
.radio-group{display:flex;gap:12px}
.radio-item{
  flex:1;height:48px;background:rgba(255,255,255,0.05);
  border:1px solid #3a3a5a;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:0.9rem;color:#8a7e6b;cursor:pointer;transition:all 0.2s;user-select:none
}
.radio-item.active{border-color:#D4AF37;color:#D4AF37;background:rgba(212,175,55,0.1)}
.date-type-tabs{display:flex;gap:12px;margin-bottom:12px}
.date-tab{
  flex:1;height:38px;background:rgba(255,255,255,0.05);
  border:1px solid #3a3a5a;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:0.8rem;color:#8a7e6b;cursor:pointer;transition:all 0.2s;user-select:none
}
.date-tab.active{border-color:#D4AF37;color:#D4AF37;background:rgba(212,175,55,0.1)}
.date-picker-box{
  background:rgba(255,255,255,0.05);border:1px solid #3a3a5a;
  border-radius:10px;height:48px;display:flex;align-items:center;padding:0 16px
}
.date-picker-box input[type="date"]{
  width:100%;background:none;border:none;font-size:0.9rem;color:#e0d8c8;outline:none;font-family:inherit
}
.date-picker-box input[type="date"]::-webkit-calendar-picker-indicator{filter:invert(0.7)}
.btn-submit{
  grid-column:1/-1;height:56px;background:linear-gradient(135deg,#D4AF37,#C49F27);
  border:none;border-radius:28px;font-size:1.05rem;color:#1a1a2e;font-weight:bold;
  cursor:pointer;margin-top:8px;transition:all 0.3s;
  display:flex;align-items:center;justify-content:center;gap:8px
}
.btn-submit:hover{opacity:0.9;transform:translateY(-2px);box-shadow:0 8px 24px rgba(212,175,55,0.3)}
.btn-submit:disabled{opacity:0.6;cursor:not-allowed;transform:none}
.spinner{
  display:inline-block;width:20px;height:20px;
  border:2px solid rgba(26,26,46,0.3);border-top-color:#1a1a2e;
  border-radius:50%;animation:spin 0.6s linear infinite
}
@keyframes spin{to{transform:rotate(360deg)}}
.form-note{text-align:center;margin-top:16px;font-size:0.75rem;color:#6a6040}
@media(max-width:768px){.form-section-wrapper{padding:32px 20px}.form-grid{grid-template-columns:1fr}}

/* ===== Chart Result ===== */
.result-section{display:none}
.result-section.active{display:block}
.chart-wrapper{
  background:#1A1A2E;border-radius:20px;padding:32px;
  border:1px solid #2a2a4a
}
.chart-info{text-align:center;margin-bottom:24px}
.chart-name{font-size:1.1rem;color:#D4AF37;font-weight:bold}
.chart-date{font-size:0.85rem;color:#8a7e6b;margin-top:4px}
.ganzhi-bar{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-bottom:20px}
.ganzhi-item{
  font-size:0.75rem;color:#8a7e6b;background:rgba(255,255,255,0.05);
  padding:4px 14px;border-radius:6px
}
.chart-grid-table{width:100%;border:1px solid #3a3a5a;border-radius:12px;overflow:hidden}
.chart-row{display:flex;border-bottom:1px solid #2a2a4a}
.chart-row:last-child{border-bottom:none}
.chart-cell{
  flex:1;min-height:105px;padding:10px 8px;background:rgba(255,255,255,0.02);
  border-right:1px solid #2a2a4a;cursor:pointer;transition:background 0.2s
}
.chart-cell:hover{background:rgba(212,175,55,0.06)}
.chart-cell:last-child{border-right:none}
.chart-cell.ming{background:rgba(212,175,55,0.1)}
.center-cell{
  flex:2;min-height:105px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  background:rgba(212,175,55,0.04);padding:10px;border-right:1px solid #2a2a4a
}
.center-element{font-size:0.95rem;color:#D4AF37;font-weight:bold}
.center-label{font-size:0.65rem;color:#6a6048;margin-top:2px}
.center-lunar{font-size:0.7rem;color:#8a7e6b;margin-top:4px}
.center-ziwei{font-size:1rem;margin-top:2px;color:#D4AF37}
.cell-branch-row{display:flex;align-items:center;gap:4px;margin-bottom:3px}
.cell-branch-tag{font-size:0.7rem;color:#5a5040;font-weight:bold}
.cell-shen-tag{
  font-size:0.6rem;color:#10B981;background:rgba(16,185,129,0.15);
  padding:0 6px;border-radius:3px
}
.cell-title{font-size:0.75rem;color:#D4AF37;font-weight:bold;display:block;margin-bottom:4px}
.cell-stars-list{display:flex;flex-wrap:wrap;gap:3px}
.star-tag{font-size:0.58rem;padding:1px 5px;border-radius:3px;white-space:nowrap;line-height:1.5}
.star-tag.main{color:#f0d080;background:rgba(240,208,128,0.15)}
.star-tag.aux{color:#80c0f0;background:rgba(128,192,240,0.12)}
.star-tag.sha{color:#f08080;background:rgba(240,128,128,0.12)}
.cell-hua{display:flex;flex-wrap:wrap;gap:2px;margin-top:3px}
.hua-tag{font-size:0.52rem;padding:1px 5px;border-radius:2px;font-weight:bold}
.hua-tag.lu{color:#f0d080;background:rgba(240,208,128,0.2)}
.hua-tag.quan{color:#10B981;background:rgba(16,185,129,0.2)}
.hua-tag.ke{color:#80c0f0;background:rgba(128,192,240,0.2)}
.hua-tag.ji{color:#f08080;background:rgba(240,128,128,0.2)}
.hua-bar{
  display:flex;align-items:center;justify-content:center;flex-wrap:wrap;
  gap:14px;margin:20px 0;padding:14px;background:rgba(255,255,255,0.03);border-radius:12px
}
.hua-label{font-size:0.85rem;color:#8a7e6b}
.hua-item{font-size:0.85rem;font-weight:bold;padding:4px 14px;border-radius:8px}
.hua-item.lu{color:#f0d080;background:rgba(240,208,128,0.12)}
.hua-item.quan{color:#10B981;background:rgba(16,185,129,0.12)}
.hua-item.ke{color:#80c0f0;background:rgba(128,192,240,0.12)}
.hua-item.ji{color:#f08080;background:rgba(240,128,128,0.12)}
.daxian-scroll{overflow-x:auto;padding-bottom:8px}
.daxian-row{display:flex;gap:10px}
.daxian-item{
  flex:0 0 auto;display:flex;flex-direction:column;align-items:center;
  padding:12px 18px;background:rgba(255,255,255,0.03);
  border:1px solid #2a2a4a;border-radius:10px;min-width:80px
}
.daxian-age{font-size:0.7rem;color:#8a7e6b}
.daxian-palace{font-size:0.75rem;color:#D4AF37;margin-top:4px}
.chart-actions{display:flex;flex-direction:column;gap:14px;margin-top:28px}
.btn-outline{
  height:50px;background:transparent;border:2px solid #D4AF37;
  border-radius:25px;font-size:0.92rem;color:#D4AF37;font-weight:bold;
  cursor:pointer;transition:background 0.2s;
  display:flex;align-items:center;justify-content:center
}
.btn-outline:hover{background:rgba(212,175,55,0.08)}
.btn-outline.unlocked{border-color:#10B981;color:#10B981;background:rgba(16,185,129,0.08)}
.btn-secondary{
  height:46px;background:rgba(255,255,255,0.05);border:1px solid #3a3a5a;
  border-radius:23px;font-size:0.85rem;color:#8a7e6b;cursor:pointer;
  transition:background 0.2s;display:flex;align-items:center;justify-content:center
}
.btn-secondary:hover{background:rgba(255,255,255,0.08)}
@media(max-width:768px){.chart-wrapper{padding:16px 8px}}

/* ===== Detail View ===== */
.detail-section-wrapper{display:none}
.detail-section-wrapper.active{display:block}
.detail-inner{
  background:#1A1A2E;border-radius:20px;padding:40px;
  border:1px solid #2a2a4a
}
.detail-header{text-align:center;margin-bottom:28px}
.detail-title{font-size:1.2rem;color:#D4AF37;font-weight:bold}
.detail-subtitle{font-size:0.8rem;color:#8a7e6b;margin-top:6px}
.summary-card{
  background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);
  border-radius:14px;padding:18px;margin-bottom:24px
}
.summary-text{display:block;font-size:0.85rem;color:#c0b8a8;line-height:1.7}
.hua-grid{display:flex;gap:12px;margin-bottom:24px}
.hua-card{flex:1;padding:16px 10px;border-radius:12px;text-align:center}
.hua-card.lu{background:rgba(240,208,128,0.1);border:1px solid rgba(240,208,128,0.25)}
.hua-card.quan{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25)}
.hua-card.ke{background:rgba(128,192,240,0.1);border:1px solid rgba(128,192,240,0.25)}
.hua-card.ji{background:rgba(240,128,128,0.1);border:1px solid rgba(240,128,128,0.25)}
.hua-type{display:block;font-size:0.7rem;color:#8a7e6b;margin-bottom:4px}
.hua-star{display:block;font-size:1.05rem;font-weight:bold}
.hua-card.lu .hua-star{color:#f0d080}
.hua-card.quan .hua-star{color:#10B981}
.hua-card.ke .hua-star{color:#80c0f0}
.hua-card.ji .hua-star{color:#f08080}
.hua-desc{display:block;font-size:0.63rem;color:#6a6048;margin-top:3px}
.pattern-card{
  background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.15);
  border-radius:12px;padding:14px;margin-bottom:12px
}
.pattern-name{display:block;font-size:0.9rem;color:#D4AF37;font-weight:bold;margin-bottom:6px}
.pattern-desc{display:block;font-size:0.78rem;color:#b0a898;line-height:1.6}
.palace-card{
  background:rgba(255,255,255,0.02);border:1px solid #2a2a4a;
  border-radius:12px;padding:16px;margin-bottom:10px;cursor:pointer;transition:background 0.2s
}
.palace-card:hover{background:rgba(212,175,55,0.04);border-color:#3a3a5a}
.palace-card.ming{background:rgba(212,175,55,0.08);border-color:rgba(212,175,55,0.25)}
.palace-header{display:flex;align-items:center;gap:8px}
.palace-left{display:flex;align-items:center;gap:6px;min-width:100px}
.palace-name{font-size:0.9rem;color:#D4AF37;font-weight:bold}
.palace-branch{font-size:0.72rem;color:#6a6048}
.shen-tag{
  font-size:0.65rem;color:#10B981;background:rgba(16,185,129,0.15);
  padding:0 6px;border-radius:3px
}
.palace-stars{flex:1;display:flex;flex-wrap:wrap;gap:4px}
.palace-star{font-size:0.7rem;padding:2px 8px;border-radius:4px}
.palace-star.main{color:#f0d080;background:rgba(240,208,128,0.12)}
.arrow-icon{font-size:1.1rem;color:#3a3a5a}
.palace-hua{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.hua-badge{font-size:0.65rem;padding:2px 8px;border-radius:4px}
.hua-badge.lu{color:#f0d080;background:rgba(240,208,128,0.12)}
.hua-badge.quan{color:#10B981;background:rgba(16,185,129,0.12)}
.hua-badge.ke{color:#80c0f0;background:rgba(128,192,240,0.12)}
.hua-badge.ji{color:#f08080;background:rgba(240,128,128,0.12)}
.palace-preview{margin-top:8px}
.preview-text{font-size:0.78rem;color:#6a6048;line-height:1.5}
.dx-list{display:flex;flex-wrap:wrap;gap:10px}
.dx-card{
  width:calc(33.33% - 7px);padding:12px 8px;
  background:rgba(255,255,255,0.02);border:1px solid #2a2a4a;
  border-radius:10px;text-align:center
}
.dx-age{display:block;font-size:0.7rem;color:#8a7e6b;margin-bottom:3px}
.dx-palace{display:block;font-size:0.8rem;color:#D4AF37;font-weight:bold;margin-bottom:3px}
.dx-stars{display:block;font-size:0.65rem;color:#6a6048}
.text-card{
  background:rgba(255,255,255,0.02);border:1px solid #2a2a4a;
  border-radius:12px;padding:18px;margin-bottom:24px
}
.body-text{font-size:0.85rem;color:#c0b8a8;line-height:1.7}
.advice-card{
  background:rgba(128,192,240,0.05);border:1px solid rgba(128,192,240,0.15);
  border-radius:12px;padding:18px
}
.advice-text{font-size:0.85rem;color:#a0b8d0;line-height:1.7}
@media(max-width:768px){
  .detail-inner{padding:20px 16px}
  .hua-grid{flex-wrap:wrap}
  .dx-card{width:calc(50% - 5px)}
}

/* ===== Testimonials ===== */
.testimonials-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.testimonial-card{
  background:#1A1A2E;border-radius:16px;padding:28px;
  border:1px solid #2a2a4a
}
.testimonial-stars{color:#D4AF37;font-size:1.1rem;margin-bottom:12px}
.testimonial-text{font-size:0.9rem;color:#c0b8a8;line-height:1.7;margin-bottom:16px}
.testimonial-author{font-size:0.85rem;color:#D4AF37;font-weight:bold}
.testimonial-role{font-size:0.75rem;color:#6a6048}
.stats-row{display:flex;justify-content:center;gap:48px;margin-top:48px;flex-wrap:wrap}
.stat-item{text-align:center}
.stat-num{font-size:2rem;font-weight:bold;color:#D4AF37}
.stat-label{font-size:0.85rem;color:#8a7e6b;margin-top:4px}
@media(max-width:768px){.testimonials-grid{grid-template-columns:1fr}.stats-row{gap:24px}}

/* ===== Pricing ===== */
.pricing-card{
  max-width:440px;margin:0 auto;background:#1A1A2E;border-radius:20px;
  padding:40px;border:2px solid #D4AF37;text-align:center;position:relative
}
.pricing-badge{
  position:absolute;top:-14px;left:50%;transform:translateX(-50%);
  background:#10B981;color:#fff;padding:4px 16px;border-radius:12px;
  font-size:0.75rem;font-weight:bold
}
.pricing-name{font-size:1.2rem;color:#fff;font-weight:bold;margin-bottom:20px}
.pricing-price{font-size:3rem;font-weight:bold;color:#D4AF37;margin-bottom:4px}
.pricing-period{font-size:0.85rem;color:#8a7e6b;margin-bottom:28px}
.pricing-features{list-style:none;margin-bottom:32px}
.pricing-features li{
  font-size:0.9rem;color:#c0b8a8;padding:8px 0;
  border-bottom:1px solid #2a2a4a
}
.pricing-features li:last-child{border:none}
.pricing-features .check{color:#10B981;margin-right:8px}

/* ===== FAQ ===== */
.faq-list{max-width:700px;margin:0 auto}
.faq-item{
  background:#1A1A2E;border:1px solid #2a2a4a;border-radius:12px;
  margin-bottom:12px;overflow:hidden;cursor:pointer
}
.faq-q{
  padding:18px 24px;display:flex;justify-content:space-between;
  align-items:center;font-weight:bold;color:#fff;font-size:0.95rem
}
.faq-q:hover{color:#D4AF37}
.faq-q .arrow-icon{color:#D4AF37;transition:transform 0.3s;font-size:0.8rem}
.faq-item.open .faq-q .arrow-icon{transform:rotate(180deg)}
.faq-a{padding:0 24px;max-height:0;overflow:hidden;transition:all 0.3s}
.faq-item.open .faq-a{padding:0 24px 18px;max-height:300px}
.faq-a p{font-size:0.85rem;color:#9088a8;line-height:1.7}

/* ===== CTA Section ===== */
.cta-section{background:#2D1B4E;text-align:center}
.cta-title{font-size:2rem;font-weight:bold;color:#fff;margin-bottom:16px}
.cta-desc{font-size:1rem;color:#c0b8d0;margin-bottom:32px}
@media(max-width:768px){.cta-title{font-size:1.5rem}}

/* ===== Footer ===== */
.site-footer{
  background:#0d0d1f;padding:48px 0 24px;text-align:center;
  border-top:1px solid #2a2a4a
}
.footer-brand{font-size:1.2rem;color:#D4AF37;font-weight:bold;margin-bottom:8px}
.footer-desc{font-size:0.85rem;color:#6a6048;margin-bottom:24px}
.footer-links{display:flex;justify-content:center;gap:32px;flex-wrap:wrap;margin-bottom:24px}
.footer-links a{font-size:0.85rem;color:#8a7e6b;transition:color 0.2s}
.footer-links a:hover{color:#D4AF37}
.footer-bottom{font-size:0.75rem;color:#4a4050}

/* ===== Modal ===== */
.modal-overlay{
  position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:900;
  display:flex;align-items:center;justify-content:center;padding:24px
}
.modal-overlay.hidden{display:none}
.modal-box{
  background:#1A1A2E;border:1px solid #3a3a5a;border-radius:18px;
  padding:32px 28px 24px;max-width:420px;width:100%;max-height:80vh;overflow-y:auto
}
.modal-title{font-size:1.1rem;color:#D4AF37;font-weight:bold;margin-bottom:16px;text-align:center}
.modal-body{
  font-size:0.88rem;color:#c0b8a8;line-height:1.8;white-space:pre-wrap;margin-bottom:22px
}
.modal-btn{
  width:100%;height:48px;background:linear-gradient(135deg,#D4AF37,#C49F27);
  border:none;border-radius:24px;font-size:1rem;color:#1a1a2e;font-weight:bold;
  cursor:pointer;transition:opacity 0.2s
}
.modal-btn:hover{opacity:0.9}
.modal-btn:disabled{opacity:0.6;cursor:not-allowed}
.modal-btn-cancel{
  width:100%;height:42px;background:transparent;border:1px solid #3a3a5a;
  border-radius:21px;font-size:0.85rem;color:#8a7e6b;cursor:pointer;
  margin-top:12px;transition:background 0.2s
}
.modal-btn-cancel:hover{background:rgba(255,255,255,0.05)}

/* ===== Toast ===== */
.toast-container{
  position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
  z-index:1000;pointer-events:none
}
.toast-msg{
  background:rgba(0,0,0,0.9);color:#e0d8c8;padding:14px 28px;
  border-radius:12px;font-size:0.88rem;text-align:center;
  max-width:320px;transition:opacity 0.3s
}
</style>
'''

# New body HTML (landing page)
new_body = '''<body>
<div class="toast-container" id="toast"></div>

<!-- Modal -->
<div class="modal-overlay hidden" id="modalOverlay">
  <div class="modal-box">
    <div class="modal-title" id="modalTitle"></div>
    <div class="modal-body" id="modalBody"></div>
    <button class="modal-btn" onclick="App.closeModal()">知道了</button>
    <button class="modal-btn-cancel" style="display:none;" onclick="App.closeModal()">暂不需要</button>
  </div>
</div>

<!-- ===== HEADER ===== -->
<header class="site-header">
  <div class="container header-inner">
    <a class="header-logo" href="#">
      <span class="icon">&#x263E;</span>
      <span>yourfate.xyz</span>
    </a>
    <nav class="header-nav">
      <a href="#features">服务分类</a>
      <a href="#how-it-works">如何使用</a>
      <a href="#form">在线排盘</a>
      <a href="#pricing">定价</a>
      <a href="#faq">常见问题</a>
    </nav>
    <button class="header-cta" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">立即解密</button>
    <button class="mobile-menu-btn" onclick="this.nextElementSibling.classList.toggle('show')">&#9776;</button>
  </div>
</header>

<!-- ===== HERO ===== -->
<section class="hero-section" id="home">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-badge">&#x2B50; 紫微斗数 · 专业解密 · 隐私保护</div>
    <h1 class="hero-title">用千年智慧，<br>解密你的<span class="gold">人生运势</span></h1>
    <p class="hero-sub">基于传统紫微斗数算法，精准排盘，十二宫详解<br>命盘格局 · 大限运势 · 四化飞星 · 综合解读</p>
    <div class="hero-btns">
      <button class="btn-gold" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">&#x1F52E; 立即解密</button>
      <button class="btn-outline-light" onclick="document.getElementById('how-it-works').scrollIntoView({behavior:'smooth'})">了解服务</button>
    </div>
  </div>
  <div class="hero-scroll" onclick="document.getElementById('features').scrollIntoView({behavior:'smooth'})">
    <span>&#x2304;</span>
  </div>
</section>

<!-- ===== FEATURES ===== -->
<section class="section" id="features">
  <div class="container">
    <div class="section-header">
      <div class="section-label">服务分类</div>
      <h2 class="section-title">全方位命运解读</h2>
      <p class="section-desc">从事业财运到感情健康，紫微斗数为你揭示人生的各个面向</p>
    </div>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">&#x1F4BC;</div>
        <div class="feature-name">事业运</div>
        <div class="feature-desc">事业宫解读职业发展方向，分析官禄运、贵人运，助你做出正确职涯决策</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">&#x1F498;</div>
        <div class="feature-name">感情运</div>
        <div class="feature-desc">夫妻宫详解桃花姻缘，了解感情模式，把握良缘时机</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">&#x1F4B0;</div>
        <div class="feature-name">财运</div>
        <div class="feature-desc">财帛宫分析求财方式，识财运旺衰，掌财富密码</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">&#x1F3E5;</div>
        <div class="feature-name">综合运势</div>
        <div class="feature-desc">十二宫全盘解读，命盘格局分析，大限运势推演，全方位了解人生轨迹</div>
      </div>
    </div>
  </div>
</section>

<!-- ===== HOW IT WORKS ===== -->
<section class="section bg-dark" id="how-it-works" style="background:#0d0d1f;">
  <div class="container">
    <div class="section-header">
      <div class="section-label">如何使用</div>
      <h2 class="section-title">三步揭秘你的命运密码</h2>
      <p class="section-desc">简单三步，获取专业级紫微斗数命盘解读</p>
    </div>
    <div class="steps-grid">
      <div class="step-card">
        <div class="step-num">1</div>
        <div class="step-title">输入出生信息</div>
        <div class="step-desc">填写你的出生年月日时和性别，支持公历和农历两种日期输入方式</div>
        <span class="step-arrow">&#x2192;</span>
      </div>
      <div class="step-card">
        <div class="step-num">2</div>
        <div class="step-title">智能排盘</div>
        <div class="step-desc">系统自动计算十二宫星曜分布、四化飞星、大限运势，生成专业命盘</div>
        <span class="step-arrow">&#x2192;</span>
      </div>
      <div class="step-card">
        <div class="step-num">3</div>
        <div class="step-title">详细解盘</div>
        <div class="step-desc">获取十二宫详细解读、命盘格局分析、大限运势推演，全面了解人生运势</div>
      </div>
    </div>
  </div>
</section>

<!-- ===== FORTUNE FORM ===== -->
<section class="section" id="form">
  <div class="container">
    <div class="section-header">
      <div class="section-label">在线排盘</div>
      <h2 class="section-title">填入你的出生信息</h2>
      <p class="section-desc">准确填写出生资料，即可免费查看紫微斗数命盘</p>
    </div>
    <div class="form-section-wrapper">
      <div class="form-grid" id="formGrid">
        <div class="form-group">
          <label class="form-label">姓名（选填）</label>
          <input class="form-input" id="inputName" placeholder="请输入您的姓名" maxlength="20">
        </div>
        <div class="form-group">
          <label class="form-label">性别</label>
          <div class="radio-group">
            <div class="radio-item active" data-gender="male" onclick="App.selectGender(this)">&#x1F468; 男</div>
            <div class="radio-item" data-gender="female" onclick="App.selectGender(this)">&#x1F469; 女</div>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">出生日期</label>
          <div class="date-type-tabs">
            <div class="date-tab active" data-type="solar" onclick="App.selectDateType(this)">&#x2600;&#xFE0F; 公历</div>
            <div class="date-tab" data-type="lunar" onclick="App.selectDateType(this)">&#x1F319; 农历</div>
          </div>
          <div class="date-picker-box">
            <input type="date" id="inputDate" value="1990-01-01" min="1900-01-01" max="2100-12-31">
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">出生时辰</label>
          <div class="form-select-wrapper">
            <select class="form-select" id="inputHour">
              <option value="0">子时 (23:00-01:00)</option>
              <option value="1">丑时 (01:00-03:00)</option>
              <option value="2">寅时 (03:00-05:00)</option>
              <option value="3">卯时 (05:00-07:00)</option>
              <option value="4">辰时 (07:00-09:00)</option>
              <option value="5">巳时 (09:00-11:00)</option>
              <option value="6">午时 (11:00-13:00)</option>
              <option value="7">未时 (13:00-15:00)</option>
              <option value="8">申时 (15:00-17:00)</option>
              <option value="9">酉时 (17:00-19:00)</option>
              <option value="10">戌时 (19:00-21:00)</option>
              <option value="11">亥时 (21:00-23:00)</option>
            </select>
          </div>
        </div>
        <button class="btn-submit" id="btnSubmit" onclick="App.onSubmit()">
          开始排盘
        </button>
      </div>
      <div class="form-note">命理分析仅供参考 · 命运由自己掌握</div>
    </div>
  </div>
</section>

<!-- ===== CHART RESULT ===== -->
<section class="section result-section" id="resultSection">
  <div class="container">
    <div class="section-header">
      <div class="section-label">排盘结果</div>
      <h2 class="section-title">你的紫微斗数命盘</h2>
    </div>
    <div class="chart-wrapper" id="chartContainer"></div>
    <div class="chart-actions">
      <button class="btn-outline" id="btnDetail" onclick="App.goToDetail()"><span id="btnDetailText">查看详细解盘</span></button>
      <button class="btn-secondary" onclick="App.resetForm()">重新输入</button>
    </div>
  </div>
</section>

<!-- ===== DETAIL RESULT ===== -->
<section class="section detail-section-wrapper" id="detailSection">
  <div class="container">
    <div class="detail-inner" id="detailContainer"></div>
    <div class="chart-actions">
      <button class="btn-secondary" onclick="App.backToChart()">返回命盘</button>
    </div>
  </div>
</section>

<!-- ===== TESTIMONIALS ===== -->
<section class="section" style="background:#0d0d1f;">
  <div class="container">
    <div class="section-header">
      <div class="section-label">用户评价</div>
      <h2 class="section-title">他们都在用紫微斗数解密人生</h2>
    </div>
    <div class="testimonials-grid">
      <div class="testimonial-card">
        <div class="testimonial-stars">&#x2605;&#x2605;&#x2605;&#x2605;&#x2605;</div>
        <div class="testimonial-text">排盘结果非常详细，十二宫的解读让我对自己有了全新的认识。特别是事业宫的解读，和我的实际情况非常吻合。</div>
        <div class="testimonial-author">李先生</div>
        <div class="testimonial-role">互联网从业者</div>
      </div>
      <div class="testimonial-card">
        <div class="testimonial-stars">&#x2605;&#x2605;&#x2605;&#x2605;&#x2605;</div>
        <div class="testimonial-text">夫妻宫的解读让我对感情有了更清晰的认识。化忌的地方也确实是我需要努力的方向。非常专业的解析！</div>
        <div class="testimonial-author">王女士</div>
        <div class="testimonial-role">教师</div>
      </div>
      <div class="testimonial-card">
        <div class="testimonial-stars">&#x2605;&#x2605;&#x2605;&#x2605;&#x2605;</div>
        <div class="testimonial-text">大限运势的推算让我对未来的规划有了方向。格局分析准确度很高，推荐给需要的朋友。</div>
        <div class="testimonial-author">张先生</div>
        <div class="testimonial-role">创业者</div>
      </div>
    </div>
    <div class="stats-row">
      <div class="stat-item"><div class="stat-num">10,000+</div><div class="stat-label">已服务用户</div></div>
      <div class="stat-item"><div class="stat-num">98%</div><div class="stat-label">好评率</div></div>
      <div class="stat-item"><div class="stat-num">100%</div><div class="stat-label">隐私保护</div></div>
    </div>
  </div>
</section>

<!-- ===== PRICING ===== -->
<section class="section" id="pricing">
  <div class="container">
    <div class="section-header">
      <div class="section-label">定价</div>
      <h2 class="section-title">选择适合你的方案</h2>
    </div>
    <div class="pricing-card">
      <div class="pricing-badge">&#x1F31F; 最受欢迎</div>
      <div class="pricing-name">详细解盘套餐</div>
      <div class="pricing-price">$9.99</div>
      <div class="pricing-period">一次性付费 · 永久查看</div>
      <ul class="pricing-features">
        <li><span class="check">&#x2713;</span> 十二宫详细解读</li>
        <li><span class="check">&#x2713;</span> 命盘格局分析</li>
        <li><span class="check">&#x2713;</span> 大限运势推演</li>
        <li><span class="check">&#x2713;</span> 四化飞星详解</li>
        <li><span class="check">&#x2713;</span> 综合运势建议</li>
      </ul>
      <button class="btn-gold" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">&#x1F52E; 立即开始</button>
    </div>
  </div>
</section>

<!-- ===== FAQ ===== -->
<section class="section" id="faq" style="background:#0d0d1f;">
  <div class="container">
    <div class="section-header">
      <div class="section-label">常见问题</div>
      <h2 class="section-title">有任何疑问？我们为你解答</h2>
    </div>
    <div class="faq-list">
      <div class="faq-item" onclick="this.classList.toggle('open')">
        <div class="faq-q">紫微斗数是什么？<span class="arrow-icon">&#x2304;</span></div>
        <div class="faq-a"><p>紫微斗数是中国传统命理学的重要分支，起源于宋代，通过出生年月日时推算十二宫星曜分布，分析人生各个方面的运势和发展趋势。与八字并称为中国传统命理学的两大体系。</p></div>
      </div>
      <div class="faq-item" onclick="this.classList.toggle('open')">
        <div class="faq-q">排盘结果准确吗？<span class="arrow-icon">&#x2304;</span></div>
        <div class="faq-a"><p>我们使用传统紫微斗数算法，严格按照古法计算星曜分布和四化飞星。但请注意，命理分析仅供参考，人生的走向更多取决于自己的选择和努力。</p></div>
      </div>
      <div class="faq-item" onclick="this.classList.toggle('open')">
        <div class="faq-q">如何保证我的隐私安全？<span class="arrow-icon">&#x2304;</span></div>
        <div class="faq-a"><p>所有出生信息仅用于排盘计算，我们不会存储或分享你的个人数据。支付通过 Stripe 安全处理，我们不接触你的支付信息。</p></div>
      </div>
      <div class="faq-item" onclick="this.classList.toggle('open')">
        <div class="faq-q">支持哪些支付方式？<span class="arrow-icon">&#x2304;</span></div>
        <div class="faq-a"><p>我们通过 Stripe 接受全球主流信用卡和借记卡支付（Visa、Mastercard、American Express 等），安全便捷。</p></div>
      </div>
    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="cta-section section">
  <div class="container">
    <h2 class="cta-title">准备好解密你的人生运势了吗？</h2>
    <p class="cta-desc">输入出生信息，即刻获取你的专属紫微斗数命盘解读</p>
    <button class="btn-gold" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">&#x1F52E; 立即开始</button>
  </div>
</section>

<!-- ===== FOOTER ===== -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-brand">&#x263E; yourfate.xyz</div>
    <div class="footer-desc">紫微斗数在线命理解密服务平台</div>
    <div class="footer-links">
      <a href="#home">首页</a>
      <a href="#features">服务分类</a>
      <a href="#form">在线排盘</a>
      <a href="#pricing">定价</a>
      <a href="#faq">常见问题</a>
    </div>
    <div class="footer-bottom">&copy; 2026 yourfate.xyz · 命理分析仅供参考 · 命运由自己掌握</div>
  </div>
</footer>
'''

# Build the new file
before_style = old[:style_start]
style_to_body_tag = old[style_end:body_tag]
after_first_script = old[body_tag_end:first_script]
body_close = old.find('</body>', first_script)
scripts_and_after = old[first_script:]

new_html = before_style + new_css + new_body + scripts_and_after

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'Done! New index.html: {len(new_html)} bytes')
print(f'CSS section: {len(new_css)} chars')
print(f'Body section: {len(new_body)} chars')
print(f'JS section: {len(scripts_and_after)} chars')
