/**
 * Large-Scale Sitemap Management — Next.js App Router
 *
 * This pattern demonstrates how to manage 270+ URL entries
 * with proper metadata for search engines and AI systems.
 *
 * WHY THIS MATTERS FOR LLMO:
 * - changeFrequency tells AI crawlers how often to re-check
 * - priority signals which pages are most important
 * - lastModified triggers re-crawling when content updates
 * - Grouped by content type for maintainability at scale
 *
 * USAGE:
 *   Place as src/app/sitemap.ts in a Next.js App Router project.
 *   Next.js automatically generates /sitemap.xml from this file.
 */

import { MetadataRoute } from 'next'

const BASE_URL = 'https://example.com'

export default function sitemap(): MetadataRoute.Sitemap {
  // ============================================================
  // Static pages — manually maintained
  // ============================================================

  const staticPages: MetadataRoute.Sitemap = [
    // Homepage — highest priority, changes frequently
    {
      url: BASE_URL,
      lastModified: new Date('2026-03-20'),
      changeFrequency: 'weekly',
      priority: 1.0,
    },

    // Core pages
    {
      url: `${BASE_URL}/about`,
      lastModified: new Date('2026-03-15'),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/contact`,
      lastModified: new Date('2026-01-01'),
      changeFrequency: 'yearly',
      priority: 0.6,
    },

    // Service pages — moderate priority, rarely change
    {
      url: `${BASE_URL}/services/service-1`,
      lastModified: new Date('2026-03-01'),
      changeFrequency: 'monthly',
      priority: 0.85,
    },
    {
      url: `${BASE_URL}/services/service-2`,
      lastModified: new Date('2026-03-01'),
      changeFrequency: 'monthly',
      priority: 0.85,
    },
  ]

  // ============================================================
  // Content hub pages — high priority, updated with new content
  // ============================================================

  const hubPages: MetadataRoute.Sitemap = [
    {
      url: `${BASE_URL}/blog`,
      lastModified: new Date('2026-03-20'),
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${BASE_URL}/guides`,
      lastModified: new Date('2026-03-15'),
      changeFrequency: 'weekly',
      priority: 0.85,
    },
  ]

  // ============================================================
  // Dynamic content — generated from data
  // ============================================================

  // Blog articles — add new entries at the TOP of the array
  const blogSlugs = [
    // Newest first
    '2026-03-20-latest-article',
    '2026-03-15-another-article',
    '2026-03-10-older-article',
    // ... add more as you publish
  ]

  const blogEntries: MetadataRoute.Sitemap = blogSlugs.map((slug) => ({
    url: `${BASE_URL}/blog/${slug}`,
    lastModified: new Date(slug.slice(0, 10)),  // Extract date from slug
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }))

  // Guide pages — can also be data-driven
  const guideSlugs = [
    'getting-started',
    'advanced-usage',
    'best-practices',
    'troubleshooting',
  ]

  const guideEntries: MetadataRoute.Sitemap = guideSlugs.map((slug) => ({
    url: `${BASE_URL}/guides/${slug}`,
    lastModified: new Date('2026-03-01'),
    changeFrequency: 'monthly' as const,
    priority: 0.75,
  }))

  // ============================================================
  // Regional content — scalable pattern for 47+ regions
  // ============================================================

  const regions = [
    'tokyo',
    'osaka',
    'aichi',
    // ... all regions
  ]

  // Sub-pages per region — same structure for consistency
  const regionSubPages = [
    'overview',
    'schedule',
    'statistics',
    'industries',
    'faq',
  ]

  const regionalEntries: MetadataRoute.Sitemap = regions.flatMap((region) => [
    // Region hub page
    {
      url: `${BASE_URL}/regions/${region}`,
      lastModified: new Date('2026-03-01'),
      changeFrequency: 'monthly' as const,
      priority: 0.8,
    },
    // Region sub-pages
    ...regionSubPages.map((subPage) => ({
      url: `${BASE_URL}/regions/${region}/${subPage}`,
      lastModified: new Date('2026-03-01'),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    })),
  ])

  // ============================================================
  // Legal pages — low priority, rarely change
  // ============================================================

  const legalPages: MetadataRoute.Sitemap = [
    {
      url: `${BASE_URL}/privacy`,
      lastModified: new Date('2025-01-01'),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${BASE_URL}/terms`,
      lastModified: new Date('2025-01-01'),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
  ]

  // ============================================================
  // Combine all entries
  // ============================================================

  return [
    ...staticPages,
    ...hubPages,
    ...blogEntries,
    ...guideEntries,
    ...regionalEntries,
    ...legalPages,
  ]
}

// ============================================================
// DESIGN NOTES:
//
// 1. PRIORITY GUIDE:
//    1.0  — Homepage only
//    0.9  — Content hub pages (blog index, guide index)
//    0.85 — Service pages, pillar content
//    0.8  — Important sub-hubs (regional hubs)
//    0.7  — Individual content pages (articles, guides)
//    0.6  — Secondary content (interviews, archive)
//    0.3  — Legal, utility pages
//
// 2. CHANGE FREQUENCY:
//    - Set this honestly. Don't claim 'daily' if you update monthly.
//    - Hub pages: 'weekly' (they change when you add child content)
//    - Individual articles: 'monthly' or 'never' (after publication)
//    - Legal pages: 'yearly'
//
// 3. LAST MODIFIED:
//    - Update this when content actually changes
//    - For hub pages: update when any child page is added/modified
//    - This triggers re-crawling — don't abuse it
//
// 4. SCALING TO 1,000+ ENTRIES:
//    - Use data arrays + .map() patterns (as shown above)
//    - Group by content type for maintainability
//    - Consider splitting into multiple sitemaps if > 50,000 URLs
//      (use sitemap index: src/app/sitemap/[id]/route.ts)
//
// 5. EXCLUDING PAGES:
//    - Don't include pages with noindex
//    - Don't include redirect sources
//    - Don't include unpublished/draft content
// ============================================================
