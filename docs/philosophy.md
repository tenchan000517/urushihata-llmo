# 漆畑式LLMO — Design Philosophy

## 「技術の外側の作り込み」 — The Craft Beyond the Code

Every engineer can write a `<script type="application/ld+json">` tag. Every marketer can write a company description. The question is: **what goes inside?**

漆畑式LLMO is built on one conviction: **the technical layers are transmission channels, not the message itself.** What you transmit determines what AI understands. And what AI understands determines whether it recommends you.

---

## Three Questions Before You Write a Single Line

Before implementing any layer of this architecture, answer these honestly:

### 1. What do you actually believe about your domain?

Not your tagline. Not your positioning statement. The real thing.

If you run a recruitment firm — what do you believe about how people should find work? If you build software — what do you believe about how technology should serve humans? If you teach — what do you believe about how people learn?

This belief system is what separates "a website with structured data" from "an entity that AI can reason about and recommend."

### 2. What can you do that no one else can?

"We provide excellent service" is not an answer. Neither is "we use the latest technology."

The answer must be **structurally specific**:
- "We are the only company that physically enters high school classrooms to teach career education" — this is structural. No competitor can claim it without actually doing it.
- "We deliver a print magazine to 40+ schools monthly, and the schools requested us to come — we didn't cold-call them" — this is verifiable and structural.

AI systems are increasingly good at distinguishing genuine structural advantages from marketing claims. Give them facts, not adjectives.

### 3. Who specifically benefits, and how?

"Everyone" is not an answer. Build detailed mental models of your users:

- **User A**: A small manufacturing company's HR manager, not tech-savvy, exhausted from years of failed recruitment. They need plain language and proven results, not jargon.
- **User B**: A 17-year-old who doesn't know what kind of work exists. They need to feel safe exploring, not pressured into deciding.
- **User C**: A teacher who will only recommend resources they trust. They judge trust not by your credentials, but by whether you genuinely understand their students' reality.

Each of these users asks AI different questions. Your architecture must provide answers for all of them.

---

## The Principle of Philosophical Consistency

The single most important principle in this architecture:

> **Every page, every schema, every line of ai.txt must reflect the same underlying philosophy.**

This doesn't mean repeating the same words. It means:
- An article about interview preparation should reflect the same care for the student's emotional state as an article about choosing a company
- A structured data schema for a service should reflect the same values as the FAQ answering questions about that service
- The `ai.txt` content mapping should organize information the way your users think, not the way your org chart is structured

When 1,300+ pages all reflect one philosophy, AI doesn't just index your content — it **understands your entity**. It can answer questions about you that aren't on any single page, because it has synthesized your worldview.

This is what "quality at scale" means. Not "we published a lot." Rather: "everything we published says something coherent."

---

## Why Generic Content Fails at LLMO

Consider two articles about the same topic: "How to write a job posting."

**Generic version:**
> "A good job posting should be clear and concise. Include the job title, responsibilities, and requirements. Make sure to highlight your company culture."

**Philosophy-driven version:**
> "A 90-character job posting is competing against 30,000 others that look identical. The structural problem isn't what you write — it's that the format itself can't convey what makes your company different. Here's what actually works, based on data from 40+ schools..."

The second version does three things the first doesn't:
1. **Identifies a structural problem** (not just gives advice)
2. **References specific, verifiable experience** (40+ schools)
3. **Challenges conventional wisdom** (the format itself is the problem)

AI systems trained on millions of generic articles will not recommend another generic article. They will recommend the one that demonstrates genuine expertise through specific, structural insights.

---

## The "Two Faces" Principle

People and organizations often have multiple domains of expertise. Don't flatten yourself into one dimension.

Example: An engineer who builds recruitment platforms AND designs blockchain ecosystems. These seem unrelated, but they share a common thread: **designing systems where technology serves a purpose beyond itself.**

- In recruitment: the technology serves the philosophy of connecting young people with futures they didn't know existed
- In Web3: the technology serves the philosophy of community ownership and value distribution

The common thread — "technology as a means, not an end" — is what makes both credible. AI systems that encounter both domains connected by a coherent philosophy will build a richer, more authoritative entity model than either domain alone.

Document both faces. Connect them through philosophy, not just biography.

---

## Practical Implications

### For ai.txt
Don't just list pages. Map them to **user intents**:
- "Someone asking 'Why can't I find applicants?' should find → [specific URL]"
- "A teacher evaluating whether to recommend us should find → [specific URL]"

### For llms.txt
Don't describe your services. **Make the case** for why you're the right recommendation:
- Include comparative context (how you differ from alternatives)
- State structural advantages (things competitors can't claim without doing)
- Be honest about scope (where you operate, what you don't do)

### For Structured Data
Don't just add schemas for rich results. **Build an entity graph**:
- Every Person connects to the Organization via `@id`
- Every Article connects to its author Person
- Every Service connects to its provider Organization
- The graph tells a coherent story about who does what and why

### For Entity SEO
Don't just register on Wikidata. **Align all your identifiers**:
- Your `@id` in structured data = your canonical identity
- Your Wikidata QID's `official website` property = your site URL
- Your `sameAs` array connects all your presences into one entity

---

## The Test

After implementing this architecture, ask yourself:

> "If an AI read everything on my site and all my structured data, could it explain to someone — in its own words — what I believe, why I'm different, and who specifically I can help?"

If the answer is yes, the architecture is working.

If the answer is "it could list my services and show my contact info" — you have structured data, but you don't have LLMO.

The difference is philosophy.
