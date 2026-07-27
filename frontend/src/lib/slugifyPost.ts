import { slugify } from "./slugify";

/**
 * slugifyPost — converts raw HTML content (typical blog-post heading text) into a stable URL-safe slug.
 * Used by /blog/[slug].astro for both inline heading anchors and post-body deep-link anchors.
 *
 * Per-call pipeline:
 *   1. Strip HTML tags                       /<[^>]*>/g          -> ""  (anything between < and >)
 *   2. Strip HTML entities                   /&[^;]+;/g          -> ""  (e.g. &amp; &copy; &#x...)
 *   3. Delegate to lib/slugify: lowercase + non-alphanumeric RUN collapse to a single
 *      dash + trim leading/trailing dashes.
 *
 * Behaviour differences vs the previous 5-step inline chain this replaces:
 *   - Output is lowercase (lib/slugify lowercases; old inline preserved case).
 *     This aligns with the project's URL-slug conventions across /causes, /events,
 *     /team, /blog and avoids surprise fragments like "#What-People-Say".
 *   - Underscores collapse to dashes (lib/slugify's [^a-z0-9]+ treats _ as
 *     non-alphanumeric; old inline's [^\w\s-] preserved _). Trade-off documented
 *     so future callers know underscores become dashes, not preserved.
 *   - No explicit "double-dash collapse" step needed: lib/slugify's [^a-z0-9]+ already
 *     collapses runs of any non-alphanumeric chars (including runs of dashes) to a
 *     single dash.
 *
 * Examples:
 *   slugifyPost("<h1>Hello, World!</h1>")           -> "hello-world"
 *   slugifyPost("Q &amp; A: Peace <em>Now</em>")    -> "q-a-peace-now"
 *   slugifyPost("My_Post_Title")                    -> "my-post-title"
 *   slugifyPost("What People Say")                  -> "what-people-say"
 *   slugifyPost("")                                 -> ""
 */
export function slugifyPost(html: string): string {
  const stripped = String(html)
    .replace(/<[^>]*>/g, "")
    .replace(/&[^;]+;/g, "");
  return slugify(stripped);
}
