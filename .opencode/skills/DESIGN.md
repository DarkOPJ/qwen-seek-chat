---
name: Auralis Precision
colors:
  surface: '#f9f9f7'
  surface-dim: '#dadad8'
  surface-bright: '#f9f9f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f2'
  surface-container: '#eeeeec'
  surface-container-high: '#e8e8e6'
  surface-container-highest: '#e2e3e1'
  on-surface: '#1a1c1b'
  on-surface-variant: '#4c4546'
  inverse-surface: '#2f3130'
  inverse-on-surface: '#f1f1ef'
  outline: '#7e7576'
  outline-variant: '#cfc4c5'
  surface-tint: '#5e5e5e'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1b1b1b'
  on-primary-container: '#848484'
  inverse-primary: '#c6c6c6'
  secondary: '#5e5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e1dfdf'
  on-secondary-container: '#626262'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#1b1b1b'
  on-tertiary-container: '#848484'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c6'
  on-primary-fixed: '#1b1b1b'
  on-primary-fixed-variant: '#474747'
  secondary-fixed: '#e4e2e2'
  secondary-fixed-dim: '#c7c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#464747'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c6'
  on-tertiary-fixed: '#1b1b1b'
  on-tertiary-fixed-variant: '#474747'
  background: '#f9f9f7'
  on-background: '#1a1c1b'
  surface-variant: '#e2e3e1'
  surface-panel: '#F3F2EF'
  surface-card: '#FCFCFB'
  border-subtle: '#E7E7E4'
  accent-emerald: '#10B981'
  neural-indigo: '#6366F1'
  neural-purple: '#A855F7'
  neural-rose: '#FB7185'
typography:
  h1:
    fontFamily: Geist
    fontSize: 84px
    fontWeight: '600'
    lineHeight: '1.05'
    letterSpacing: -0.04em
  h1-mobile:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.03em
  h2:
    fontFamily: Geist
    fontSize: 64px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.03em
  h3:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  body-lg:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: -0.01em
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.1em
  mono-metrics:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: '0'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 32px
  margin: 32px
  section-gap-desktop: 180px
  section-gap-mobile: 80px
  max-width: 1280px
---

## Brand & Style
Auralis Precision is a sophisticated, technology-forward design system that blends **Modern Corporate** reliability with **Glassmorphism** and **Neural Aesthetics**. The brand personality is analytical, clean, and highly organized, evoking a sense of "engineered precision" for high-end AI and developer tools.

The visual style relies on a "Soft-Tech" approach: using a pristine, warm-neutral foundation punctuated by vibrant, blurred "neural orbs" and glassmorphic widgets. It prioritizes clarity and high-quality typography to convey institutional trust while using motion and depth to signal innovation.

## Colors
The palette is rooted in a "Warm White" spectrum, moving away from sterile grays to create a more premium, editorial feel. 

- **Primary Canvas:** The background uses `#F7F7F5`, providing a soft, non-reflective base.
- **Tonal Layering:** Deep depth is achieved through subtle shifts to `#F3F2EF` (Panels) and `#FCFCFB` (Cards).
- **Core Action:** Pure Black (`#000000`) is used for primary actions and high-contrast typography, ensuring maximum legibility.
- **Semantic Accents:** Emerald is used exclusively for "Live" or "Active" states. Neural gradients (Indigo, Purple, Rose) are reserved for data visualizations and background atmospheric elements to represent AI activity.

## Typography
The system utilizes **Geist** for its technical yet approachable character. 

- **Display Hierarchy:** Large-scale headings use tight line-heights and negative letter-spacing to create a "locked-up" editorial look.
- **Body & Precision:** Body text maintains generous line-height (1.5-1.6) for readability. 
- **Monospace:** For technical metrics, synthesis values, and timestamps, a monospaced font (like JetBrains Mono or Geist Mono) is introduced to emphasize the "Neural Engine" aspect of the brand.

## Layout & Spacing
Auralis uses a **Fixed Grid** model for desktop, centered within a 1280px container.

- **The 8px Rhythm:** All padding, margins, and component heights must be multiples of 8px.
- **Sectional Breathing:** Significant vertical whitespace (140px-180px) is used to separate high-level concepts, forcing focus on one module at a time.
- **Responsive Behavior:** 
  - **Desktop:** 12-column grid with 32px gutters.
  - **Tablet:** 8-column grid with 24px gutters.
  - **Mobile:** 4-column grid with 16px margins; section gaps reduce to 80px to maintain momentum.

## Elevation & Depth
The system employs **Tonal Layering** and **Glassmorphism** instead of traditional shadows to establish hierarchy.

- **Base Level:** `#F7F7F5` (Background).
- **Secondary Level:** `#F3F2EF` with a 1px solid border (`#E7E7E4`) creates a recessed "well" effect for large feature panels.
- **Floating Level (Glass):** Used for controls and overlay widgets. Requires `backdrop-blur-3xl` and a semi-transparent white background (`rgba(255,255,255,0.25)`). It features a distinct internal "inner glow" via a 1px inset white border to simulate light catching the edge of the glass.
- **Shadows:** Only used sparingly on interactive elements like the "Play" button, utilizing a large blur radius with very low opacity (`black/5%`) to prevent a "dirty" look on the warm background.

## Shapes
Auralis uses a tiered rounding strategy to communicate "Soft-Precision."

- **Standard Components:** Buttons and small chips are **Pill-shaped (Full)**. This provides a friendly, touchable contrast to the structured grid.
- **Containers:** Small cards use `1rem` (16px), while large hero panels and glass containers use `1.75rem - 2rem` (28px-32px).
- **Interactive States:** Hovering over cards should trigger a subtle shadow expansion or border-color shift, maintaining the large corner radius.

## Components
- **Buttons:** 
  - *Primary:* Black background, white text, pill-shaped, medium weight.
  - *Secondary:* Transparent with a 1px border (`outline`), pill-shaped.
- **Chips & Tabs:** Use a "Segmented Control" style. A pill-shaped container (`surface-container-low`) holds individual pill buttons. The active state is a white card with a subtle shadow.
- **Neural Widgets:** High-complexity components (like the spectral visualizer) should be housed in glassmorphic containers. Use thin, rounded bars for data visualization with vertical gradients.
- **Cards:** Feature cards should be minimal with a top-left icon and bottom-left typography. Use background gradients (5-10% opacity) to indicate different product zones (e.g., Indigo for Editor, Emerald for Transcript).
- **Inputs:** Text fields should be clean, using the same corner radius as cards but with a slightly more prominent border when focused.