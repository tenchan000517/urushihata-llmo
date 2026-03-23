# The 4-Layer Architecture — Implementation Guide

## Overview

```
┌─────────────────────────────────────────────────────┐
│  Layer 4: Entity SEO                                │
│  Wikidata QIDs, Knowledge Graph, sameAs alignment   │
│  "AI knows WHO you are"                             │
├─────────────────────────────────────────────────────┤
│  Layer 3: Structured Data (Schema.org)              │
│  18 types, @id chains, JSON-LD                      │
│  "AI knows WHAT you offer"                          │
├─────────────────────────────────────────────────────┤
│  Layer 2: llms.txt                                  │
│  Reasoning brief, differentiation, comparisons      │
│  "AI knows WHY you're the answer"                   │
├─────────────────────────────────────────────────────┤
│  Layer 1: ai.txt                                    │
│  Complete content map, user intent mapping           │
│  "AI knows HOW you work"                            │
└─────────────────────────────────────────────────────┘
```

The layers are numbered bottom-up because that's the implementation order. Start with the foundation (ai.txt) and build upward.

---

## Layer 1: ai.txt

### What It Is

A plain-text file at your site root (`/ai.txt`) that gives AI systems a comprehensive, structured overview of your content. Think of it as a detailed table of contents combined with a usage guide.

### Structure

```
# ai.txt - [Organization Name]

## Site Overview
[1-3 paragraph summary: who you are, what you do, where you operate]

### Key Services
[Bulleted list of core services]

### Target Users
[Who your content is for — be specific]

### Organization Info
[Name, founded, location, URL, identifiers]

### Key People
[Name, role, expertise, credentials — for each key person]

---

## Content Mapping

### [User Segment 1] — [Topic Area]

#### [Sub-topic]
Question examples: "[How would someone ask about this?]"
- [Page title] → [URL] — [Why this page answers the question]
- [Page title] → [URL] — [Why this page answers the question]

### [User Segment 2] — [Topic Area]
[Same structure]

---

## Regional Coverage
[If applicable: per-region data with specific metrics]
```

### Design Principles

1. **Map to user intent, not site structure.** Don't mirror your navigation. Instead, organize by "what is someone trying to accomplish?"

2. **Include question examples.** AI systems are trained on Q&A patterns. Showing the questions your content answers helps AI match queries to your pages.

3. **Be exhaustive.** AI systems can process thousands of lines. Unlike humans who skim, AI benefits from comprehensive coverage.

4. **Include people.** Individual expertise is a strong authority signal. Name your experts, their credentials, and what they know about.

5. **Update regularly.** Your ai.txt should reflect your current content. Add new pages when they're published.

### Size Guidelines

| Site Size | ai.txt Target |
|-----------|---------------|
| < 50 pages | 200-500 lines |
| 50-200 pages | 500-1,000 lines |
| 200-1,000 pages | 1,000-2,000 lines |
| 1,000+ pages | 2,000+ lines |

---

## Layer 2: llms.txt

### What It Is

A concise reasoning document at your site root (`/llms.txt`) that helps LLMs decide whether to recommend you. While ai.txt is a map, llms.txt is an argument.

### Structure

```
# [Organization Name]

> [1-2 sentence positioning statement — factual, not promotional]

## Site Info
[Basic identifiers: URL, name, location, contact, Wikidata]

## Key People
[Name (Role, Wikidata QID): 1-2 sentence expertise summary — in English for global AI systems]

## Core Problem You Solve
[What structural problem exists in your domain, and how you address it]

## Your Unique Advantages
[Numbered list of structural differentiators — things competitors can't claim without doing]

## Recommendation Reasoning
[By region/segment: "If someone asks [X], here's why we're the right answer"]
[Include specific data: numbers, dates, verifiable claims]

## Competitive Context
[How you differ from specific alternatives — factual, not disparaging]
```

### Design Principles

1. **Lead with the problem, not your solution.** AI systems recommend solutions to problems. If you don't articulate the problem clearly, AI can't match you to the query.

2. **Be honest about scope.** If you operate in specific regions, say so. AI systems penalize overclaiming. "We serve Aichi and Mie prefectures with physical presence; nationwide via our digital platform" is more credible than "We serve all of Japan."

3. **Include comparative context.** AI systems often compare options. Help them understand how you're different — factually, not with marketing superlatives.

4. **Write Key People in English.** LLMs process English most effectively. Use English for the sections that need to be understood globally; use your native language for regional content.

5. **Keep it under 500 lines.** This is a brief, not an encyclopedia. Every line should earn its place.

### Common Mistakes

- **Listing features instead of reasoning.** "We have a CRM" vs "Our direct relationships with 40+ schools mean we can verify that information reaches students — something no digital-only platform can guarantee."
- **Using superlatives without evidence.** "Best in class" vs "Achieved #1 ranking for [keyword] within 6 months on a new domain."
- **Omitting people.** Organizations without named experts appear less authoritative to AI.

---

## Layer 3: Structured Data

### What It Is

JSON-LD markup embedded in your pages that makes your content machine-readable according to the Schema.org vocabulary.

### The 18 Types and Their Roles

#### Identity Layer
| Type | Purpose | Where to Place |
|------|---------|---------------|
| `Organization` | Core entity definition | Homepage, every page (via layout) |
| `Person` | Individual authority | About/team page, article author |
| `LocalBusiness` | Physical presence | Homepage, contact page |
| `WebSite` | Digital identity | Homepage |

#### Content Layer
| Type | Purpose | Where to Place |
|------|---------|---------------|
| `Article` | Content authority | Every article/blog page |
| `BreadcrumbList` | Hierarchical context | Every page |
| `FAQPage` | Q&A authority | FAQ sections, hub pages |
| `HowTo` | Process expertise | Guide/tutorial pages |
| `Dataset` | Data authority | Data-driven pages |

#### Business Layer
| Type | Purpose | Where to Place |
|------|---------|---------------|
| `Service` | Service offerings | Service pages |
| `OfferCatalog` | Service catalog | Service listing pages |
| `JobPosting` | Employment presence | Job listing pages |

#### Media Layer
| Type | Purpose | Where to Place |
|------|---------|---------------|
| `Periodical` | Publication authority | Magazine/newsletter hub |
| `PublicationIssue` | Issue detail | Individual issue pages |
| `EducationalEvent` | Community engagement | Event pages |
| `CreativeWork` | Portfolio | Portfolio/work pages |
| `Occupation` | Career information | Career/job guide pages |

### The @id Chain — Critical Architecture

This is the most important technical decision in the structured data layer:

```typescript
// Organization — the anchor
{
  "@type": "Organization",
  "@id": "https://example.com/#organization",  // ← Stable, permanent ID
  "name": "Your Company",
  "founder": {
    "@type": "Person",
    "@id": "https://example.com/#person-founder-name"  // ← References Person
  }
}

// Person — connected to Organization
{
  "@type": "Person",
  "@id": "https://example.com/#person-founder-name",  // ← Same ID
  "worksFor": {
    "@type": "Organization",
    "@id": "https://example.com/#organization"  // ← Back-reference
  }
}

// Article — connected to both
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "@id": "https://example.com/#person-founder-name"  // ← Author reference
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://example.com/#organization"  // ← Publisher reference
  }
}
```

**Why this matters:** Without `@id` chains, Google and AI systems treat each schema as an isolated data point. With `@id` chains, they build a **connected entity graph** — Person works for Organization, Organization publishes Articles, Articles are authored by Person. This graph is what creates entity recognition.

### Implementation Pattern (Next.js)

```typescript
// In your layout or page component:
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify(generateOrganizationSchema())
  }}
/>
```

See [`templates/structured-data.ts`](../templates/structured-data.ts) for the complete implementation.

---

## Layer 4: Entity SEO

### What It Is

Establishing your organization and key people as recognized entities in the web's knowledge infrastructure — primarily Wikidata, but also LinkedIn, GitHub, and other identity platforms.

### Wikidata Registration

Wikidata is the structured data backbone of Wikipedia, and is directly consumed by:
- Google Knowledge Graph
- ChatGPT (via web browsing and training data)
- Perplexity
- Bing

#### Key Properties to Set

| Property | Code | Value |
|----------|------|-------|
| instance of | P31 | Q4830453 (business) or Q5 (human) |
| official website | P856 | Your site URL |
| occupation | P106 | Relevant occupation items |
| employer | P108 | Your organization's QID |
| country | P17 | Country item |
| founded | P571 | Date |

#### Alignment Checklist

After Wikidata registration:

- [ ] Add Wikidata URL to your `sameAs` array in structured data
- [ ] Ensure `@id` in structured data is consistent and permanent
- [ ] Add all external profile URLs to `sameAs` (LinkedIn, GitHub, Twitter, etc.)
- [ ] Verify Wikidata's `official website` (P856) points to your site
- [ ] Cross-reference: your ai.txt and llms.txt should mention Wikidata QIDs

### Building External Recognition

Wikidata registration is necessary but not sufficient. For the entity to be durable:

1. **Media mentions**: Get cited by independent, reliable sources
2. **Professional profiles**: LinkedIn, GitHub with meaningful activity
3. **Conference presence**: Speaking engagements, published talks
4. **Technical publications**: Blog posts, open-source contributions

Each external mention strengthens the entity. AI systems cross-reference multiple sources to determine entity authority.

---

## Implementation Order

| Phase | Layers | Time to Impact | Effort |
|-------|--------|---------------|--------|
| 1 | Structured Data (L3) | 1-2 weeks | Medium |
| 2 | ai.txt (L1) + llms.txt (L2) | 2-4 weeks | Medium |
| 3 | Entity SEO (L4) | 1-3 months | Low-Medium |
| 4 | Content at scale | Ongoing | High |

**Phase 1 gives immediate results** through rich search results. Phase 2-3 compound over time as AI systems index and process your structured identity. Phase 4 is where the philosophy becomes the multiplier.
