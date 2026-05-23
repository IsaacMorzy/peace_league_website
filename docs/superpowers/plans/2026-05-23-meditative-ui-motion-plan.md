# Meditative UI Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deepen a meditative browsing experience and sharpen donation persuasion by refining layout rhythm and introducing a calm, limited motion system (dove drift, heart rise, soft glow) only in hero, donation CTA, and footer zones.

**Architecture:** Define a small set of CSS motion utilities in `global.css`, apply them sparingly to decorative elements, and reduce competing animations in `index.astro`, `about.astro`, `donate.astro`, and `Footer.astro`. Parallax is gated to the home hero only; all other ambient effects are removed or reduced.

**Tech Stack:** Astro 6, Tailwind CSS v4, plain CSS animations

---

## File Map
- Modify: `apps/peace_league_website/frontend/src/styles/global.css` — new motion utilities, section banding, reduced-motion gating
- Modify: `apps/peace_league_website/frontend/src/layouts/Layout.astro` — parallax gating, remove confetti hook
- Modify: `apps/peace_league_website/frontend/src/pages/index.astro` — hero/CTA decorations, header alignment, remove marquee animation
- Modify: `apps/peace_league_website/frontend/src/pages/about.astro` — reduce hero motion, remove ring glow animation, spacing rhythm
- Modify: `apps/peace_league_website/frontend/src/pages/donate.astro` — reduce hero/form/M‑Pesa animations, add calm decorations
- Modify: `apps/peace_league_website/frontend/src/components/Footer.astro` — remove bubbles, reduce motion, add calmer hearts

---

### Task 1: Add Meditative Motion Utilities + Banding

**Files:**
- Modify: `apps/peace_league_website/frontend/src/styles/global.css`

- [ ] **Step 1: Add decorative motion utilities and keyframes**

Add the following block near the existing animation utilities (after the bubble animation section is fine):

```css
/* ── Meditative Decorative Motion ── */
.motion-decor {
  position: absolute;
  pointer-events: none;
  z-index: 1;
  opacity: 0.45;
}

.dove-drift {
  animation: dove-drift 26s ease-in-out infinite;
}

.heart-rise {
  animation: heart-rise 30s ease-in-out infinite;
  color: rgba(245, 158, 11, 0.28);
}

.soft-glow {
  border-radius: 999px;
  background: radial-gradient(circle, rgba(0, 212, 164, 0.18) 0%, rgba(0, 212, 164, 0) 70%);
  animation: soft-glow 12s ease-in-out infinite;
  filter: blur(2px);
}

@keyframes dove-drift {
  0% { transform: translate3d(0, 0, 0) scale(0.9); opacity: 0; }
  20% { opacity: 0.4; }
  50% { transform: translate3d(30px, -12px, 0) scale(1); opacity: 0.55; }
  80% { opacity: 0.35; }
  100% { transform: translate3d(60px, -18px, 0) scale(0.95); opacity: 0; }
}

@keyframes heart-rise {
  0% { transform: translate3d(0, 20px, 0) scale(0.6); opacity: 0; }
  20% { opacity: 0.5; }
  70% { opacity: 0.35; }
  100% { transform: translate3d(0, -140px, 0) scale(1); opacity: 0; }
}

@keyframes soft-glow {
  0%, 100% { opacity: 0.25; }
  50% { opacity: 0.55; }
}
```

- [ ] **Step 2: Add subtle section banding utility**

Add a small banding utility near other layout utilities:

```css
.section-band {
  background: linear-gradient(180deg, var(--color-canvas) 0%, var(--color-surface-soft) 100%);
}
```

- [ ] **Step 3: Gate decorative motion on small screens and reduced motion**

Add this media rule near other global media blocks and extend the reduced-motion block at the end:

```css
@media (max-width: 640px) {
  .motion-decor {
    display: none !important;
  }
}
```

Extend the existing prefers-reduced-motion block (near the end):

```css
  .motion-decor,
  .soft-glow {
    display: none !important;
  }
```

- [ ] **Step 4: Build check**

Run: `pnpm -C frontend build`

Expected: `astro build` completes without errors.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/styles/global.css
git commit -m "style: add meditative motion utilities"
```

---

### Task 2: Gate Parallax to Home Hero + Remove Confetti Hook

**Files:**
- Modify: `apps/peace_league_website/frontend/src/layouts/Layout.astro`

- [ ] **Step 1: Gate parallax to hero sections marked with data attribute**

Replace the parallax block in the inline script with the following:

```js
// Defer parallax init until idle — guard against missing elements
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => {
    const parallaxTargets = document.querySelectorAll('.hero-gradient[data-parallax="true"]');
    if (!parallaxTargets.length) return;

    let parallaxTicking = false;
    window.addEventListener('scroll', () => {
      if (!parallaxTicking) {
        requestAnimationFrame(() => {
          parallaxTargets.forEach(section => {
            const speed = 0.15;
            const y = section.getBoundingClientRect().top;
            const shapes = section.querySelectorAll('.parallax-bg-shape');
            const dots = section.querySelectorAll('.parallax-dot-grid');
            if (!shapes.length && !dots.length) return;
            shapes.forEach(s => { s.style.transform = `translateY(${y * speed}px)`; });
            dots.forEach(d => { d.style.transform = `translateY(${y * speed * 0.5}px)`; });
          });
          parallaxTicking = false;
        });
        parallaxTicking = true;
      }
    }, { passive: true });
  });
}
```

- [ ] **Step 2: Remove the confetti hook entirely**

Delete the `window.createConfetti` function in `Layout.astro` (the block starting with `window.createConfetti = (element) => { ... }`). No replacement is needed.

- [ ] **Step 3: Build check**

Run: `pnpm -C frontend build`

Expected: build completes without errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/layouts/Layout.astro
git commit -m "refactor: gate parallax to home hero"
```

---

### Task 3: Home Page — Hero + CTA Decorations, Calm Headers, Remove Marquee Animation

**Files:**
- Modify: `apps/peace_league_website/frontend/src/pages/index.astro`

- [ ] **Step 1: Gate parallax to home hero and add meditative decorations**

Update the hero section opening tag and add a decorative layer:

```astro
<section id="hero-section" data-parallax="true" class="relative text-white hero-gradient overflow-hidden min-h-[85vh] flex items-center">
  <!-- existing background layers -->
  <div class="absolute inset-0 z-[2] pointer-events-none" aria-hidden="true">
    <span class="motion-decor dove-drift" style="left:12%; top:18%; font-size:1.75rem;">&#x1F54A;</span>
    <span class="motion-decor heart-rise" style="left:72%; bottom:-10%; font-size:1rem;">&#x2764;</span>
    <span class="motion-decor soft-glow" style="left:58%; top:30%; width:220px; height:220px;"></span>
  </div>
```

- [ ] **Step 2: Make "Our Causes" and "How We Work" headers left-aligned**

For the “Our Causes” section header block, replace `text-center` with `text-left` and limit width:

```astro
<h2 class="scroll-reveal text-2xl sm:text-3xl lg:text-4xl font-semibold leading-[1.2] tracking-[-0.5px] text-ink text-left mb-4 max-w-2xl">Our Causes</h2>
<p class="scroll-reveal text-left text-lg text-steel max-w-2xl mb-14">Every cause is community-driven, locally led, and fully transparent. Here is where your support goes.</p>
```

Repeat the same alignment change for “How We Work”:

```astro
<h2 class="scroll-reveal text-2xl sm:text-3xl lg:text-4xl font-semibold leading-[1.2] tracking-[-0.5px] text-ink text-left mb-4 max-w-2xl">How We Work</h2>
<p class="scroll-reveal text-lg text-steel text-left max-w-2xl mb-14">A proven process rooted in listening, local leadership, and lasting change.</p>
```

- [ ] **Step 3: Add subtle decoration near donation CTA block**

Inside the “Your Donation Changes Lives” section wrapper, add:

```astro
<div class="absolute inset-0 pointer-events-none" aria-hidden="true">
  <span class="motion-decor heart-rise" style="left:18%; bottom:-6%; font-size:0.95rem;">&#x2764;</span>
  <span class="motion-decor dove-drift" style="right:12%; top:12%; font-size:1.25rem;">&#x1F54A;</span>
</div>
```

If the section wrapper is not `relative`, add `relative` to the section class.

- [ ] **Step 4: Remove marquee animation from partner logos**

Update the logos row to remove the animated class:

```astro
<div class="flex gap-6 whitespace-nowrap items-center opacity-30">
```

(Remove `animate-marquee` and `logo-marquee` from this container.)

- [ ] **Step 5: Add a calm decorative layer to the final CTA**

Inside the final hero CTA section (Peace Begins With You), add a single dove/heart:

```astro
<div class="absolute inset-0 pointer-events-none z-[2]" aria-hidden="true">
  <span class="motion-decor dove-drift" style="left:8%; top:22%; font-size:1.5rem;">&#x1F54A;</span>
  <span class="motion-decor heart-rise" style="right:14%; bottom:-12%; font-size:0.9rem;">&#x2764;</span>
</div>
```

- [ ] **Step 6: Build check**

Run: `pnpm -C frontend build`

Expected: build completes without errors.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/pages/index.astro
git commit -m "style: calm home hero and section rhythm"
```

---

### Task 4: About Page — Reduce Hero Motion, Calm Sections, Remove Ring Glow

**Files:**
- Modify: `apps/peace_league_website/frontend/src/pages/about.astro`

- [ ] **Step 1: Remove parallax layer and reduce hero hearts**

Replace the hero decorations with a minimal set (keep only two elements):

```astro
<section class="hero-gradient text-white py-16 lg:py-20 relative overflow-hidden">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
    <h1 class="text-3xl sm:text-4xl lg:text-5xl font-semibold leading-[1.10] tracking-tight">About Peace League Africa</h1>
    <p class="mt-4 text-lg text-white/80 max-w-2xl">From a single peace workshop in 2015 to a movement spanning 12 countries — we replace division with dialogue, poverty with opportunity, and despair with hope.</p>
  </div>
  <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
    <span class="motion-decor dove-drift" style="left:10%; top:20%; font-size:1.5rem;">&#x1F54A;</span>
    <span class="motion-decor heart-rise" style="right:14%; bottom:-12%; font-size:0.95rem;">&#x2764;</span>
  </div>
</section>
```

Remove the old `<div class="parallax-layer">` block and the existing `.about-float-heart` spans.

- [ ] **Step 2: Apply section banding to break up long content**

Add `section-band` to one or two dense sections (for example, the Values section wrapper):

```astro
<section class="py-16 bg-surface section-band">
```

Use the banding sparingly (1–2 sections) to avoid visual noise.

- [ ] **Step 3: Remove animated ring glow in Chapters**

In the Chapters SVG, remove the `animate-ring-glow` class:

```astro
<circle cx="100" cy="100" r="85" stroke-width="1" stroke-dasharray="4 4" opacity="0.35" filter="url(#ring-glow)" />
```

- [ ] **Step 4: Build check**

Run: `pnpm -C frontend build`

Expected: build completes without errors.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/about.astro
git commit -m "style: calm about hero and sections"
```

---

### Task 5: Donate Page — Simplify Motion + Add Calm Decorations

**Files:**
- Modify: `apps/peace_league_website/frontend/src/pages/donate.astro`

- [ ] **Step 1: Remove parallax from hero and add calm decorations**

Replace the hero background layer with minimal decor:

```astro
<section class="hero-gradient hero-pattern text-white py-16 lg:py-20">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="text-3xl sm:text-4xl lg:text-5xl font-semibold leading-[1.10] tracking-tight">Your Gift Rebuilds Communities</h1>
    <p class="mt-4 text-lg text-white/70 max-w-2xl">$50 trains a peace teacher. $25 provides clean water for a family. $500 launches a youth mentorship program. Every dollar goes to peace-building across 12 African countries.</p>
  </div>
  <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
    <span class="motion-decor dove-drift" style="left:12%; top:16%; font-size:1.4rem;">&#x1F54A;</span>
    <span class="motion-decor heart-rise" style="right:16%; bottom:-10%; font-size:0.9rem;">&#x2764;</span>
  </div>
</section>
```

Remove the existing `<div class="parallax-layer">` block.

- [ ] **Step 2: Reduce animation on the form container**

Remove `animate-in` classes from the form container to calm entry motion:

```astro
<div class="scroll-reveal bg-canvas/80 backdrop-blur-xl rounded-2xl border border-hairline p-6 md:p-8 shadow-[0_8px_32px_rgba(0,0,0,0.08)] relative overflow-hidden">
```

- [ ] **Step 3: Simplify M‑Pesa waiting animations**

Remove these animation classes:

```astro
<!-- remove mpesa-screen-pulse from the rect -->
<rect x="25" y="40" width="70" height="8" rx="2" fill="var(--color-accent)" opacity="0.15"/>

<!-- remove animate-glow from timer ring -->
<circle id="mpesa-timer-ring" cx="36" cy="36" r="30" fill="none" stroke="var(--color-accent)" stroke-width="5" stroke-linecap="round" stroke-dasharray="188.5" stroke-dashoffset="0" class="transition-all duration-500 ease-linear"/>

<!-- remove animate-float-slow from the phone icon -->
<svg class="w-8 h-8 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">...</svg>
```

- [ ] **Step 4: Remove confetti triggers in the script**

Delete any calls to `window.createConfetti(...)` in the donation script. For example:

```js
// Remove these lines
window.createConfetti(submitButton);
window.createConfetti(document.getElementById('mpesa-success'));
```

- [ ] **Step 5: Build check**

Run: `pnpm -C frontend build`

Expected: build completes without errors.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/pages/donate.astro
git commit -m "style: calm donate motion and hero"
```

---

### Task 6: Footer — Remove Bubbles, Reduce Motion, Add Calm Hearts

**Files:**
- Modify: `apps/peace_league_website/frontend/src/components/Footer.astro`

- [ ] **Step 1: Remove bounce and heartbeat animations**

Update these lines:

```astro
<span class="inline-block text-sm">&uarr;</span>
```

```astro
<span class="inline-block w-2 h-2 rounded-full bg-accent"></span>
```

- [ ] **Step 2: Make the flags row static**

Remove the marquee animation class:

```astro
<div class="flex gap-8 whitespace-nowrap items-center opacity-30">
```

- [ ] **Step 3: Remove bubble divs and replace hearts with calm motion**

Delete all `.footer-bubble-up` and `.footer-bubble-up-slow` divs. Replace the five heart spans with two or three calmer hearts using the new global class:

```astro
<span class="motion-decor heart-rise" style="left:18%; bottom:-6%; font-size:0.95rem;">&#x2764;</span>
<span class="motion-decor heart-rise" style="left:52%; bottom:-8%; font-size:1.05rem; animation-delay:6s;">&#x2764;</span>
<span class="motion-decor heart-rise" style="right:16%; bottom:-10%; font-size:0.9rem; animation-delay:3s;">&#x2764;</span>
```

- [ ] **Step 4: Remove the inline `<style>` block at the bottom**

Delete the inline `@keyframes footer-heart-rise` block (the `<style>` tag in Footer.astro). The global `.heart-rise` class now provides motion.

- [ ] **Step 5: Build check**

Run: `pnpm -C frontend build`

Expected: build completes without errors.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/Footer.astro
git commit -m "style: calm footer motion"
```

---

### Task 7: Final Verification

**Files:**
- No new files; verify the full build

- [ ] **Step 1: Full build**

Run: `pnpm -C frontend build`

Expected: build completes without errors.

- [ ] **Step 2: Visual spot check**

Open the following pages and confirm calm motion and CTA focus:
- `/` (home hero + donation CTA + footer)
- `/about` (hero + chapters ring static)
- `/donate` (hero + form + M‑Pesa waiting)

- [ ] **Step 3: Commit any remaining adjustments**

```bash
git add frontend/src/pages/index.astro frontend/src/pages/about.astro frontend/src/pages/donate.astro frontend/src/components/Footer.astro
git commit -m "style: finalize meditative UI motion"
```

---

## Self-Review Checklist
- All decorative motion is confined to hero/CTA/footer zones.
- No confetti or high-energy motion remains.
- Parallax only runs on the home hero (`data-parallax="true"`).
- Reduced motion hides all decorative elements.
- Build completes without errors.
