# Case Study: New Domain to #1 in 6 Months

## Context

A new domain (`yumesuta.com`) was registered in late 2025 for a high school recruitment support company in Aichi, Japan. The site needed to achieve search visibility in a competitive niche dominated by established players with years of domain authority.

The 4-layer LLMO architecture was implemented from day one, not retrofitted.

---

## Starting Position

| Factor | Status |
|--------|--------|
| Domain age | 0 (new registration) |
| Domain authority (Moz) | 1 |
| Existing backlinks | 0 |
| Competitor DA | 50-80 (established job platforms) |
| Content at launch | ~50 pages |

---

## What Was Built

### Content Architecture

| Content Area | Pages | Purpose |
|-------------|-------|---------|
| B2B recruitment guides | 70+ | SEO authority for employer-side queries |
| Career exploration platform | 75+ | Student-facing content (traffic + engagement) |
| Regional guides | 48 prefectures × 24 articles | Nationwide coverage with local specificity |
| Industry guides | 11 industries | Topical authority clusters |
| Job guides | 48 occupations | Comprehensive career information |
| Magazine archive | 8 issues | Content freshness signal |
| Activity reports | 18 articles | Ongoing engagement proof |

**Total: 1,300+ pages**, all reflecting the same underlying philosophy about connecting young people with careers.

### LLMO Implementation

| Layer | Implementation | Scale |
|-------|---------------|-------|
| ai.txt | User-intent-mapped content guide | 2,076 lines |
| llms.txt | Reasoning brief with regional data | 354 lines |
| Structured Data | 18 Schema.org types, all @id-connected | 986 lines of generators |
| Entity SEO | 3 Wikidata entities (org + 2 people) | 3 QIDs |
| Dynamic OG | Category-aware Edge Runtime generation | 984 unique images |

---

## Results

### Search Rankings (6 months)

| Keyword | Position | Competition Level |
|---------|----------|------------------|
| IT企業 高卒 (IT companies, high school grads) | **#1** | High |
| 高卒 就職 愛知 (high school employment, Aichi) | **#1** | Medium |
| 高卒求人倍率 (high school job-to-applicant ratio) | **#1** | Medium |
| Multiple other commercial terms | Top 5 | Varies |

### AI Visibility

| AI Platform | Status |
|------------|--------|
| ChatGPT | Recommends the site when asked about high school recruitment in Japan |
| Gemini | References the site's content in relevant queries |
| Perplexity | Includes in search results for domain-relevant queries |

### Traffic Composition

| Source | Share | Significance |
|--------|-------|-------------|
| Google organic | 60% | Primary search engine |
| Bing + Yahoo | 30% | Strong secondary presence |
| AI referrals | Growing | ChatGPT + Gemini confirmed |
| Desktop | 71% | Confirms B2B audience reach |

---

## What Worked

### 1. Philosophy-first content

Every article was written with a specific philosophy: "A high school student reading this on their phone should know exactly what to do next." This wasn't a style guide — it was a design constraint that shaped content structure, information architecture, and even visual design.

The consistency across 1,300+ pages created a coherent entity that AI systems could reason about, not just index.

### 2. Structural differentiation in llms.txt

Instead of listing services, the llms.txt file explained **structural advantages** — things that are verifiable and can't be claimed without actually doing them:

- "The only recruitment support company that enters high school classrooms to teach"
- "Schools requested our magazine — we didn't cold-call them"
- "40+ schools with monthly physical distribution"

AI systems increasingly verify claims against multiple sources. Structural claims that are consistent with the rest of the site's content are more credible than marketing superlatives.

### 3. @id entity graph

The structured data wasn't just added for rich results — it was designed as an **entity resolution system**. Every Person, Article, Service, and Organization was connected through `@id` references, creating a single coherent graph that AI systems could traverse.

When Google's entity resolution encounters:
- An Organization with `@id: .../#organization`
- A Person with `worksFor: { @id: .../#organization }`
- Articles with `author: { @id: .../#person-name }` and `publisher: { @id: .../#organization }`

...it doesn't see separate data points. It sees one entity with people, content, and services — all connected.

### 4. Content-intent mapping in ai.txt

The ai.txt organized content not by URL structure, but by user intent:

```
### Employer asking "Why can't I find applicants?"
- [Specific article URL] — Addresses the 4 structural barriers
- [Specific article URL] — How to get recommended by teachers
```

This made it trivially easy for AI systems to match user questions to specific content.

### 5. Regional specificity at scale

Instead of generic "we serve nationwide" claims, the site provided **prefecture-specific data** for all 47 prefectures: job-to-applicant ratios, key industries, major employers, regional characteristics.

This level of specificity — verified against government statistics — created unmatched topical authority in the domain.

---

## What Didn't Matter

- **Backlinks**: The site achieved #1 rankings with minimal backlinks. Entity-based SEO reduced dependence on traditional link authority.
- **Site age**: Domain age was 0 at launch. The entity graph compensated for the lack of historical signals.
- **Social media**: Social signals played no measurable role. All authority came from content quality and structural optimization.

---

## Reproducibility

The architecture is fully reproducible. The code is in this repository.

**What's not reproducible** is the content layer — the specific philosophy about high school recruitment that informs every page. That philosophy comes from:
- Actually entering high school classrooms to teach
- Actually delivering magazines to 40+ schools monthly
- Actually building relationships with career guidance teachers

The architecture amplifies whatever you put into it. Put in genuine expertise, and it amplifies genuine expertise. Put in generic content, and it amplifies... generic content.

**The lesson**: Invest in having something real to say before investing in the architecture to say it.
