/**
 * wireFilterPills — single source of truth for the project-filter-pill pattern.
 * Used by /causes, /gallery, and any future page that wants a category rail with
 * live filtering + aria-live count + role="status" empty-state.
 *
 * Per-page wiring:
 *   wireFilterPills({
 *     buttons: document.querySelectorAll<HTMLButtonElement>("[data-filter-cat]"),
 *     cards:   document.querySelectorAll<HTMLElement>("[data-{whatever}-card]"),
 *     countEl: document.querySelector<HTMLElement>("[data-...-count]"),
 *     emptyEl: document.querySelector<HTMLElement>("[data-...-empty]"),
 *     matchAttr: "category",
 *     countMessage: (visible, total, cat) => cat === "All"
 *       ? `Showing all ${total} causes.`
 *       : `Showing ${visible} cause(s) in ${cat}.`,
 *   });
 *
 * countMessage contract:
 *   visible: number of cards currently matching the active filter
 *   total:   total number of cards (cards.length)
 *   cat:     the active category string ("All" for unfiltered state)
 */
export interface FilterPillsConfig {
  buttons: ArrayLike<HTMLButtonElement>;
  cards: ArrayLike<HTMLElement>;
  matchAttr?: string;
  countEl?: HTMLElement | null;
  emptyEl?: HTMLElement | null;
  countMessage: (visible: number, total: number, cat: string) => string;
}

export function wireFilterPills(cfg: FilterPillsConfig): void {
  const { buttons, cards, matchAttr = "category", countEl, emptyEl, countMessage } = cfg;
  // Both pages have inline guards; preserve the no-op on empty so a page without
  // matching buttons/cards never errors at runtime.
  if (!buttons.length || !cards.length) return;

  function applyFilter(cat: string): void {
    let visible = 0;
    cards.forEach((card) => {
      const match = cat === "All" || card.dataset[matchAttr] === cat;
      card.toggleAttribute("hidden", !match);
      if (match) visible++;
    });
    if (countEl) countEl.textContent = countMessage(visible, cards.length, cat);
    if (emptyEl) emptyEl.hidden = visible > 0;
  }

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const cat = btn.dataset.filterCat || "All";
      buttons.forEach((b) => {
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
