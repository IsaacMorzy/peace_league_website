/**
 * Lowercase ASCII, replace non-alphanumeric runs with a single dash, trim
 * leading/trailing dashes. Used for fragment identifiers + URL slugs across
 * the site so any heading that mentions a topic can be deep-linked.
 *
 * Examples:
 *   slugify("Peace Education")     -> "peace-education"
 *   slugify("What People Say")    -> "what-people-say"
 *   slugify("Hello, World!")      -> "hello-world"
 */
export function slugify(input: string): string {
  return String(input)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}
