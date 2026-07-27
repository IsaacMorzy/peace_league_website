/**
 * Locale-aware KES currency formatting. Always emits with the "KES " prefix
 * and a thousands separator. Avoids the unregulated KSh prefix to keep
 * canonical across donor receipts and Stripe payment notifications.
 *
 * Examples:
 *   formatKes(0)        -> "KES 0"
 *   formatKes(1950000)  -> "KES 1,950,000"
 *   formatKes(11050000) -> "KES 11,050,000"
 */
export function formatKes(n: number): string {
  return "KES " + Number(n || 0).toLocaleString("en-US");
}

/**
 * Clamp-safe progress percentage for funding progress bars. Always returns
 * a finite number in the [0, 100] range, even when goal is 0 or raised
 * overshoots goal.
 *
 * Examples:
 *   progressPct(1950000, 6500000) -> 30
 *   progressPct(0, 100)          -> 0
 *   progressPct(200, 100)        -> 100
 */
export function progressPct(raised: number, goal: number): number {
  if (!goal || goal <= 0) return 0;
  return Math.min(Math.round((raised / goal) * 100), 100);
}
