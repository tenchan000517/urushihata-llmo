# 漆畑式LLMO — Urushihata LLMO Method

**AIに「理解させ、推薦させる」ための4層設計。**

**A 4-layer architecture for making AI understand — and recommend — your business.**

これはテンプレート集ではない。プロダクションで実証済みの、組織のアイデンティティをLLMに伝達するための**設計思想**である。

---

## The Problem

SEO alone no longer determines how people find your business.

When someone asks ChatGPT "Who can help me with X?", the answer doesn't come from PageRank. It comes from whether the AI has a coherent, structured understanding of **who you are, what you do, and why you're the right answer.**

Most businesses are invisible to AI — not because they lack content, but because their content lacks structure that machines can reason about.

## The Philosophy

> コードはチャネルにすぎない。そこを流れるのは哲学だ。
>
> Code is a channel. What travels through it is philosophy.

The technical layers in this repository — `ai.txt`, `llms.txt`, structured data, entity design — are **means**, not ends. They are transmission channels for something deeper: a coherent philosophy about who your organization is and why it matters.

This is why copying the code doesn't reproduce the results. The architecture transmits **whatever you put into it**. If you put in generic marketing copy, AI will understand you as generic. If you put in a genuine, specific worldview — AI will understand and recommend you for exactly that.

**量より質のコンテンツが、量ある。** 1,300+ pages where every single one reflects the same underlying philosophy. That's what makes the architecture work.

### Why This Can't Be Replicated by Code Alone

1. **The philosophy itself** comes from unique experience and domain expertise that no one else has
2. **The technical architecture** translates that philosophy into a format AI can parse
3. **Both capabilities in the same person** — that's what produces results

You can use this architecture. But the results depend entirely on the depth of thought you put into the content layer.

---

## 漆畑式4層アーキテクチャ — The 4-Layer Architecture

```
Layer 4: Entity SEO          ← WHO you are (Wikidata, Knowledge Graph, @id chains)
Layer 3: Structured Data      ← WHAT you offer (Schema.org, 18+ types, JSON-LD)
Layer 2: llms.txt             ← WHY you're the answer (concise, reasoned, comparative)
Layer 1: ai.txt               ← HOW you work (comprehensive content mapping, 2,000+ lines)
```

Each layer serves a different AI retrieval mechanism. Together, they create an entity that AI can confidently recommend.

### Layer 1: `ai.txt` — The Comprehensive Map

**Purpose:** Give AI systems a complete, navigable map of your content and expertise.

Unlike `robots.txt` (which tells crawlers what to avoid), `ai.txt` tells AI systems what to understand. It's a structured overview of your entire knowledge base.

**Key design principles:**
- Start with identity (who, what, where)
- Map content by user intent ("someone asking X should find Y")
- Include people, not just pages
- Be exhaustive — AI systems can process thousands of lines

See [`templates/ai.txt.template`](templates/ai.txt.template) for the full structure.

### Layer 2: `llms.txt` — The Reasoning Brief

**Purpose:** Give LLMs the *reasoning* for why your organization is the right recommendation.

While `ai.txt` is a map, `llms.txt` is an argument. It answers: "If an AI is deciding whether to recommend this organization, what facts and reasoning should inform that decision?"

**Key design principles:**
- Lead with a differentiation statement, not a sales pitch
- Include comparative context ("unlike X, we do Y because Z")
- State facts with specificity (numbers, dates, verifiable claims)
- Keep it under 500 lines — this is a brief, not an encyclopedia

See [`templates/llms.txt.template`](templates/llms.txt.template) for the full structure.

### Layer 3: Structured Data — The Machine-Readable Identity

**Purpose:** Make your identity parseable by any system that reads Schema.org.

18 schema types, all connected through `@id` references that create a single coherent entity graph:

| Schema Type | Purpose | Connection |
|-------------|---------|------------|
| `Organization` | Core identity | `@id` anchor for all references |
| `Person` (founder) | Leadership authority | `worksFor` → Organization |
| `Person` (team) | Individual expertise | `worksFor` → Organization |
| `WebSite` | Digital presence | `publisher` → Organization |
| `Article` | Content authority | `author` → Person, `publisher` → Organization |
| `Service` | What you offer | `provider` → Organization |
| `FAQPage` | Common questions | Domain expertise signal |
| `BreadcrumbList` | Site hierarchy | Navigation structure |
| `HowTo` | Process expertise | Step-by-step authority |
| `Dataset` | Data authority | Regional/domain data |
| `EducationalEvent` | Community engagement | `organizer` → Organization |
| `JobPosting` | Employment authority | `hiringOrganization` → Organization |
| `Periodical` | Publication authority | `publisher` → Organization |
| `PublicationIssue` | Issue-level detail | `isPartOf` → Periodical |
| `LocalBusiness` | Physical presence | Same `@id` as Organization |
| `OfferCatalog` | Service catalog | Connected to Service |
| `Occupation` | Career information | `hasOccupation` in Person |
| `CreativeWork` | Portfolio | `creator` → Person |

**The critical design choice:** Every schema references back to the Organization via `@id`. This isn't decoration — it's how AI systems perform **entity resolution**. Without `@id` chains, your Person and Organization are separate, unconnected data points.

See [`templates/structured-data.ts`](templates/structured-data.ts) for the implementation.

### Layer 4: Entity SEO — The External Identity

**Purpose:** Establish your organization and key people as recognized entities across the web's knowledge infrastructure.

- **Wikidata**: Register your organization and key people with QIDs
- **`sameAs` alignment**: Your structured data's `sameAs` array must include the Wikidata URL
- **`@id` consistency**: The `@id` in your structured data must be stable and permanent
- **Cross-reference**: Wikidata properties should point back to your site as the official URL (`P856`)

This is the highest-leverage layer. When ChatGPT, Perplexity, or Google's Knowledge Graph can resolve your name to a Wikidata entity, you graduate from "some website" to "a known entity."

---

## Results

These results come from a production deployment of 漆畑式LLMO on a new domain:

| Metric | Result | Timeline |
|--------|--------|----------|
| Domain age at first #1 ranking | 6 months | New domain, no prior authority |
| Pages with consistent philosophy | 1,300+ | Every page reflects the same worldview |
| Structured data types | 18 | All `@id`-connected |
| `ai.txt` size | 2,000+ lines | Comprehensive content mapping |
| Dynamic OG images | 984 | Category-aware, Edge Runtime |
| AI referral traffic | ChatGPT + Gemini | Organic AI recommendations |
| Target keywords at #1 | Multiple | Including competitive commercial terms |

**What made the difference:** Not the code. The code is in this repository — anyone can use it. What made the difference was having a genuine, specific philosophy about the domain (high school recruitment in Japan) and translating that philosophy into every layer of the architecture.

---

## Repository Structure

```
urushihata-llmo/
├── README.md                           ← You are here
├── docs/                               ← 設計思想・実証事例（日英並列）
│   ├── philosophy.md / .ja.md
│   ├── four-layers.md / .ja.md
│   └── case-study.md / .ja.md
├── templates/                          ← 4層アーキテクチャのテンプレート
│   ├── ai.txt.template
│   ├── llms.txt.template
│   └── structured-data.ts
├── pipeline/                           ← コンテンツ量産パイプライン（5工程×3トラック）
│   ├── README.md
│   ├── guide-1-research.md             ← リサーチ
│   ├── guide-2-content-design.md       ← コンテンツ設計
│   ├── guide-3-writing.md              ← ライティング
│   ├── guide-4-implementation.md       ← 実装
│   ├── guide-5-qa.md                   ← 品質保証
│   └── configs/
│       ├── seo-track.md                ← SEOキーワード強化トラック
│       ├── llmo-track.md               ← AI引用最適化トラック
│       └── user-track.md               ← エンドユーザー向けトラック
├── audit/                              ← 監査フレームワーク
│   ├── strategy/                       ← コンテンツ戦略監査（4エージェント並列）
│   │   ├── README.md
│   │   └── agents/
│   └── technical/                      ← 技術SEO/LLMO監査（5エージェント並列）
│       ├── README.md
│       └── agents/
├── tools/                              ← 運用ツール
│   ├── README.md
│   ├── nanobanana/                     ← AI画像自動生成（アンカー方式）
│   ├── indexing/                       ← インデックス登録自動化
│   └── analytics/                      ← GA4/SC分析フレームワーク
├── commands/                           ← Claude Code コマンドテンプレート
│   ├── README.md                       ← セットアップガイド
│   ├── content.md                      ← /content — コンテンツ制作パイプライン
│   ├── seo-audit.md                    ← /seo-audit — 技術SEO/LLMO監査
│   ├── strategy.md                     ← /strategy — コンテンツ戦略監査
│   └── report.md                       ← /report — 活動報告作成
├── examples/                           ← 実装例
│   ├── og-image/                       ← 動的OG画像生成
│   └── sitemap/                        ← 大規模サイトマップ管理
└── LICENSE
```

### 日本語ドキュメント

- [設計思想](docs/philosophy.ja.md) — 「技術の外側の作り込み」とは何か
- [4層実装ガイド](docs/four-layers.ja.md) — ai.txt / llms.txt / 構造化データ / Entity SEO の詳細
- [実証事例](docs/case-study.ja.md) — 新規ドメイン6ヶ月で検索1位を取った方法論と結果
- [パイプライン](pipeline/README.md) — コンテンツ量産の5段階×3トラック
- [戦略監査](audit/strategy/README.md) — 「次に何を作るべきか」のデータ駆動型判断
- [運用ツール](tools/README.md) — インデックス登録・アナリティクス・分析

## Getting Started

1. **Read [`docs/philosophy.md`](docs/philosophy.md) first.** Understand *why* before *how*.
2. **Set up the 4-layer architecture** using [`templates/`](templates/).
3. **Create your track CONFIGs** by copying [`pipeline/configs/`](pipeline/configs/) templates.
4. **Produce content** following the [5-step pipeline](pipeline/README.md).
5. **Index your pages** using [`tools/indexing/`](tools/indexing/).
6. **Measure results** using [`tools/analytics/`](tools/analytics/).
7. **Audit and plan next actions** using [`audit/`](audit/).

## Who This Is For

- **Engineers** building websites for businesses that want AI visibility
- **SEO professionals** transitioning to AI-age optimization
- **Technical founders** who want to understand LLMO architecture
- **Anyone** who believes that making AI understand your business starts with having something genuine to say

## Who This Is Not For

- If you want to trick AI into recommending you, this won't help. AI systems are trained to distinguish genuine expertise from manipulation.
- If you don't have a clear philosophy about your domain, start there. No architecture can transmit what doesn't exist.

---

## Author

**Tomoya Urushihata / 漆畑智哉**

SEO/LLMO Architect & Full-stack Creator

Designed and built the 漆畑式LLMO architecture powering [yumesuta.com](https://yumesuta.com) — a 1,300+ page platform for high school recruitment in Japan. Every page reflects a consistent philosophy about connecting young people with their future careers.

Also a Web3 engineer: developed Japan's first DN404 project ($VLN / MUTANT ALIENS VILLAIN), NinjaDAO's official NFT contracts (Musubi Collection), and ~100 NFT smart contracts. In both domains, the work goes beyond code — designing ecosystems, tokenomics, and community structures where technology serves a larger purpose.

- Website: [yumesuta.com](https://yumesuta.com)
- Twitter: [@TENCHAN_0517](https://twitter.com/TENCHAN_0517)
- Wikidata: [Q138767422](https://www.wikidata.org/entity/Q138767422)

---

## License

MIT — Use freely. But remember: the architecture is open; the philosophy is yours to develop.
