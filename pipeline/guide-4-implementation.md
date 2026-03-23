# 漆畑式LLMO Pipeline — Step 4: 実装 / Implementation

**目的: 構成案と執筆済みコンテンツを受け取り、既存のデザインパターンに従ってページを実装する。**

**大前提: オリジナルデザインは作らない。**
**トラック固有のコンポーネント・データ登録先はトラック設定ファイル（CONFIG）を参照すること。**

---

## このガイドの使い方

1. 構成案（セクション構成・テーマ色）と執筆済みテキストを受け取る
2. **トラック設定ファイル（CONFIG）を読み、使用コンポーネント・データ登録先を確認する**
3. このガイドの共通パターンと CONFIG の固有パターンを組み合わせて実装する
4. 新しいデザインを発明しない。ここにないパターンが必要な場合はユーザーに相談する

---

## ファイル構成（2ファイル構成・共通）

### page.tsx（server component）

メタデータと構造化データのみ。レイアウト・スタイルの記述をしない。

```tsx
import { Metadata } from 'next'
import XxxContent from './XxxContent'
import StructuredData from '@/components/StructuredData'
import {
  generateBreadcrumbSchema,
  generateArticleSchema,
  generateOrganizationSchema,
} from '@/lib/structured-data'

export const metadata: Metadata = {
  title: 'ページタイトル | セクション名 | サイト名',
  description: 'ページの説明文（120文字程度）',
  keywords: ['キーワード1', 'キーワード2'],
  openGraph: {
    title: 'ページタイトル',
    description: 'ページの説明文',
    url: 'https://[YOUR_DOMAIN]/path/slug',
    type: 'article',
    images: [{ url: '/api/og?title=ページタイトル&category=[CATEGORY]', width: 1200, height: 630, alt: 'ページタイトル' }],
  },
  alternates: {
    canonical: '/path/slug',
  },
}

// breadcrumbSchema, articleSchema, organizationSchema は CONFIG のURL構造に従う

export default function XxxPage() {
  const organizationSchema = generateOrganizationSchema()
  // breadcrumbSchema, articleSchema もここで生成

  return (
    <>
      <StructuredData data={[breadcrumbSchema, articleSchema, organizationSchema]} />
      <XxxContent />
    </>
  )
}
```

### XxxContent.tsx（client component）

UIロジック・レイアウト・全セクションの実装。

```tsx
'use client'

import Link from 'next/link'
import Image from 'next/image'
// アイコン、CTA コンポーネントは CONFIG に従って選択
```

---

## 共通セクションパターン

### パターン1: テキストセクション（最も基本）

```tsx
<section className="mb-12">
  <h2 className="text-2xl font-bold text-gray-900 mb-2">見出し</h2>
  <p className="text-gray-700 mb-6">導入文</p>

  <div className="space-y-3">
    <div className="bg-white rounded-2xl px-5 py-4">
      <h3 className="font-bold text-gray-900 mb-1">小見出し</h3>
      <p className="text-[15px] text-gray-700 leading-relaxed">
        本文テキスト
      </p>
    </div>
  </div>
</section>
```

### パターン2: ステップ番号付きカード

```tsx
<div className="space-y-3">
  <div className="bg-white rounded-2xl px-5 py-4">
    <div className="flex items-start gap-3">
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-[THEME]-600 text-white text-xs font-bold flex-shrink-0 mt-0.5">1</span>
      <div>
        <h3 className="font-bold text-gray-900 mb-1">ステップ名</h3>
        <p className="text-[15px] text-gray-700 leading-relaxed">説明文</p>
      </div>
    </div>
  </div>
</div>
```

### パターン3: タイムライン

```tsx
<div className="bg-white rounded-2xl p-6">
  <div className="space-y-0">
    {[
      { time: '10分前', label: '到着', detail: '説明文' },
    ].map((item, i, arr) => (
      <div key={item.label} className={`flex gap-4 ${i < arr.length - 1 ? 'pb-5 border-b border-gray-100' : ''} ${i > 0 ? 'pt-5' : ''}`}>
        <div className="w-16 flex-shrink-0 text-right">
          {item.time && <span className="text-sm font-bold text-[THEME]-600">{item.time}</span>}
        </div>
        <div className="flex-1">
          <h3 className="font-bold text-gray-900 mb-1">{item.label}</h3>
          <p className="text-[15px] text-gray-700 leading-relaxed">{item.detail}</p>
        </div>
      </div>
    ))}
  </div>
</div>
```

### パターン4: 補足ボックス（テーマ色-50）

```tsx
<div className="bg-[THEME]-50 rounded-xl p-4 mt-4">
  <p className="text-[15px] text-gray-700 leading-relaxed">補足情報</p>
</div>
```

### パターン5: フルワイド背景（注意喚起）

```tsx
<section className="mb-12">
  <div className="relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] w-screen bg-amber-100 px-6 py-10">
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">見出し</h2>
      <div className="space-y-3">
        {/* 白カードを並べる */}
      </div>
    </div>
  </div>
</section>
```

### パターン6: チェックリスト

```tsx
<div className="space-y-2">
  {['項目1', '項目2'].map(item => (
    <div key={item} className="flex items-start gap-2">
      <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
      <p className="text-[15px] text-gray-700">{item}</p>
    </div>
  ))}
</div>
```

---

## 出典セクション（共通）

```tsx
<div className="text-xs text-gray-400 mb-12 space-y-1">
  <p className="font-medium text-gray-500">この記事のデータ出典</p>
  <p>組織名「資料名」（年度）</p>
</div>
```

---

## 色体系

プロジェクト固有のデザインシステムに従うこと。CONFIG または別途定義されたカラーパレットを参照する。

一般的な考え方として、テーマ色は**コンテンツの性質**に対応させる:

| 性質 | 用途例 |
|------|-------|
| スケジュール・技術系 | 寒色系 |
| 探索・発見系 | ティール系 |
| 応募・選択・行動系 | 暖色系 |
| 作成・達成系 | グリーン系 |
| 対人・コミュニケーション系 | 水色系 |
| 結果・感情系 | ローズ系 |
| 準備・実用系 | アンバー系 |

---

## 禁止事項（共通・厳守）

- **グラデーション:** 全面禁止
- **装飾的サイドライン:** `border-l-4` 等の左ライン禁止（囲み枠はOK）
- **絵文字アイコン:** 禁止（SVGアイコンライブラリを使う）
- **スワイプUI:** 禁止
- **コントラスト不足のテキスト色:** 白背景上では十分なコントラストを確保する
- **サブテキストの色分け:** タイトルと違う色にしない
- **SaaS風グラデーション・無意味なシャドウ:** 禁止

**上記に加えて、プロジェクト固有の禁止事項がある場合は CONFIG を参照すること。**

---

## SEO/LLMO 世界最高峰基準（全コンテンツ必須）

### 構造化データ（JSON-LD）

**全新規ページに以下の3スキーマを必ず含めること:**

1. **BreadcrumbSchema** — パンくずリスト
2. **ArticleSchema** — 記事情報
3. **OrganizationSchema** — 組織情報

```tsx
// 正しい: 集中管理関数を使用
import { generateBreadcrumbSchema, generateArticleSchema, generateOrganizationSchema } from '@/lib/structured-data'
const organizationSchema = generateOrganizationSchema()

// 禁止: Organizationをハードコード
const organizationSchema = { '@context': 'https://schema.org', '@type': 'Organization', ... }
```

**FAQがある記事は `faqSchema` も追加する。**

**出力は必ず構造化データ用コンポーネント経由:**
```tsx
import StructuredData from '@/components/StructuredData'
<StructuredData data={[breadcrumbSchema, articleSchema, organizationSchema]} />
```

### OG画像（動的OG）

全新規ページの metadata.openGraph に images を設定すること。動的OG画像APIがある場合はそれを使用する。

### RSC / Client 分離

- `page.tsx` は **Server Component**（メタデータ + 構造化データ + Content import のみ）
- `XxxContent.tsx` は **Client Component**（`'use client'` + UI ロジック）
- `'use client'` は **本当に必要な場合のみ** 付与（useState/useEffect/onClick等を使う場合）
- 静的コンテンツのみのContent.tsxには `'use client'` を付けない

### セマンティックHTML

- 記事本文を `<article>` で囲む
- 各セクションを `<section>` で囲む
- 画像+キャプションは `<figure>` + `<figcaption>` を使用
- 日付は `<time datetime="YYYY-MM-DD">` を使用

### 画像

画像の生成・ホスティング方法はプロジェクト固有の設定に従うこと。CONFIG または別途定義された画像管理ガイドを参照する。
