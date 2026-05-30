# SellerAI Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-ready single-page landing page for SellerAI SaaS in Apple.com style

**Architecture:** Single HTML file (index.html) with embedded CSS and vanilla JS. Google Fonts as only external dependency. Semantic HTML5 with ARIA attributes. Mobile-first responsive design with Intersection Observer scroll animations.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox), vanilla JavaScript (Intersection Observer, smooth scroll, interactive calculator)

---

### Task 1: Project scaffold and HTML structure

**Files:**
- Create: `D:\PROEKT\sellerai\index.html`
- Modify: None

- [ ] **Step 1: Create directory and base HTML file**

```bash
New-Item -ItemType Directory -Path "D:\PROEKT\sellerai" -Force | Out-Null
```

- [ ] **Step 2: Write HTML skeleton with head, Google Fonts import, and empty body**

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SellerAI — ИИ-помощник для продавцов маркетплейсов</title>
  <meta name="description" content="Контент для Wildberries, Ozon и Яндекс Маркет за 3 секунды. Заголовки, описания, SEO — нейросеть для продавцов.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* CSS will be added in Task 2 */
  </style>
</head>
<body>
  <!-- Content will be added in Task 3-7 -->
  <script>
    // JS will be added in Task 8
  </script>
</body>
</html>
```

- [ ] **Step 3: Verify file created**

Run: `Test-Path -LiteralPath "D:\PROEKT\sellerai\index.html"`
Expected: `True`

- [ ] **Step 4: Commit**

```bash
git add D:\PROEKT\sellerai\index.html
git commit -m "chore: scaffold sellerai landing page"
```

---

### Task 2: CSS design system — variables, reset, typography

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add CSS inside `<style>` tag)

- [ ] **Step 1: Add CSS reset and custom properties**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #ffffff;
  color: #1d1d1f;
  line-height: 1.5;
  overflow-x: hidden;
}
img { max-width: 100%; display: block; }
a { text-decoration: none; color: inherit; }
button { cursor: pointer; font-family: inherit; }
```

- [ ] **Step 2: Add design tokens as CSS custom properties**

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f7;
  --bg-tertiary: #e8e8ed;
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --text-tertiary: #aeaeb2;
  --accent-blue: #0071e3;
  --accent-blue-hover: #0077ed;
  --accent-orange: #FF4D00;
  --border-subtle: rgba(0,0,0,0.04);
  --border-light: rgba(0,0,0,0.06);
  --radius-pill: 980px;
  --radius-card: 14px;
  --radius-lg: 20px;
  --max-width: 1100px;
  --content-width: 650px;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

- [ ] **Step 3: Add utility classes**

```css
.container { max-width: var(--max-width); margin: 0 auto; padding: 0 1.5rem; }
.content { max-width: var(--content-width); margin: 0 auto; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
```

- [ ] **Step 4: Add typography styles for Apple-style text hierarchy**

```css
.eyebrow {
  font-size: 0.8rem; font-weight: 600; color: var(--accent-orange);
  letter-spacing: 0.03em; text-transform: uppercase; margin-bottom: 0.75rem;
}
.section-title {
  font-size: 1.3rem; font-weight: 700; color: var(--text-primary);
  letter-spacing: -0.02em; margin-bottom: 0.5rem;
}
.section-sub {
  font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;
}
```

- [ ] **Step 5: Add button styles**

```css
.btn-primary {
  display: inline-block; background: var(--accent-blue); color: white;
  border: none; padding: 12px 24px; border-radius: var(--radius-pill);
  font-size: 0.9rem; font-weight: 500; font-family: var(--font-sans);
  transition: background 0.2s; text-align: center;
}
.btn-primary:hover { background: var(--accent-blue-hover); }
.btn-secondary {
  display: inline-block; background: transparent; color: var(--accent-blue);
  border: none; padding: 12px 24px; border-radius: var(--radius-pill);
  font-size: 0.9rem; font-weight: 500; font-family: var(--font-sans);
  transition: opacity 0.2s;
}
.btn-secondary:hover { opacity: 0.7; }
```

- [ ] **Step 6: Verify styles load**

Open file in browser — text should render in Inter with correct colors. No JS errors.

---

### Task 3: Navigation bar — sticky frosted navbar

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add nav HTML and CSS)

- [ ] **Step 1: Add nav CSS**

```css
.nav {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.75rem 1.5rem; position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,0.95);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border-subtle);
}
.nav-logo { font-weight: 700; font-size: 0.9rem; color: var(--text-primary); letter-spacing: -0.01em; }
.nav-links { display: flex; gap: 1.5rem; align-items: center; }
.nav-link { font-size: 0.75rem; color: var(--text-secondary); transition: color 0.2s; background: none; border: none; cursor: pointer; font-family: var(--font-sans); }
.nav-link:hover { color: var(--text-primary); }
.nav-cta {
  background: var(--accent-blue); color: white; border: none;
  padding: 5px 14px; border-radius: var(--radius-pill);
  font-size: 0.75rem; font-weight: 500; font-family: var(--font-sans);
  transition: background 0.2s;
}
.nav-cta:hover { background: var(--accent-blue-hover); }
@media (max-width: 640px) {
  .nav-links { gap: 1rem; }
  .nav-link { font-size: 0.65rem; }
}
```

- [ ] **Step 2: Add nav HTML inside `<body>`**

```html
<nav class="nav" role="navigation" aria-label="Основная навигация">
  <div class="nav-logo">SellerAI</div>
  <div class="nav-links">
    <button class="nav-link" data-section="features">Возможности</button>
    <button class="nav-link" data-section="pricing">Тарифы</button>
    <button class="nav-link" data-section="cta">Контакты</button>
    <button class="nav-cta" data-section="cta">Купить</button>
  </div>
</nav>
```

- [ ] **Step 3: Verify nav renders with frosted glass effect**

Open in browser — nav should be sticky, semi-transparent white, centered links.

---

### Task 4: Hero section — headline, sub, CTAs

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add hero HTML and CSS)

- [ ] **Step 1: Add hero CSS**

```css
.hero { text-align: center; padding: 2.5rem 1.5rem 0; }
.hero-title {
  font-size: 3rem; font-weight: 700; color: var(--text-primary);
  letter-spacing: -0.03em; line-height: 1.05; margin-bottom: 0.5rem;
}
.hero-sub {
  font-size: 1.15rem; color: var(--text-secondary);
  max-width: 480px; margin: 0 auto 1.25rem; line-height: 1.4;
}
.hero-cta { display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; margin-bottom: 0.5rem; }
.hero-trust { font-size: 0.8rem; color: var(--text-secondary); }
@media (max-width: 640px) {
  .hero-title { font-size: 2rem; }
  .hero-sub { font-size: 1rem; }
}
```

- [ ] **Step 2: Add hero HTML after nav**

```html
<section class="hero">
  <p class="eyebrow">ИИ-ПОМОЩНИК ДЛЯ ПРОДАВЦОВ</p>
  <h1 class="hero-title">Контент за 3 секунды</h1>
  <p class="hero-sub">Самое важное для продавцов Wildberries, Ozon и Яндекс Маркет.</p>
  <div class="hero-cta">
    <a href="#cta" class="btn-primary">Попробовать бесплатно</a>
    <a href="#features" class="btn-secondary">Подробнее ›</a>
  </div>
  <p class="hero-trust">7 дней бесплатно. Без привязки карты.</p>
</section>
```

- [ ] **Step 3: Add scroll reveal animation CSS**

```css
.reveal { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }
.reveal.visible { opacity: 1; transform: translateY(0); }
```

- [ ] **Step 4: Verify hero renders with correct hierarchy**

Open in browser — Hero should show eyebrow → title → sub → CTAs → trust line.

---

### Task 5: Product visual mockup section

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add product visual HTML and CSS)

- [ ] **Step 1: Add product visual CSS**

```css
.product-visual { padding: 1.5rem 1.5rem 0; text-align: center; }
.product-frame {
  background: linear-gradient(180deg, var(--bg-secondary), var(--bg-tertiary));
  border-radius: var(--radius-lg); padding: 2rem 1.5rem;
  max-width: var(--content-width); margin: 0 auto;
}
.product-label { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.25rem; }
.product-sublabel { font-size: 0.7rem; color: var(--text-secondary); margin-bottom: 1rem; }
.product-card {
  background: white; border-radius: 12px; padding: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}
.product-input-row { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }
.product-input {
  flex: 1; background: var(--bg-secondary); border-radius: 8px;
  padding: 0.5rem 0.75rem; text-align: left;
}
.product-input-label { font-size: 0.6rem; color: var(--text-secondary); }
.product-input-value { font-size: 0.8rem; color: var(--text-primary); }
.product-btn {
  background: var(--accent-blue); color: white; border: none;
  border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 500;
}
.product-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
.product-tile {
  background: var(--bg-secondary); border-radius: 8px; padding: 0.6rem; text-align: left;
}
.product-tile-label { font-size: 0.55rem; color: var(--text-secondary); text-transform: uppercase; }
.product-tile-value { font-size: 0.7rem; color: var(--text-primary); font-weight: 500; }
.product-tile-ctr { font-size: 0.55rem; color: #34c759; }
@media (max-width: 640px) {
  .product-frame { padding: 1.25rem; }
  .product-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 2: Add product visual HTML after hero**

```html
<section class="product-visual" aria-label="Интерфейс генератора контента">
  <div class="product-frame reveal">
    <div class="product-label">SellerAI</div>
    <div class="product-sublabel">Генератор контента</div>
    <div class="product-card">
      <div class="product-input-row">
        <div class="product-input">
          <div class="product-input-label">Товар</div>
          <div class="product-input-value">Нож профессиональный ✎</div>
        </div>
        <button class="product-btn" aria-label="Сгенерировать">→</button>
      </div>
      <div class="product-grid">
        <div class="product-tile">
          <div class="product-tile-label">ЗАГОЛОВОК</div>
          <div class="product-tile-value">Профессиональный нож из стали</div>
          <div class="product-tile-ctr">CTR +176%</div>
        </div>
        <div class="product-tile">
          <div class="product-tile-label">ОПИСАНИЕ</div>
          <div class="product-tile-value">Готово ✓ 1 240 символов</div>
          <div class="product-tile-ctr"></div>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify product mockup renders**

Open in browser — interface mockup should appear below hero with input field and result tiles.

---

### Task 6: Metrics strip + Features grid

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add metrics and features HTML + CSS)

- [ ] **Step 1: Add metrics CSS**

```css
.metrics {
  display: flex; justify-content: center; gap: 2.5rem;
  padding: 2rem 1.5rem; flex-wrap: wrap;
}
.metric { text-align: center; }
.metric-number { font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em; }
.metric-label { font-size: 0.8rem; color: var(--text-secondary); }
@media (max-width: 640px) {
  .metrics { gap: 1.5rem; }
}
```

- [ ] **Step 2: Add features CSS**

```css
.features { padding: 1.5rem; border-top: 1px solid var(--border-subtle); }
.features-header { text-align: center; margin-bottom: 1.5rem; }
.features-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; max-width: 500px; margin: 0 auto; }
.feature-card {
  background: var(--bg-secondary); border-radius: var(--radius-card);
  padding: 1rem; transition: transform 0.2s;
}
.feature-card:hover { transform: scale(1.02); }
.feature-title { font-weight: 600; font-size: 0.9rem; color: var(--text-primary); margin-bottom: 0.15rem; }
.feature-desc { font-size: 0.8rem; color: var(--text-secondary); }
@media (max-width: 480px) {
  .features-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: Add metrics HTML**

```html
<section class="metrics reveal" aria-label="Ключевые показатели">
  <div class="metric"><div class="metric-number">3с</div><div class="metric-label">скорость</div></div>
  <div class="metric"><div class="metric-number">+40%</div><div class="metric-label">CTR</div></div>
  <div class="metric"><div class="metric-number">4.9★</div><div class="metric-label">рейтинг</div></div>
  <div class="metric"><div class="metric-number">450+</div><div class="metric-label">продавцов</div></div>
</section>
```

- [ ] **Step 4: Add features HTML**

```html
<section class="features" id="features" aria-label="Возможности">
  <div class="features-header">
    <p class="eyebrow">ВОЗМОЖНОСТИ</p>
    <h2 class="section-title">6 инструментов</h2>
  </div>
  <div class="features-grid">
    <div class="feature-card reveal"><div class="feature-title">Заголовок</div><div class="feature-desc">до 100 символов</div></div>
    <div class="feature-card reveal"><div class="feature-title">Описание</div><div class="feature-desc">800–1500 символов</div></div>
    <div class="feature-card reveal"><div class="feature-title">Ключевые слова</div><div class="feature-desc">20–40 с группировкой</div></div>
    <div class="feature-card reveal"><div class="feature-title">Ответы на отзывы</div><div class="feature-desc">позитив + негатив</div></div>
    <div class="feature-card reveal"><div class="feature-title">Идеи для фото</div><div class="feature-desc">5–8 сценариев</div></div>
    <div class="feature-card reveal"><div class="feature-title">Анализ</div><div class="feature-desc">конкуренты</div></div>
  </div>
</section>
```

- [ ] **Step 5: Verify metrics and features render**

Open in browser — 4 metrics in a row, 2×3 feature grid below.

---

### Task 7: Pricing, CTA section, footer

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add pricing/CTA/footer HTML + CSS)

- [ ] **Step 1: Add pricing CSS**

```css
.pricing { padding: 1.5rem; border-top: 1px solid var(--border-subtle); }
.pricing-header { text-align: center; margin-bottom: 1.5rem; }
.pricing-row { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; max-width: 600px; margin: 0 auto; }
.pricing-plan {
  flex: 1; min-width: 160px; max-width: 200px;
  background: var(--bg-secondary); border-radius: var(--radius-card);
  padding: 1.25rem; text-align: center; position: relative;
}
.pricing-plan.highlight {
  background: white; border: 2px solid var(--accent-orange);
  transform: translateY(-4px);
}
.pricing-badge {
  position: absolute; top: -8px; right: 12px;
  background: var(--accent-orange); color: white;
  font-size: 0.55rem; padding: 2px 8px; border-radius: var(--radius-pill);
  font-weight: 600;
}
.pricing-name { font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
.pricing-price { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 0.25rem 0; }
.pricing-period { font-size: 0.65rem; color: var(--text-secondary); }
.pricing-features { font-size: 0.75rem; color: var(--text-secondary); margin: 0.75rem 0; line-height: 1.7; }
.pricing-btn {
  display: block; border: 1px solid var(--border-light);
  border-radius: var(--radius-pill); padding: 7px; text-align: center;
  font-size: 0.75rem; color: var(--text-secondary);
}
.pricing-btn.highlight {
  background: var(--accent-blue); color: white; border: none;
}
```

- [ ] **Step 2: Add CTA CSS**

```css
.cta-section { text-align: center; padding: 2.5rem 1.5rem; }
.cta-title { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.cta-sub { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.25rem; }
```

- [ ] **Step 3: Add footer CSS**

```css
.footer { text-align: center; padding: 0.75rem 1.5rem; border-top: 1px solid var(--border-subtle); font-size: 0.65rem; color: var(--text-secondary); }
.footer-links { display: flex; gap: 1rem; justify-content: center; margin-top: 0.25rem; }
```

- [ ] **Step 4: Add pricing HTML**

```html
<section class="pricing" id="pricing" aria-label="Тарифы">
  <div class="pricing-header">
    <p class="eyebrow">ТАРИФЫ</p>
    <h2 class="section-title">Выберите план</h2>
  </div>
  <div class="pricing-row">
    <div class="pricing-plan reveal">
      <div class="pricing-name">Starter</div>
      <div class="pricing-price">499</div>
      <div class="pricing-period">₽/мес</div>
      <div class="pricing-features">50 генераций<br>1 маркетплейс</div>
      <div class="pricing-btn">Выбрать</div>
    </div>
    <div class="pricing-plan highlight reveal">
      <div class="pricing-badge">ТОП</div>
      <div class="pricing-name">Business</div>
      <div class="pricing-price">999</div>
      <div class="pricing-period">₽/мес</div>
      <div class="pricing-features">200 генераций<br>Все маркетплейсы</div>
      <div class="pricing-btn highlight">Выбрать</div>
    </div>
    <div class="pricing-plan reveal">
      <div class="pricing-name">Pro</div>
      <div class="pricing-price">1 990</div>
      <div class="pricing-period">₽/мес</div>
      <div class="pricing-features">Безлимит<br>API доступ</div>
      <div class="pricing-btn">Выбрать</div>
    </div>
  </div>
</section>
```

- [ ] **Step 5: Add CTA and footer HTML**

```html
<section class="cta-section" id="cta" aria-label="Начать бесплатно">
  <h2 class="cta-title">Начните бесплатно</h2>
  <p class="cta-sub">7 дней бесплатного доступа.</p>
  <a href="#" class="btn-primary" style="padding:14px 28px;font-size:1rem;">Попробовать бесплатно →</a>
</section>

<footer class="footer" role="contentinfo">
  <div>Copyright © 2026 SellerAI</div>
  <div class="footer-links">
    <a href="#">Политика</a>
    <a href="#">Оферта</a>
  </div>
</footer>
```

- [ ] **Step 6: Verify all sections render in order**

Open in browser — full page flow: nav → hero → product → metrics → features → pricing → cta → footer.

---

### Task 8: JavaScript — scroll animations, smooth nav, calculator

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add JS inside `<script>` tag)

- [ ] **Step 1: Add Intersection Observer for scroll reveals**

```javascript
document.addEventListener('DOMContentLoaded', function() {
  // Scroll reveal animations
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length > 0) {
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    revealElements.forEach(function(el) { observer.observe(el); });
  }

  // Smooth scroll for nav links
  document.querySelectorAll('.nav-link, .nav-cta').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var section = this.getAttribute('data-section');
      var target = document.getElementById(section);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
```

- [ ] **Step 2: Add hero CTA smooth scroll**

```javascript
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var id = this.getAttribute('href').slice(1);
      var target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
```

- [ ] **Step 3: Verify JS works**

Open in browser — scroll down, elements should fade in. Click nav links, page should scroll smoothly to sections.

---

### Task 9: Interactive calculator (from original spec)

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add calculator HTML between features and pricing, CSS, JS)

- [ ] **Step 1: Add calculator CSS**

```css
.calculator { padding: 1.5rem; border-top: 1px solid var(--border-subtle); }
.calc-box {
  max-width: 500px; margin: 0 auto;
  background: var(--bg-secondary); border-radius: var(--radius-lg);
  padding: 1.5rem;
}
.calc-label { font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem; }
.calc-value { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); }
.calc-slider { width: 100%; margin: 0.5rem 0 1rem; -webkit-appearance: none; appearance: none; height: 4px; background: #d1d1d6; border-radius: 2px; outline: none; }
.calc-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; border-radius: 50%; background: var(--accent-blue); cursor: pointer; }
.calc-result { text-align: center; padding-top: 1rem; border-top: 1px solid var(--border-light); margin-top: 1rem; }
.calc-result-label { font-size: 0.8rem; color: var(--text-secondary); }
.calc-result-value { font-size: 2rem; font-weight: 700; color: var(--accent-blue); letter-spacing: -0.02em; }
```

- [ ] **Step 2: Add calculator HTML**

```html
<section class="calculator" id="calculator" aria-label="Калькулятор выгоды">
  <div class="features-header">
    <p class="eyebrow">КАЛЬКУЛЯТОР</p>
    <h2 class="section-title">Посчитайте выгоду</h2>
  </div>
  <div class="calc-box reveal">
    <div class="calc-label">Товаров в месяц</div>
    <div class="calc-value" id="calc-products">50</div>
    <input type="range" class="calc-slider" id="calc-slider-products" min="10" max="500" value="50" step="10" aria-label="Количество товаров">
    <div class="calc-label">Тариф</div>
    <div style="display:flex;gap:0.5rem;">
      <button class="calc-plan" data-plan="499" style="flex:1;padding:8px;border-radius:8px;border:1px solid var(--border-light);background:white;font-size:0.8rem;color:var(--text-primary);font-weight:500;">Starter 499₽</button>
      <button class="calc-plan active" data-plan="999" style="flex:1;padding:8px;border-radius:8px;background:var(--accent-blue);color:white;border:none;font-size:0.8rem;font-weight:500;">Business 999₽</button>
      <button class="calc-plan" data-plan="1990" style="flex:1;padding:8px;border-radius:8px;border:1px solid var(--border-light);background:white;font-size:0.8rem;color:var(--text-primary);font-weight:500;">Pro 1 990₽</button>
    </div>
    <div class="calc-result">
      <div class="calc-result-label">Экономия времени в месяц</div>
      <div class="calc-result-value" id="calc-result">~17 часов</div>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Add calculator JS**

```javascript
  // Calculator
  var calcSlider = document.getElementById('calc-slider-products');
  var calcResult = document.getElementById('calc-result');
  var calcProducts = document.getElementById('calc-products');
  var calcPlanBtns = document.querySelectorAll('.calc-plan');
  var currentPlan = 999;

  if (calcSlider) {
    calcSlider.addEventListener('input', function() {
      calcProducts.textContent = this.value;
      updateCalc();
    });
  }

  calcPlanBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      calcPlanBtns.forEach(function(b) {
        b.style.background = 'white';
        b.style.color = 'var(--text-primary)';
        b.style.border = '1px solid var(--border-light)';
      });
      this.style.background = 'var(--accent-blue)';
      this.style.color = 'white';
      this.style.border = 'none';
      currentPlan = parseInt(this.getAttribute('data-plan'));
      updateCalc();
    });
  });

  function updateCalc() {
    var products = parseInt(calcSlider.value);
    // Each product takes ~20 min manually, SellerAI does in 3 sec
    var manualHours = Math.round(products * 20 / 60);
    var aiHours = Math.round(products * 3 / 3600);
    var saved = manualHours - aiHours;
    calcResult.textContent = '~' + saved + ' часов';
  }
```

- [ ] **Step 4: Verify calculator works**

Open in browser — slide the slider, hours should update. Click plan buttons, hours recalculate.

---

### Task 10: Responsive polish and mobile optimization

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html` (add remaining responsive styles)

- [ ] **Step 1: Add responsive styles for tablet**

```css
@media (max-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .pricing-row { flex-direction: column; align-items: center; }
  .pricing-plan { max-width: 280px; width: 100%; }
  .pricing-plan.highlight { transform: none; }
}
```

- [ ] **Step 2: Add responsive styles for mobile**

```css
@media (max-width: 480px) {
  .hero { padding: 2rem 1rem 0; }
  .hero-title { font-size: 1.8rem; }
  .hero-sub { font-size: 0.9rem; }
  .nav { padding: 0.5rem 1rem; }
  .nav-links { gap: 0.5rem; }
  .nav-link { font-size: 0.6rem; }
  .nav-cta { font-size: 0.65rem; padding: 4px 10px; }
  .metrics { gap: 1rem; padding: 1.5rem 1rem; }
  .metric-number { font-size: 1.5rem; }
  .features-grid { grid-template-columns: 1fr; }
  .calc-box { padding: 1rem; }
}
```

- [ ] **Step 3: Verify responsive layout**

Resize browser to mobile width — all sections should stack and reflow cleanly.

---

### Task 11: Performance and accessibility pass

**Files:**
- Modify: `D:\PROEKT\sellerai\index.html`

- [ ] **Step 1: Add semantic landmarks** — verify `<main>`, `<section>`, `<nav>`, `<footer>` are used correctly. Wrap content sections in `<main>`.

- [ ] **Step 2: Add ARIA attributes** — verify `aria-label` on sections, `role="navigation"` on nav, `role="contentinfo"` on footer, `aria-label` on slider.

- [ ] **Step 3: Verify no JS errors** — open browser console, ensure no errors.

- [ ] **Step 4: Final review of the complete file**

Check: all sections present, no broken links, smooth scroll works, calculator works, animations trigger.

- [ ] **Step 5: Commit final version**

```bash
git add D:\PROEKT\sellerai\index.html
git commit -m "feat: create SellerAI landing page in Apple-style design"
```
