import type { APIRoute } from "astro";
import { buildSearchIndex } from "@freshjuice/astro-search-plugin/build";
import causesData from "../lib/causes-data.json";
import eventsData from "../lib/events-data.json";

interface SearchDocument {
  id: string;
  title: string;
  desc: string;
  url: string;
  category: string;
}

// All 62 award categories from backend fixtures — embedded at build time
// so the search palette works even before the API seed runs.
const AWARD_CATEGORIES: { name: string; slug: string }[] = [
  { name: "Best Author in Cultural Narratives of Unity and Hope", slug: "best-author-cultural-narratives-unity-hope" },
  { name: "Best Author for Excellence in Language Book Writing Award", slug: "best-author-excellence-language-book-writing-award" },
  { name: "Best Author in Heritage Land Restoration Award", slug: "best-author-heritage-land-restoration-award" },
  { name: "Best Author in Voices of Perseverance in Literature Award", slug: "best-author-voices-perseverance-literature-award" },
  { name: "Best Media Personnel Advocating for an Ethical Society", slug: "best-media-personnel-advocating-ethical-society" },
  { name: "Best Personality Promoting Peace Through Arts", slug: "best-personality-promoting-peace-through-arts" },
  { name: "Best Radio Personnel Advocating for Peace and Spirituality", slug: "best-radio-personnel-advocating-peace-spirituality" },
  { name: "Best Radio Personnel Advocating for Positive Relationships", slug: "best-radio-personnel-advocating-positive-relationships" },
  { name: "Best Spiritual Wisdom Author Award", slug: "best-spiritual-wisdom-author-award" },
  { name: "Best Teacher of the Year Award", slug: "best-teacher-year-award" },
  { name: "Best TV Producer Advocating for Peace in Society", slug: "best-tv-producer-advocating-peace-society" },
  { name: "Champion of Disability Rights and Inclusion Award", slug: "champion-disability-rights-inclusion-award" },
  { name: "Champion of Interfaith Harmony Award", slug: "champion-interfaith-harmony-award" },
  { name: "Champion of Labour Rights and Social Protection", slug: "champion-labour-rights-social-protection" },
  { name: "Champion of Mosque Peace and Unity Award", slug: "champion-mosque-peace-unity-award" },
  { name: "Champion for Women's Rights and Empowerment Award", slug: "champion-womens-rights-empowerment-award" },
  { name: "Championing Mangrove Conservation", slug: "championing-mangrove-conservation" },
  { name: "Exceptional Commitment to Philanthropy and Selfless Contributions to the Betterment of Society", slug: "exceptional-commitment-philanthropy-selfless-contributions-betterment-society" },
  { name: "Excellence in Business Leadership and Philanthropy Award", slug: "excellence-business-leadership-philanthropy-award" },
  { name: "Excellence in Championing Shariah Finance Compliance in Kenya Award", slug: "excellence-championing-shariah-finance-compliance-kenya-award" },
  { name: "Excellence in Community Policing Award", slug: "excellence-community-policing-award" },
  { name: "Excellence in Community Service Award", slug: "excellence-community-service-award" },
  { name: "Excellence in Counselling and Girl-Child Mentorship Award", slug: "excellence-counselling-girl-child-mentorship-award" },
  { name: "Excellence in Creative Branding Award", slug: "excellence-creative-branding-award" },
  { name: "Excellence in Cultural Diplomacy Award", slug: "excellence-cultural-diplomacy-award" },
  { name: "Excellence in Digital Innovation for Peace Award", slug: "excellence-digital-innovation-peace-award" },
  { name: "Excellence in Environmental Conservation and Social Empowerment Award", slug: "excellence-environmental-conservation-social-empowerment-award" },
  { name: "Excellence in Humanitarian Leadership", slug: "excellence-humanitarian-leadership" },
  { name: "Excellence in Islamic Banking and Community Development Award", slug: "excellence-islamic-banking-community-development-award" },
  { name: "Excellence in Islamic Jurisprudence Award", slug: "excellence-islamic-jurisprudence-award" },
  { name: "Excellence in Journalism and Advocacy Award", slug: "excellence-journalism-advocacy-award" },
  { name: "Excellence in Leadership and Governance Award", slug: "excellence-leadership-governance-award" },
  { name: "Excellence in Leadership, Religious Guidance and Literary Contribution Award", slug: "excellence-leadership-religious-guidance-literary-contribution-award" },
  { name: "Excellence in Legal Leadership", slug: "excellence-legal-leadership" },
  { name: "Excellence in Mediation and Conflict Resolution Award", slug: "excellence-mediation-conflict-resolution-award" },
  { name: "Excellence in Music and Literary Arts Award", slug: "excellence-music-literary-arts-award" },
  { name: "Excellence in National Security Leadership Award", slug: "excellence-national-security-leadership-award" },
  { name: "Excellence in Natural Health and Religious Leadership Award", slug: "excellence-natural-health-religious-leadership-award" },
  { name: "Excellence in Philanthropy and Community Enrichment Award", slug: "excellence-philanthropy-community-enrichment-award" },
  { name: "Excellence in Promoting Discipline in Schools Through Chaplaincy", slug: "excellence-promoting-discipline-schools-chaplaincy" },
  { name: "Excellence in Psychology and Mental Health Advocacy Award", slug: "excellence-psychology-mental-health-advocacy-award" },
  { name: "Excellence in Sports for Peace and Unity Award", slug: "excellence-sports-peace-unity-award" },
  { name: "Interfaith Harmony and Collaboration Award", slug: "interfaith-harmony-collaboration-award" },
  { name: "Leadership in Firearms Policy and Safety Award", slug: "leadership-firearms-policy-safety-award" },
  { name: "Leadership in Public Administration Award", slug: "leadership-public-administration-award" },
  { name: "Lifetime Achievement Award in Diplomacy and Governance", slug: "lifetime-achievement-award-diplomacy-governance" },
  { name: "Lifetime Achievement in Peacebuilding and Reconciliation Award", slug: "lifetime-achievement-peacebuilding-reconciliation-award" },
  { name: "Medical Doctor of the Year", slug: "medical-doctor-year" },
  { name: "Outstanding Contribution to Cultural Exchange Award", slug: "outstanding-contribution-cultural-exchange-award" },
  { name: "Outstanding Contribution to Da'wah in the City Centre", slug: "outstanding-contribution-dawah-city-centre" },
  { name: "Outstanding Contribution to Education and Professional Development Award", slug: "outstanding-contribution-education-professional-development-award" },
  { name: "Outstanding Contribution to Legal Reforms Award", slug: "outstanding-contribution-legal-reforms-award" },
  { name: "Outstanding Contribution to National Security Award", slug: "outstanding-contribution-national-security-award" },
  { name: "Outstanding Contribution to Peace Journalism Award", slug: "outstanding-contribution-peace-journalism-award" },
  { name: "Outstanding Contribution to Refugee and IDP Support Award", slug: "outstanding-contribution-refugee-idp-support-award" },
  { name: "Outstanding Contribution to Social Impact Award", slug: "outstanding-contribution-social-impact-award" },
  { name: "Outstanding Contribution to Social Welfare", slug: "outstanding-contribution-social-welfare" },
  { name: "Peace Ambassador for Fighting Radicalism and Terrorism", slug: "peace-ambassador-fighting-radicalism-terrorism" },
  { name: "Promoting Peace Through Sports and Journalism", slug: "promoting-peace-through-sports-journalism" },
  { name: "Trailblazer Award in Military Leadership and Gender Empowerment", slug: "trailblazer-award-military-leadership-gender-empowerment" },
  { name: "Trailblazer in Police Leadership and Literature Award", slug: "trailblazer-police-leadership-literature-award" },
  { name: "Youth Leadership and Empowerment Award", slug: "youth-leadership-empowerment-award" },
];

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export const GET: APIRoute = async () => {
  const docs: SearchDocument[] = [];

  // ── Static key pages ──
  const pages: { title: string; desc: string; url: string; category: string }[] = [
    { title: "Awards 2026", desc: "Peace League Africa Awards — celebrate peace-building champions", url: "/awards", category: "Page" },
    { title: "Nominate for Awards", desc: "Submit a nomination for the Peace League Africa Awards", url: "/awards/nominate", category: "Page" },
    { title: "Awards Results", desc: "View winners of the Peace League Africa Awards", url: "/awards/results", category: "Page" },
    { title: "Awards Tickets", desc: "Purchase tickets for the Peace League Africa Awards Gala", url: "/awards/tickets", category: "Page" },
    { title: "Donate", desc: "Support peace-building across East Africa with your donation", url: "/donate", category: "Page" },
    { title: "Volunteer", desc: "Sign up to volunteer with Peace League Africa", url: "/volunteer", category: "Page" },
    { title: "Events", desc: "Peace League Africa events and community gatherings", url: "/events", category: "Page" },
    { title: "Causes", desc: "Our peace-building causes and campaigns across Africa", url: "/causes", category: "Page" },
    { title: "About Us", desc: "Learn about Peace League Africa's mission and team", url: "/about", category: "Page" },
    { title: "Contact", desc: "Get in touch with Peace League Africa", url: "/contact", category: "Page" },
    { title: "Careers", desc: "Join the Peace League Africa team", url: "/careers", category: "Page" },
    { title: "Partner With Us", desc: "Become a partner of Peace League Africa", url: "/partner", category: "Page" },
    { title: "Fundraise", desc: "Start a fundraiser for peace-building causes", url: "/fundraise", category: "Page" },
    { title: "Testimonials", desc: "Hear from Peace League Africa beneficiaries and supporters", url: "/testimonials", category: "Page" },
    { title: "FAQ", desc: "Frequently asked questions about Peace League Africa", url: "/faq", category: "Page" },
    { title: "Privacy Policy", desc: "Peace League Africa privacy policy", url: "/privacy", category: "Page" },
    { title: "Terms of Service", desc: "Peace League Africa terms of service", url: "/terms", category: "Page" },
    { title: "Sitemap", desc: "Complete sitemap for Peace League Africa", url: "/sitemap", category: "Page" },
  ];

  for (const p of pages) {
    docs.push({ id: `page-${p.url.replace(/\//g, "-")}`, title: p.title, desc: p.desc, url: p.url, category: p.category });
  }

  // ── Award Categories (62 total, from backend fixtures) ──
  for (const cat of AWARD_CATEGORIES) {
    docs.push({
      id: `award-${cat.slug}`,
      title: cat.name,
      desc: `Award category: ${cat.name}`,
      url: `/awards/category/${encodeURIComponent(cat.slug)}`,
      category: "Award Category",
    });
  }

  // ── Campaign Causes (from causes-data.json) ──
  if (Array.isArray(causesData)) {
    for (const cause of causesData as Record<string, unknown>[]) {
      const name = (cause.name || cause.title || "") as string;
      const slug = slugify(name);
      if (!slug) continue;
      docs.push({
        id: `cause-${slug}`,
        title: name,
        desc: ((cause.description || cause.tagline || "Peace League Africa cause") as string).slice(0, 160),
        url: `/causes/${encodeURIComponent(slug)}`,
        category: "Cause",
      });
    }
  }

  // ── Events (from events-data.json) ──
  if (Array.isArray(eventsData)) {
    for (const event of eventsData as Record<string, unknown>[]) {
      const slug = (event.slug || slugify((event.title || "") as string)) as string;
      if (!slug) continue;
      docs.push({
        id: `event-${slug}`,
        title: (event.title || event.name || "Event") as string,
        desc: ((event.description || event.tagline || "Peace League Africa event") as string).slice(0, 160),
        url: `/events/${encodeURIComponent(slug)}`,
        category: "Event",
      });
    }
  }

  // Build the Orama search index
  const index = await buildSearchIndex({
    schema: {
      id: "string",
      title: "string",
      desc: "string",
      url: "string",
      category: "string",
    },
    documents: docs,
  });

  return new Response(JSON.stringify(index), {
    headers: { "Content-Type": "application/json" },
  });
};
