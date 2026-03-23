/**
 * 漆畑式LLMO — Structured Data Generator
 *
 * 18 Schema.org types, all connected through @id references
 * to create a coherent entity graph that AI systems can reason about.
 *
 * CRITICAL DESIGN PRINCIPLE:
 * Every schema references back to the Organization via @id.
 * This is how AI systems perform entity resolution.
 * Without @id chains, your schemas are isolated data points.
 *
 * USAGE (Next.js):
 *   <script
 *     type="application/ld+json"
 *     dangerouslySetInnerHTML={{
 *       __html: JSON.stringify(generateOrganizationSchema())
 *     }}
 *   />
 *
 * CUSTOMIZATION:
 * 1. Replace all placeholder values with your actual data
 * 2. Remove schema types you don't need
 * 3. Keep the @id pattern consistent across all types
 * 4. Add your Wikidata QIDs to sameAs arrays
 */

// ============================================================
// Configuration — Replace these with your actual values
// ============================================================

const SITE_URL = 'https://example.com'
const ORG_NAME = 'Your Organization Name'
const ORG_LEGAL_NAME = 'Your Legal Organization Name'
const ORG_DESCRIPTION = 'A specific description of what your organization does, who it serves, and what makes it structurally different.'

// @id anchors — these MUST be consistent across all schemas
const ORG_ID = `${SITE_URL}/#organization`
const WEBSITE_ID = `${SITE_URL}/#website`

// ============================================================
// 1. Organization — The anchor entity
// ============================================================

export const generateOrganizationSchema = () => ({
  '@context': 'https://schema.org',
  '@type': ['Organization', 'EmploymentAgency'],  // Add relevant types
  '@id': ORG_ID,
  'name': ORG_NAME,
  'legalName': ORG_LEGAL_NAME,
  'url': SITE_URL,
  'logo': `${SITE_URL}/logo.png`,
  'description': ORG_DESCRIPTION,

  // What your organization knows about — strengthens topical authority
  'knowsAbout': [
    'Your Domain 1',
    'Your Domain 2',
    'Your Domain 3',
  ],

  'areaServed': [
    { '@type': 'State', 'name': 'Your Region' },
  ],

  'foundingDate': '2025-01-01',

  // Founder — references the Person entity below
  'founder': {
    '@type': 'Person',
    '@id': `${SITE_URL}/#person-founder-name`,
    'name': 'Founder Name',
  },

  // Team — all reference Person entities
  'employee': [
    {
      '@type': 'Person',
      '@id': `${SITE_URL}/#person-founder-name`,
      'name': 'Founder Name',
      'jobTitle': 'CEO',
    },
    {
      '@type': 'Person',
      '@id': `${SITE_URL}/#person-team-member`,
      'name': 'Team Member Name',
      'jobTitle': 'CTO',
    },
  ],

  'address': {
    '@type': 'PostalAddress',
    'addressLocality': 'City',
    'addressRegion': 'Region',
    'addressCountry': 'JP',
  },

  'contactPoint': {
    '@type': 'ContactPoint',
    'telephone': '+81-XXX-XXX-XXXX',
    'contactType': 'customer service',
    'areaServed': 'JP',
    'availableLanguage': 'Japanese',
  },

  // Services offered — connects to Service schemas
  'makesOffer': [
    {
      '@type': 'Offer',
      'itemOffered': {
        '@type': 'Service',
        'name': 'Service 1',
        'description': 'What this service does and who it helps.',
      },
    },
    {
      '@type': 'Offer',
      'itemOffered': {
        '@type': 'Service',
        'name': 'Service 2',
        'description': 'What this service does and who it helps.',
      },
    },
  ],

  // External identities — CRITICAL for entity resolution
  'sameAs': [
    'https://www.linkedin.com/company/your-company',
    'https://github.com/your-org',
    'https://www.wikidata.org/entity/QXXXXXXX',  // Your Wikidata QID
  ],
})

// ============================================================
// 2. WebSite — Digital presence
// ============================================================

export const generateWebSiteSchema = () => ({
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': WEBSITE_ID,
  'name': `${ORG_NAME} - Your Tagline`,
  'url': SITE_URL,
  'description': 'Site-level description (different from org description).',
  'publisher': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
  },
})

// ============================================================
// 3. BreadcrumbList — Hierarchical navigation
// ============================================================

export const generateBreadcrumbSchema = (
  breadcrumbs: Array<{ name: string; url: string }>
) => ({
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  'itemListElement': breadcrumbs.map((crumb, index) => ({
    '@type': 'ListItem',
    'position': index + 1,
    'name': crumb.name,
    'item': crumb.url,
  })),
})

// ============================================================
// 4. Article — Content authority
// ============================================================

export const generateArticleSchema = (article: {
  title: string
  description: string
  url: string
  datePublished: string
  dateModified?: string
  author: string | { name: string; id: string }
  image: string
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Article',
  'headline': article.title,
  'description': article.description,
  'url': article.url,
  'datePublished': article.datePublished,
  'dateModified': article.dateModified || article.datePublished,

  // Author can be Organization (string) or Person (object with @id)
  'author':
    typeof article.author === 'string'
      ? {
          '@type': 'Organization',
          '@id': ORG_ID,
          'name': article.author,
        }
      : {
          '@type': 'Person',
          '@id': `${SITE_URL}/#${article.author.id}`,
          'name': article.author.name,
        },

  'publisher': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
    'logo': {
      '@type': 'ImageObject',
      'url': `${SITE_URL}/logo.png`,
    },
  },

  'image': {
    '@type': 'ImageObject',
    'url': article.image,
  },

  'mainEntityOfPage': {
    '@type': 'WebPage',
    '@id': article.url,
  },
})

// ============================================================
// 5. Person — Individual authority (for core team members)
// ============================================================

export const generateCorePersonSchema = (person: {
  id: string
  name: string
  alternateName?: readonly string[]
  nameEn: string
  jobTitle: string
  description: string
  image: string
  knowsAbout: readonly string[]
  sameAs: readonly string[]
  occupation: readonly string[]
  creator?: readonly {
    readonly type: string
    readonly name: string
    readonly url?: string
  }[]
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Person',
  '@id': `${SITE_URL}/#${person.id}`,
  'name': person.name,
  ...(person.alternateName &&
    person.alternateName.length > 0 && {
      'alternateName': person.alternateName,
    }),
  'jobTitle': person.jobTitle,
  'worksFor': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
  },
  'description': person.description,
  'image': `${SITE_URL}${person.image}`,
  'url': `${SITE_URL}/about`,
  'knowsAbout': person.knowsAbout,
  'sameAs': person.sameAs,
  'hasOccupation': person.occupation.map((occ) => ({
    '@type': 'Occupation',
    'name': occ,
  })),
  ...(person.creator &&
    person.creator.length > 0 && {
      'creator': person.creator.map((work) => ({
        '@type': work.type,
        'name': work.name,
        ...(work.url && { 'url': work.url }),
      })),
    }),
})

// ============================================================
// 6. Service — What you offer
// ============================================================

export const generateServiceSchema = (service: {
  name: string
  description: string
  url?: string
  serviceType: string
  offers?: Array<{ name: string; description: string }>
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Service',
  'name': service.name,
  'description': service.description,
  ...(service.url && { 'url': service.url }),
  'provider': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
    'url': SITE_URL,
  },
  'serviceType': service.serviceType,
  ...(service.offers && {
    'hasOfferCatalog': {
      '@type': 'OfferCatalog',
      'name': service.name,
      'itemListElement': service.offers.map((offer) => ({
        '@type': 'Offer',
        'itemOffered': {
          '@type': 'Service',
          'name': offer.name,
          'description': offer.description,
        },
      })),
    },
  }),
})

// ============================================================
// 7. FAQPage — Q&A authority
// ============================================================

export const generateFAQSchema = (
  faqs: Array<{ question: string; answer: string }>
) => ({
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  'mainEntity': faqs.map((faq) => ({
    '@type': 'Question',
    'name': faq.question,
    'acceptedAnswer': {
      '@type': 'Answer',
      'text': faq.answer,
    },
  })),
})

// ============================================================
// 8. HowTo — Process expertise
// ============================================================

export const generateHowToSchema = (guide: {
  name: string
  description: string
  steps: Array<{ title: string; text: string }>
}) => ({
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  'name': guide.name,
  'description': guide.description,
  'step': guide.steps.map((step, index) => ({
    '@type': 'HowToStep',
    'position': index + 1,
    'name': step.title,
    'text': step.text,
  })),
})

// ============================================================
// 9. Dataset — Data authority
// ============================================================

export const generateDatasetSchema = (dataset: {
  name: string
  description: string
  url: string
  temporalCoverage: string
  spatialCoverage: string
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Dataset',
  'name': dataset.name,
  'description': dataset.description,
  'url': dataset.url,
  'creator': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
  },
  'temporalCoverage': dataset.temporalCoverage,
  'spatialCoverage': {
    '@type': 'Place',
    'name': dataset.spatialCoverage,
  },
})

// ============================================================
// 10. EducationalEvent — Community engagement
// ============================================================

export const generateEducationalEventSchema = (event: {
  name: string
  description: string
  startDate: string
  endDate?: string
  location: string
}) => ({
  '@context': 'https://schema.org',
  '@type': 'EducationalEvent',
  'name': event.name,
  'description': event.description,
  'startDate': event.startDate,
  'endDate': event.endDate || event.startDate,
  'location': {
    '@type': 'Place',
    'name': event.location,
  },
  'organizer': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
  },
})

// ============================================================
// 11. JobPosting — Employment authority
// ============================================================

export interface JobPostingData {
  title: string
  company: string
  location: {
    city: string
    region: string
    address?: string
  }
  salary: {
    min: number
    max?: number
    currency: string
  }
  description: string
  datePosted: string
  validThrough: string
  employmentType: 'FULL_TIME' | 'PART_TIME' | 'CONTRACTOR'
  educationRequirements?: string
}

export const generateJobPostingSchema = (job: JobPostingData) => ({
  '@context': 'https://schema.org',
  '@type': 'JobPosting',
  'title': job.title,
  'description': job.description,
  ...(job.educationRequirements && {
    'educationRequirements': {
      '@type': 'EducationalOccupationalCredential',
      'credentialCategory': job.educationRequirements,
    },
  }),
  'hiringOrganization': {
    '@type': 'Organization',
    'name': job.company,
  },
  'jobLocation': {
    '@type': 'Place',
    'address': {
      '@type': 'PostalAddress',
      'addressLocality': job.location.city,
      'addressRegion': job.location.region,
      'streetAddress': job.location.address || '',
      'addressCountry': 'JP',
    },
  },
  'baseSalary': {
    '@type': 'MonetaryAmount',
    'currency': job.salary.currency,
    'value': {
      '@type': 'QuantitativeValue',
      'minValue': job.salary.min,
      'maxValue': job.salary.max || job.salary.min,
      'unitText': 'MONTH',
    },
  },
  'datePosted': job.datePosted,
  'validThrough': job.validThrough,
  'employmentType': job.employmentType,
})

// ============================================================
// 12. Periodical — Publication authority
// ============================================================

export const generatePeriodicalSchema = (periodical: {
  name: string
  description: string
  url: string
  genre: string[]
  isAccessibleForFree: boolean
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Periodical',
  'name': periodical.name,
  'description': periodical.description,
  'url': periodical.url,
  'publisher': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
  },
  'genre': periodical.genre,
  'isAccessibleForFree': periodical.isAccessibleForFree,
})

// ============================================================
// 13. PublicationIssue — Issue-level detail
// ============================================================

export const generatePublicationIssueSchema = (issue: {
  issueNumber: string
  datePublished: string
  name: string
  description: string
  url: string
  coverImage: string
  periodicalName: string
}) => ({
  '@context': 'https://schema.org',
  '@type': 'PublicationIssue',
  'issueNumber': issue.issueNumber,
  'datePublished': issue.datePublished,
  'name': issue.name,
  'description': issue.description,
  'url': issue.url,
  'image': issue.coverImage,
  'isPartOf': {
    '@type': 'Periodical',
    'name': issue.periodicalName,
  },
  'publisher': {
    '@type': 'Organization',
    '@id': ORG_ID,
    'name': ORG_NAME,
  },
})

// ============================================================
// 14. LocalBusiness — Physical presence
// ============================================================

export const generateLocalBusinessSchema = (business: {
  name: string
  description: string
  telephone: string
  address: {
    street?: string
    city: string
    region: string
    country: string
  }
  geo: { latitude: number; longitude: number }
  openingHours: {
    days: string[]
    opens: string
    closes: string
  }
}) => ({
  '@context': 'https://schema.org',
  '@type': ['LocalBusiness', 'EmploymentAgency'],
  '@id': ORG_ID,  // Same @id as Organization — they ARE the same entity
  'name': business.name,
  'description': business.description,
  'url': SITE_URL,
  'telephone': business.telephone,
  'address': {
    '@type': 'PostalAddress',
    'streetAddress': business.address.street || '',
    'addressLocality': business.address.city,
    'addressRegion': business.address.region,
    'addressCountry': business.address.country,
  },
  'geo': {
    '@type': 'GeoCoordinates',
    'latitude': business.geo.latitude,
    'longitude': business.geo.longitude,
  },
  'openingHoursSpecification': {
    '@type': 'OpeningHoursSpecification',
    'dayOfWeek': business.openingHours.days,
    'opens': business.openingHours.opens,
    'closes': business.openingHours.closes,
  },
})

// ============================================================
// 15-18. Additional types (Occupation, CreativeWork, etc.)
// are embedded within Person and Organization schemas above.
// They don't need standalone generators — they exist as
// nested objects within the entity graph.
// ============================================================

// ============================================================
// Usage Example — Connecting Everything
// ============================================================
//
// In your homepage layout:
//
//   const orgSchema = generateOrganizationSchema()
//   const siteSchema = generateWebSiteSchema()
//   const breadcrumbs = generateBreadcrumbSchema([
//     { name: 'Home', url: SITE_URL },
//   ])
//
// In your article pages:
//
//   const articleSchema = generateArticleSchema({
//     title: 'Article Title',
//     description: 'Article description',
//     url: `${SITE_URL}/blog/article-slug`,
//     datePublished: '2025-01-01',
//     author: { name: 'Author Name', id: 'person-author-name' },
//     image: `${SITE_URL}/images/article.jpg`,
//   })
//
// In your about/team page:
//
//   const founderSchema = generateCorePersonSchema({
//     id: 'person-founder-name',
//     name: 'Founder Name',
//     nameEn: 'Founder Name',
//     jobTitle: 'CEO',
//     description: 'Detailed description...',
//     image: '/images/founder.jpg',
//     knowsAbout: ['Domain 1', 'Domain 2'],
//     sameAs: ['https://linkedin.com/in/...', 'https://wikidata.org/entity/Q...'],
//     occupation: ['Title 1', 'Title 2'],
//   })
//
// The key: every schema that references a Person uses the same @id.
// Every schema that references the Organization uses ORG_ID.
// This creates one connected graph, not isolated data points.
