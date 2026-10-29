---
name: The Gift Edit
colors:
  surface: '#fff8f6'
  surface-dim: '#e2d8d6'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fcf1ef'
  surface-container: '#f6ecea'
  surface-container-high: '#f0e6e4'
  surface-container-highest: '#eae0de'
  on-surface: '#1f1b1a'
  on-surface-variant: '#514345'
  inverse-surface: '#352f2e'
  inverse-on-surface: '#f9eeec'
  outline: '#837374'
  outline-variant: '#d5c2c3'
  surface-tint: '#825057'
  primary: '#825057'
  on-primary: '#ffffff'
  primary-container: '#c88d94'
  on-primary-container: '#51272e'
  inverse-primary: '#f6b6bd'
  secondary: '#635d57'
  on-secondary: '#ffffff'
  secondary-container: '#eae1d8'
  on-secondary-container: '#69635c'
  tertiary: '#6e5958'
  on-tertiary: '#ffffff'
  tertiary-container: '#b09795'
  on-tertiary-container: '#42302f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd9dd'
  primary-fixed-dim: '#f6b6bd'
  on-primary-fixed: '#340f16'
  on-primary-fixed-variant: '#673940'
  secondary-fixed: '#eae1d8'
  secondary-fixed-dim: '#cdc5bd'
  on-secondary-fixed: '#1f1b16'
  on-secondary-fixed-variant: '#4b4640'
  tertiary-fixed: '#f9dcda'
  tertiary-fixed-dim: '#dbc0be'
  on-tertiary-fixed: '#271817'
  on-tertiary-fixed-variant: '#554241'
  background: '#fff8f6'
  on-background: '#1f1b1a'
  surface-variant: '#eae0de'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 3.5rem
    fontWeight: '400'
    lineHeight: 4rem
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 2.25rem
    fontWeight: '400'
    lineHeight: 2.75rem
    letterSpacing: -0.01em
  headline-xl:
    fontFamily: Playfair Display
    fontSize: 2.5rem
    fontWeight: '500'
    lineHeight: 3rem
    letterSpacing: -0.01em
  headline-xl-mobile:
    fontFamily: Playfair Display
    fontSize: 1.75rem
    fontWeight: '500'
    lineHeight: 2.25rem
  headline-md:
    fontFamily: Playfair Display
    fontSize: 1.75rem
    fontWeight: '500'
    lineHeight: 2.25rem
  headline-sm:
    fontFamily: Playfair Display
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.9375rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.25rem
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.04em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.06em
  label-caps:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.6875rem
    fontWeight: '700'
    lineHeight: 0.875rem
    letterSpacing: 0.12em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 3rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system embodies an editorial, high-touch luxury bespoke gifting experience tailored for personalized gift curation. The visual character merges delicate warmth with high-end editorial restraint—evoking ribbon-tied rigid keepsake boxes, hand-poured botanical candles, debossed monograms, and custom calligraphy. 

The aesthetic is a union of **Editorial Elegance** and **Warm Tactile Softness**:
- **Atmosphere**: Warm, intimate, romantic, and curated. It feels like an artisanal atelier rather than an industrial e-commerce storefront.
- **Visual Tenets**: Generous negative space, whisper-soft blush surfaces, illuminated card containers, crisp editorial type hierarchies, and fine-line metallic/dusty accents.
- **Target Audience**: Modern gift givers seeking curated, personal care packages, bridal hampers, and custom birthday keepsakes with an unapologetically elevated, feminine sensibility.

## Colors

The palette balances airy warmth with sharp, readable contrast. The core canvas relies on warm creams and crisp whites, grounding interactions with deep espresso typography instead of stark pitch black.

- **Primary (`#c88d94`)**: Dusty Mauve / Rose Gold. Anchors key interactive moments, primary CTAs, active badge borders, and delicate decorative rules.
- **Secondary (`#ede4db`)**: Warm Sand / Pale Alabaster. Serves as structural framing, quiet borders, and soft card container backgrounds.
- **Tertiary (`#eed2d0`)**: Soft Powder Blush. Utilized for subtle interactive hover fills, ribbon tags, and warm celebratory chips.
- **Neutral (`#2b2625`)**: Warm Deep Charcoal Espresso. Supplies high-contrast, deeply legible editorial text while sustaining a warmer, softer tone than pure `#000000`.
- **Canvas & Surface System**:
  - `canvas-default`: `#fdfbf7` (Warm Cream base).
  - `surface-elevated`: `#ffffff` (Crisp White cards to contrast against warm cream).
  - `surface-subtle`: `#f7dcdb` with 30% alpha for ambient glow panels.

## Typography

The typographical rhythm relies on a classical editorial contrast:
- **Display & Headlines (`Playfair Display`)**: Conveys romance, heritage, and refined luxury. Use normal to medium weights (`400`–`500`) to let characterful serif flourishes shine without appearing heavy.
- **Body & Functional UI (`Plus Jakarta Sans`)**: Delivers friendly, contemporary clarity. Geometric contours mirror the roundness of the components while retaining razor-sharp legibility at small sizes.
- **Micro-Copy & Eyebrows**: Utilize `label-caps` in uppercase styling with generous tracking (`0.12em`) for curation tags, step indicators, and artisan details (e.g., "BESPOKE CURATION", "BOX NO. 04").

## Layout & Spacing

A structured, fluid 12-column grid anchors the layout on desktop, condensing down to 8 columns on tablet and 4 columns on mobile. 

- **Grid Principles**:
  - Desktop (1200px+): 12 columns, 1.5rem gutter, 3rem canvas margin, bounded by a max-width container of 1320px to sustain intimate proportions.
  - Tablet (768px–1199px): 8 columns, 1.25rem gutter, 2rem margin.
  - Mobile (under 768px): 4 columns, 1rem gutter, 1.25rem margin.
- **Vertical Rhythm**:
  - Ample vertical margins (`space-xl` to `3rem`) separate thematic gift collections, sustaining a relaxed, boutique catalog pace.
  - Component internals use `space-md` for standard card padding and `space-lg` for expansive feature cards.

## Elevation & Depth

This design system avoids dark or harsh drop shadows, replacing them with warm, radiant luminescence:

- **Ambient Blush Glow**: Shadows use dusty rose and warm sand hues rather than neutral grays. 
  - *Standard Depth*: `0 8px 24px -4px rgba(200, 141, 148, 0.08), 0 2px 6px 0 rgba(43, 38, 37, 0.03)`.
  - *Floating/Drawer Depth*: `0 20px 40px -8px rgba(200, 141, 148, 0.14), 0 4px 12px 0 rgba(43, 38, 37, 0.04)`.
- **Ghost Borders**: Elements receive an ultra-fine border (`1px solid rgba(200, 141, 148, 0.18)` or `1px solid #ede4db`) to produce tailored, tactile containment reminiscent of rigid box bevels.
- **Glassmorphic Accents**: Sticky navigation ribbons and drawer overlays utilize soft translucent cream backdrops (`rgba(253, 251, 247, 0.85)` with a `16px` backdrop-blur filter).

## Shapes

The shape vocabulary is hyper-soft, pill-accented, and organic, directly matching the tactile nature of ribbons, wax seal contours, and plush packaging.

- **Base Corner Radius**: Pill tokens (`roundedness: 3`) drive interactive states:
  - Buttons, chips, search bars, and filter toggles: Fully pill-shaped (`9999px` / `rounded-full`).
  - Cards, modals, and product containers: `1.5rem` (`rounded-2xl`) scaling up to `2rem` (`rounded-3xl`) on hero presentation panels.
  - Micro-selectors (swatches, image thumbnails): `0.75rem` soft squares with organic curvature.

## Components

### Buttons
- **Primary Button**: Solid dusty mauve (`#c88d94`) with crisp white (`#ffffff`) text. Full pill curvature, `padding: 0.75rem 2rem`. Subtle hover transition to a deeper warm mauve (`#b87c84`) accompanied by an enhanced blush glow.
- **Secondary Button**: Crisp white fill, `1.5px` border in `#ede4db`, text in `#2b2625`. Hover state blends to a pale blush surface (`#eed2d0` at 25% opacity) with border color shifting to `#c88d94`.
- **Tertiary / Text Button**: Understated label text (`label-lg`) in deep charcoal with an animated hairline underline in dusty mauve that expands on hover.

### Badges & Chips
- **Status / Tag Chips**: Pill-shaped with a delicate warm sand border (`#ede4db`), filled with translucent blush (`rgba(247, 220, 219, 0.45)`). Font styled in `label-md` with neutral charcoal text.
- **Selection Chips (Box Customizer)**: Toggled states shift from `#ffffff` surface to solid dusty mauve borders with a checkmark badge.

### Form Inputs & Textareas
- **Text Inputs**: Crisp white background, `1px solid #ede4db` border, pill shape (`rounded-full`) for single-line inputs and `rounded-2xl` for message text areas. Placeholder text in `#2b2625` with 40% opacity. Focus state employs a glowing `1.5px` border in `#c88d94` without harsh browser rings.
- **Custom Gift Card Input**: Styled as a physical card inset—warm cream canvas (`#fdfbf7`), faint inner border, and script-like visual hints for personalized calligraphy messages.

### Checkboxes & Radio Buttons
- **Selection Controls**: Custom circular rings. Unselected state is a thin `#dfd3c3` border. Selected state fills with `#c88d94`, nesting a crisp white center dot or check.

### Product & Curation Cards
- **Curated Box Cards**: Crisp white elevated surfaces with `rounded-2xl` geometry. Subtle perimeter line (`1px solid #ede4db`) and ambient pink-beige shadow. Top image display maintains an inset margin with a softened inner border.
- **Item Add-to-Box Step Card**: Compact, tactile cards showing thumbnail imagery, artisan title, and a discrete "+" circular button that turns into an active check pill upon addition.

### Bespoke Domain Components
- **Gift Box Step Builder Ribbon**: Horizontal sticky stepper with soft cream glassmorphism, tracking the packaging, card choice, and inner luxury contents.
- **Wax Seal Badge**: Circular seal stamp graphic overlay (`rgba(200, 141, 148, 0.9)`) used as an authenticity marker for hand-packed gifts.