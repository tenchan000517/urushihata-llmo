/**
 * Dynamic OG Image Generation — Next.js Edge Runtime
 *
 * Generates category-aware Open Graph images on the fly.
 * This is the implementation pattern used to generate 984 unique
 * OG images without storing a single static file.
 *
 * WHY THIS MATTERS FOR LLMO:
 * - Every page gets a unique, contextual preview image
 * - Category badges signal content type to both humans and AI
 * - Consistent branding across 1,000+ pages without manual design work
 *
 * USAGE:
 *   /api/og?title=Page Title&category=blog
 *   /api/og?title=Page Title&category=service&image=https://example.com/image.png
 *
 * PARAMETERS:
 *   - title: Page title (required)
 *   - category: Category key for color/badge (optional, defaults to 'default')
 *   - image: Custom image URL for left column (optional)
 *   - subtitle: Subtitle text (optional)
 */

import { ImageResponse } from 'next/og'
import { NextRequest } from 'next/server'

export const runtime = 'edge'

// ============================================================
// Category Configuration
// Customize these for your site's content types.
// Each category gets a unique accent color and badge label.
// ============================================================

const CATEGORY_CONFIG: Record<
  string,
  { accent: string; badge: string; defaultImage: string }
> = {
  blog: {
    accent: '#059669',    // Emerald
    badge: 'Blog',
    defaultImage: 'https://example.com/images/blog-default.png',
  },
  service: {
    accent: '#2563eb',    // Blue
    badge: 'Service',
    defaultImage: 'https://example.com/images/service-default.png',
  },
  guide: {
    accent: '#7c3aed',    // Violet
    badge: 'Guide',
    defaultImage: 'https://example.com/images/guide-default.png',
  },
  product: {
    accent: '#ea580c',    // Orange
    badge: 'Product',
    defaultImage: 'https://example.com/images/product-default.png',
  },
  career: {
    accent: '#0d9488',    // Teal
    badge: 'Career',
    defaultImage: 'https://example.com/images/career-default.png',
  },
  default: {
    accent: '#374151',    // Gray
    badge: 'Your Brand',
    defaultImage: 'https://example.com/og-image.jpg',
  },
}

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl
  const title = searchParams.get('title') || 'Your Site Name'
  const category = searchParams.get('category') || 'default'
  const subtitle = searchParams.get('subtitle') || ''
  const imageUrl = searchParams.get('image') || ''

  const config = CATEGORY_CONFIG[category] || CATEGORY_CONFIG.default

  // Determine display image: custom > category default
  let displayImage = imageUrl || config.defaultImage

  // Validate custom image URL (skip for defaults — we trust those)
  if (imageUrl) {
    try {
      const res = await fetch(imageUrl, {
        method: 'HEAD',
        signal: AbortSignal.timeout(3000),
      })
      if (!res.ok || !res.headers.get('content-type')?.startsWith('image/')) {
        displayImage = config.defaultImage
      }
    } catch {
      displayImage = config.defaultImage
    }
  }

  // Adaptive title sizing
  const displayTitle =
    title.length > 50 ? title.slice(0, 47) + '…' : title
  const titleSize =
    displayTitle.length > 35
      ? 32
      : displayTitle.length > 22
        ? 38
        : 44

  try {
    return new ImageResponse(
      (
        <div
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            backgroundColor: '#ffffff',
            fontFamily: '"Noto Sans JP", "Hiragino Sans", sans-serif',
          }}
        >
          {/* Left column: Image (1/3) */}
          <div
            style={{
              width: '400px',
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: '#f3f4f6',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={displayImage}
              alt=""
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
              }}
            />
            {/* Accent color line (right edge of image) */}
            <div
              style={{
                position: 'absolute',
                right: 0,
                top: 0,
                bottom: 0,
                width: '4px',
                backgroundColor: config.accent,
              }}
            />
          </div>

          {/* Right column: Text (2/3) */}
          <div
            style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              padding: '48px 52px',
            }}
          >
            {/* Top: Category badge */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
              <div
                style={{
                  backgroundColor: config.accent,
                  color: '#ffffff',
                  padding: '6px 18px',
                  borderRadius: '20px',
                  fontSize: '16px',
                  fontWeight: 700,
                }}
              >
                {config.badge}
              </div>
              {subtitle && (
                <div style={{ color: '#6b7280', fontSize: '16px' }}>
                  {subtitle}
                </div>
              )}
            </div>

            {/* Center: Title */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                flex: 1,
                paddingTop: '16px',
                paddingBottom: '16px',
              }}
            >
              <div
                style={{
                  fontSize: titleSize,
                  fontWeight: 900,
                  color: '#111827',
                  lineHeight: 1.35,
                  letterSpacing: '-0.02em',
                }}
              >
                {displayTitle}
              </div>
            </div>

            {/* Bottom: Brand bar */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                borderTop: `3px solid ${config.accent}`,
                paddingTop: '20px',
              }}
            >
              <div
                style={{
                  fontSize: '24px',
                  fontWeight: 900,
                  color: config.accent,
                  letterSpacing: '-0.03em',
                }}
              >
                Your Brand
              </div>
              <div
                style={{
                  color: '#374151',
                  fontSize: '15px',
                  fontWeight: 600,
                }}
              >
                example.com
              </div>
            </div>
          </div>
        </div>
      ),
      {
        width: 1200,
        height: 630,
      }
    )
  } catch {
    // Fallback: text-only image when Satori rendering fails
    return new ImageResponse(
      (
        <div
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: '#ffffff',
            padding: '60px',
            fontFamily: '"Noto Sans JP", "Hiragino Sans", sans-serif',
          }}
        >
          <div
            style={{
              fontSize: 20,
              fontWeight: 700,
              color: config.accent,
              marginBottom: '16px',
            }}
          >
            {config.badge}
          </div>
          <div
            style={{
              fontSize: 40,
              fontWeight: 900,
              color: '#111827',
              textAlign: 'center',
              lineHeight: 1.3,
            }}
          >
            {displayTitle}
          </div>
          <div
            style={{
              fontSize: 20,
              fontWeight: 600,
              color: '#374151',
              marginTop: '24px',
            }}
          >
            example.com
          </div>
        </div>
      ),
      { width: 1200, height: 630 }
    )
  }
}
