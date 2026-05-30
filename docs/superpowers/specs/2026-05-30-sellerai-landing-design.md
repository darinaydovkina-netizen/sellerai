# SellerAI Landing Page — Design Spec

## Style Direction
**Apple.com-inspired, light theme, conversion-focused.**

Approved by user after iterating through 8 design directions.

## Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | #FFFFFF | Page background |
| `--bg-secondary` | #f5f5f7 | Card/section backgrounds |
| `--text-primary` | #1d1d1f | Headings, primary text |
| `--text-secondary` | #86868b | Subtext, metadata |
| `--accent-blue` | #0071e3 | Primary CTA buttons, links (Apple-blue) |
| `--accent-orange` | #FF4D00 | Eyebrow labels, "Популярное" badges |
| `--border` | rgba(0,0,0,0.04) | Subtle dividers |
| `--card-bg` | #f5f5f7 | Feature cards |

## Typography
- **Font stack:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, sans-serif
- **Hero heading:** 3rem, weight 700, letter-spacing -0.03em
- **Section headings:** 1.3-1.5rem, weight 700
- **Body text:** 1.15rem (hero sub), 0.85rem (secondary), 0.75rem (tertiary)
- **Eyebrow:** 0.7-0.8rem, weight 600, uppercase, letter-spacing 0.05em

## Layout Structure

### Navigation
- Sticky, white with 0.95 opacity + bottom border
- Logo left, nav links center-right, CTA button right
- CTA: blue pill (#0071e3, border-radius 980px)

### Hero Section
- Centered, max-width ~600px
- Eyebrow: "ИИ-ПОМОЩНИК ДЛЯ ПРОДАВЦОВ" in accent-orange
- Headline: "Контент за 3 секунды"
- Sub: brief description (1 sentence, mentions WB/Ozon/ЯМ)
- CTA: "Попробовать бесплатно" + "Подробнее ›"
- Trust line: "7 дней бесплатно. Без привязки карты."

### Product Visual
- Large mockup below hero, max-width 650px
- Background gradient #f5f5f7 → #e8e8ed, rounded corners 20px
- Interface preview showing: input field, 2 result tiles with CTR improvement
- Green CTR badge (+176%) — conversion trigger

### Metrics Strip
- 4 stats in one row: 3с, +40%, 4.9★, 450+
- Large numbers (2rem, weight 700), small labels (#86868b)

### Features Grid (2×3)
- Cards with #f5f5f7 background, border-radius 14px
- Each card: title + short description
- Section eyebrow + "6 инструментов" heading

### Pricing Section
- Simple text layout (cards NOT approved — user rejected card-heavy designs)
- Starter: 499 ₽/мес · 50 генераций
- Business: 999 ₽/мес · 200 генераций (highlighted)
- Pro: 1 990 ₽/мес · безлимит

### CTA Section
- Heading + sub + blue pill button
- Minimal, no urgency pressure

### Footer
- Copyright + links (all in small #86868b text)

## Design Principles
1. **Minimum text** — every word earns its place
2. **Product-first** — interface visual is the hero, not decorative graphics
3. **Apple spacing** — generous whitespace, no crowding
4. **One primary CTA per section** — blue pill, border-radius 980px
5. **No glassmorphism** — flat, clean, 2D

## Responsive Notes
- Mobile: stack elements vertically, reduce heading font size
- Tablet: maintain 2-column grid, reduce spacing
- Desktop: max-width ~1100px centered

## Conversion Triggers
1. Social proof in hero-sub (mentions marketplaces)
2. Metrics strip showing speed/CTR/users
3. Before/after CTR comparison in product mockup (+176%)
4. "7 дней бесплатно. Без привязки карты." — risk reversal
5. Blue CTA buttons (high contrast, Apple-trusted color)

## Implementation
- Single file: index.html (HTML + CSS + JS)
- Google Fonts: Inter (via CDN)
- No external dependencies
- Vanilla JS for calculator (per original spec)
- Intersection Observer for scroll animations
