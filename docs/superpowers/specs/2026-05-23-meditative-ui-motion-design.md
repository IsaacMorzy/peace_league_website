# Meditative Motion + Persuasive Layout Refinements (Peace League Website)

Date: 2026-05-23
Owner: OpenCode
Scope: Frontend layout, spacing, motion, and decorative animation system

## Summary
Deepen a meditative browsing experience while strengthening donation persuasion. Keep the existing brand palette and typography, reduce competing motion, and introduce a small, calm animation system (dove drift, heart rise, soft glow) placed only in high-attention zones. Refine layout rhythm and spacing to reduce visual fatigue and guide attention to a clear donation path.

## Goals
- Create a calm, meditative experience with fewer, slower, and more meaningful animations.
- Increase donation persuasion by clarifying the CTA path and calming visual noise.
- Add dove and heart float animations in hero, donation CTA, and footer only.
- Improve layout rhythm (spacing, section banding, alternating header alignment) without changing the brand palette or typography.
- Preserve accessibility (reduced motion, contrast, keyboard) and performance.

## Non-goals
- No changes to brand palette or typography.
- No major information architecture or content rewrites.
- No new backend features or data changes.
- No heavy JS animation frameworks; keep CSS-based motion where possible.

## Design Principles
- Motion must communicate meaning, not decoration noise.
- Calm hierarchy: a few strong signals beat many weak signals.
- Breathing space: spacing and rhythm should encourage slow reading.
- Persuasion is clarity: one primary CTA path and repeated trust cues.
- Performance and accessibility are non-negotiable.

## Motion System
Only three animation archetypes are allowed:

1) Dove Drift
- Purpose: symbolic peace, slow movement behind hero text.
- Behavior: gentle horizontal drift with low-amplitude vertical breathing.
- Duration: 18–28s, linear or ease-in-out.
- Count: 1–2 in hero (desktop), 0–1 on mobile.

2) Heart Rise
- Purpose: warmth and generosity in CTA zones.
- Behavior: slow upward float with subtle opacity change.
- Duration: 22–34s, ease-in-out.
- Count: 1–2 near the donation CTA, 3–5 in footer.

3) Soft Pulse Glow
- Purpose: calm focus around CTA or key trust cue.
- Behavior: low-amplitude opacity pulse.
- Duration: 10–14s.
- Count: 1 per zone max.

Rules and constraints:
- Decorative motion appears only in hero, donation CTA section, and footer.
- Remove or gate overlapping effects (parallax + marquee + bubbles) so only one "ambient" effect runs per page.
- Decorative elements must be aria-hidden and pointer-events-none.
- Reduced motion disables all animation and hides non-essential decorations.
- Mobile reduces counts to prevent visual and performance fatigue.

## Layout and Hierarchy
- Alternate header alignment to avoid repetitive section rhythm:
  - Centered for primary sections (hero, donation CTA).
  - Left-aligned for supporting sections (How We Work, Causes).
- Add subtle section banding (very light surface shift) to segment long pages.
- Increase vertical spacing between dense sections without increasing card size.
- Maintain current grid structure; only adjust spacing and header composition.

## Persuasive Flow
- Maintain a single dominant CTA: "Give Today" in the hero.
- Add one mid-page micro-CTA near "Your Donation Changes Lives."
- Keep a final quiet CTA in the footer.
- Reinforce trust cues near CTAs ("95% to programs", "local-led, transparent").

## Typography and Contrast
- Keep current font stack and scale.
- Slightly increase line-height in long body paragraphs for calm reading.
- Improve contrast for secondary text on light backgrounds without hardening the palette.

## Accessibility and Performance
- All decorative animations must be aria-hidden.
- Respect prefers-reduced-motion and provide static fallback.
- Use transform and opacity only to avoid layout thrash.
- Limit total animated elements per viewport.

## Implementation Scope (Planned Files)
- apps/peace_league_website/frontend/src/styles/global.css
  - Add animation keyframes and classes: dove drift, heart rise, soft glow.
  - Add reduced-motion and mobile gating utilities.
  - Add subtle section banding utilities.
- apps/peace_league_website/frontend/src/layouts/Layout.astro
  - Gate parallax and other ambient effects to hero only.
- apps/peace_league_website/frontend/src/pages/index.astro
  - Apply alternating header alignments and banded sections.
  - Insert dove/heart elements in hero and donation CTA sections.
  - Reduce overlapping ambient effects in dense areas.
- apps/peace_league_website/frontend/src/pages/about.astro
  - Apply calmer rhythm (spacing, banding, header alignment).
  - Remove or reduce excess decorative motion.
- apps/peace_league_website/frontend/src/pages/donate.astro
  - Add calm decorative motion near donation CTA only.
  - Improve section grouping and vertical rhythm.
- apps/peace_league_website/frontend/src/components/Footer.astro
  - Replace bubbles with fewer, slower heart rises.

## Acceptance Criteria
- Decorative motion appears only in hero, donation CTA, and footer.
- Prefers-reduced-motion disables all decorative animations.
- The donation CTA path is clear and visually dominant.
- Long pages feel calmer, with visible section segmentation.
- No new accessibility warnings or performance regressions.

## Risks and Mitigations
- Risk: Too many animations still feel busy.
  - Mitigation: strict count caps and reduced-motion gating.
- Risk: Banding makes sections feel disjointed.
  - Mitigation: use subtle, low-contrast banding and consistent spacing.
- Risk: Secondary text becomes too light on bright screens.
  - Mitigation: minor contrast bump for text-steel contexts.
