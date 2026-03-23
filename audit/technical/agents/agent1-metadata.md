# 漆畑式LLMO Technical Audit — Agent 1: メタデータ監査ガイド

## 調査対象
- 全 page.tsx / layout.tsx のメタデータ export（title, description, openGraph, twitter）
- canonical URL の設定状況
- viewport 設定
- favicon / apple-touch-icon 設定
- OGP画像の設定状況（個別化率・動的生成の有無）
- metadataBase の設定
- Google/Bing verification

## メタデータ継承ルール（誤検知防止・最重要）

Next.js App Router では、page.tsx 自体に metadata export がなくても、
同ディレクトリまたは親ディレクトリの layout.tsx で metadata が定義されていれば
そのページはメタデータ「カバー済み」と判定する。

### 判定手順（必ずこの順序で確認）
1. page.tsx に `metadata` / `generateMetadata` があるか確認
2. なければ、同ディレクトリの layout.tsx を確認
3. それもなければ、親ディレクトリの layout.tsx を再帰的に確認
4. ルート layout.tsx まで遡っても title/description がなければ「未設定」と判定

### 禁止事項
- `'use client'` だからメタデータなし、と即断しないこと
- layout.tsx でカバーされているページは「カバー済み」として報告すること
- ルートlayout.tsx のデフォルトメタデータでカバーされるページを「未設定」と報告しないこと

## 調査手順

### Step 1: ルートlayout.tsx の確認
`src/app/layout.tsx` を READ し、以下を記録:
- title（default + template）
- description
- keywords
- metadataBase
- openGraph 設定
- twitter 設定
- robots 設定
- icons 設定
- verification 設定

### Step 2: 全page.tsx の列挙
`glob` で `src/app/**/page.tsx` を全件取得し、ファイル数を記録。

### Step 3: カバレッジ判定
各 page.tsx について:
1. 自身に metadata export があるか → 「直接設定」
2. 同ディレクトリの layout.tsx に metadata があるか → 「layout経由」
3. 親ディレクトリの layout.tsx に metadata があるか → 「親layout経由」
4. ルート layout.tsx のみ → 「ルートlayout経由」
5. どこにもない → 「未設定」（このケースのみ不備として報告）

### Step 4: 品質チェック
- OGP画像が設定されているページ数
- canonical URL が設定されているページ数
- 動的メタデータ（generateMetadata）を使用しているページ

## OG画像の個別化率チェック（重要）

### 目的
汎用OG画像（og-image.jpg, og-default.png等）へのフォールバック率を計測する。
SNS共有時やAI検索結果での視認性に直結するため重要。

### 手順
1. `openGraph.images` が個別設定されているページ数を計測
   - grepで `images:` を含む metadata/openGraph ブロックを持つファイルを数える
   - layout.tsx でimages が設定されている場合、配下の全ページはカバー済み
2. 個別設定されていないページ = ルートlayoutのデフォルトにフォールバック
3. 個別化率 = 個別設定数 / 全ページ数

### 3層評価（重要度別に報告）
| 層 | 対象 | 期待 |
|----|------|------|
| Tier 2 | セクションTOP・ハブページ | カスタム画像 or 動的OGルート |
| Tier 3 | コンテンツページ（記事・サブページ） | 動的OGルート `/api/og` 経由 |

### OG画像動的生成の確認
- `src/app/api/og/route.tsx` が存在するか確認
- Next.js ImageResponse (Satori) の利用有無
- 動的OGルートのパラメータ仕様（title, category, image等）
- Edge Runtime で外部画像fetchが正常に動作するか
- フォールバック処理（画像404時にクラッシュしないか）

### カスタムOG作成リストとの照合
- `[your OG image checklist document]` が存在すれば READ し、
  未作成件数と進捗を報告する

### 評価基準
- Tier 1 が100%個別化 + Tier 3 が動的OG対応: ✅ 良好
- Tier 1 に汎用画像が残っている: ❌ 最優先で対応
- 動的OGルートが存在しない: ⚠️ 改善推奨

## 出力フォーマット
- ルートlayout.tsx の設定内容
- メタデータカバレッジ: X/Y ページ (Z%)
- カバー元の内訳（直接 / layout経由 / ルートlayout経由）
- OG画像個別化率: Tier別の表
- カスタムOG作成リストの進捗（あれば）
- 真に未設定のページ一覧（あれば）
- 改善推奨事項
- スコア: X/10
