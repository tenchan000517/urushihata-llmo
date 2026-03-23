# 漆畑式LLMO Technical Audit — Agent 2: 構造化データ監査ガイド

## 調査対象
- JSON-LD / Schema.org の実装
- 実装済みスキーマ一覧
- スキーマヘルパー関数の有無（src/lib/ や src/utils/ 内）
- 構造化データが適用されるべきだが未適用のページ
- 定義済みだが未使用のスキーマ関数の特定
- Organization スキーマの集中管理度
- エンティティ間の @id 相互参照

## 構造化データ検出ルール（誤検知防止・最重要）

### 禁止事項
- grepの結果だけで「このページはスキーマなし」と結論づけること
- page.tsx に StructuredData の直接importがないことだけで「未カバー」と判定すること
- 共有コンポーネント内部を確認せずにカバレッジを算出すること

### カバー済み判定の経路（すべてチェック）
1. page.tsx 内に直接 StructuredData / generateXxxSchema / application/ld+json があるか
2. **page.tsx がインポートしている共通コンポーネントの実装を読み、StructuredData を含むか確認する**
3. 同ディレクトリまたは親ディレクトリの layout.tsx
4. どの経路にもなければ初めて「未設定」と判定

## 調査手順

### Step 1: スキーマヘルパー関数の特定
`src/lib/` や `src/utils/` 内で `Schema` や `structured` を含むファイルを検索。
見つかったファイルを READ し、全 export 関数をリストアップ。

### Step 2: 共有テンプレートコンポーネントの特定（最重要）

**この手順を省略してはならない。**

1. `grep -r "StructuredData" src/components/` を実行
   → StructuredData を含む共有コンポーネント一覧を取得
   （例: IndustryGuide.tsx, JobGuide.tsx, CompanyTemplate.tsx 等）

2. 各共有コンポーネントを READ し、どのスキーマを注入しているか記録
   （例: IndustryGuide.tsx → ArticleSchema + BreadcrumbSchema）

3. 各共有コンポーネントの名前で page.tsx からの import を検索:
   `grep -r "import.*IndustryGuide" src/app/`
   → このコンポーネントを使う全ページを「コンポーネント経由でカバー済み」に分類

4. 同一コンポーネントを使う複数ページ（例: 11の業界ガイドが全て IndustryGuide を使用）は
   まとめてカバー済みとカウントする

### Step 3: layout.tsx 経由の構造化データ
`grep -r "StructuredData" src/app/**/layout.tsx` を実行。
layout.tsx で注入されているスキーマは、その配下の全ページに適用される。

### Step 4: 直接実装のページ
`grep -r "StructuredData\|generateArticleSchema\|generateBreadcrumbSchema" src/app/**/page.tsx`

### Step 5: カバレッジ算出
以下の3経路を合算:
- 直接実装（page.tsx 内）
- 共有コンポーネント経由（Step 2 で特定）
- layout.tsx 経由（Step 3 で特定）

カバレッジ = (直接 + コンポーネント経由 + layout経由) / 全page.tsx数

### Step 6: Organization スキーマの集中管理チェック（重要）

**目的**: ハードコードされた Organization スキーマが各ページに散在していると、
会社情報変更時に不整合が起きる。集中管理 (`generateOrganizationSchema()`) を推奨。

1. `grep -r "organizationSchema = {" src/app/` でハードコード件数を計測
2. `grep -r "generateOrganizationSchema" src/app/` で集中管理件数を計測
3. 集中管理率 = 集中管理 / (ハードコード + 集中管理)

**評価基準:**
- 100% 集中管理: ✅ 良好
- ハードコードが残存: ⚠️ 改善推奨（特に県数など変動する情報がハードコードされている場合は❌）

### Step 7: エンティティ @id 相互参照チェック

**目的**: Organization, Article, Person 等のスキーマが `@id` で相互リンクされているか。
AIのナレッジグラフ構築に直結する。

1. `grep -r "@id" src/lib/structured-data.ts` で @id の定義箇所を確認
2. 各スキーマの `publisher`, `author`, `mainEntityOfPage` が @id で参照しているか確認
3. 参照チェーン: Article → Organization (publisher) → Person (founder) が繋がっているか

**評価基準:**
- 3階層以上の参照チェーン: ✅ 良好
- @id 未使用: ⚠️ 改善推奨

### Step 8: 未使用スキーマ関数の特定
各関数名を `grep` で全 .ts/.tsx ファイルから検索。
- import 行が1箇所でもあれば「使用中」
- .md ドキュメント内での言及は使用にカウントしない
- grep の出力結果を報告に含めること

### Step 9: サンプル検証
「未カバー」と判定したページのうち最低10ページを実際に READ して確認。
1つでも誤検知があれば、方法論を見直して再集計する。

## 出力フォーマット
- スキーマ関数一覧（名前 / 使用状況 / 使用箇所）
- カバレッジ: X/Y ページ (Z%)
  - 内訳: 直接 N件 / コンポーネント経由 N件 / layout経由 N件
- Organization 集中管理率: X% (ハードコードN件 / 集中管理N件)
- エンティティ @id 参照チェーン: 状態
- 真に未カバーのページ一覧
- 未使用スキーマ関数一覧
- 改善推奨事項
- スコア: X/10
