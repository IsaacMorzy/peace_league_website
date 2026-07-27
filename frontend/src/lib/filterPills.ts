/**
 * wireFilterPills — single source of truth for the project-filter-pill pattern.
 * Used by /causes, /gallery, and any future page that wants a category rail with
 * live filtering + aria-live count + role="status" empty-state.
 *
 * Per-page wiring:
 *   const buttons = document.querySelectorAll('[data-filter-cat]');
 *   const cards   = document.querySelectorAll('[data-{whatever}-card]');
 *   wireFilterPills({
 *     buttons,
 *     cards,
 *     countEl:    document.querySelector('[data-...-count]'),
 *     emptyEl:    document.querySelector('[data...-empty]'),
 *     countMessage: (visible, total, cat) => cat === 'All'
 *       ? `Showing all ${total} causes.`
 *       : `Showing ${visible} cause(s) in ${cat}.`,
 *   });
 */
export interface FilterPillsConfig {
  buttons: ArrayLike<Element>;
  cards: ArrayLike<Element>;
  matchAttr?: string;                 // dataset key on cards, default "category"
  countEl?: Element | null;
  emptyEl?: Element | null;
  countMessage: (visible: number, total: number, cat: string) => string;
}

export function wireFilterPills(cfg: FilterPillsConfig): void {
  const { buttons, cards, matchAttr = "category", countEl, emptyEl, countMessage } = cfg;
  if (!buttons.length || !cards.length) return;

  function applyFilter(cat: string): void {
    let visible = 0;
    cards.forEach((raw) => {
      const card = raw as HTMLElement;
      const match = cat === "All" || card.dataset[matchAttr] === cat;
      card.toggleAttribute("hidden", !match);
      if (match) visible++;
    });
    if (countEl) (countEl as HTMLElement).textContent = countMessage(visible, cards.length, cat);
    if (emptyEl) (emptyEl as HTMLElement).hidden = visible > 0;
  }

  buttons.forEach((raw) => {
    const btn = raw as HTMLElement;
    btn.addEventListener("click", () => {
      const cat = btn.dataset.filterCat || "All";
      buttons.forEach((rawOther) => {
        const b = rawOther as HTMLElement;
        const isActive = b.dataset.filterCat === cat;
        b.classList.toggle("bg-primary", isActive);
        b.classList.toggle("text-on-primary", isActive);
        b.classList.toggle("border-primary", isActive);
        b.classList.toggle("bg-canvas", !isActive);
        b.classList.toggle("text-steel", !isActive);
        b.classList.toggle("border-hairline", !isActive);
        b.setAttribute("aria-pressed", isActive ? "true" : "false");
      });
      applyFilter(cat);
    });
  });
}
