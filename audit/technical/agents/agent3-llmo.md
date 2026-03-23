# 漆畑式LLMO Technical Audit — Agent 3: LLMO対策監査ガイド

## 調査対象
- robots.txt の内容（AIクローラー許可設定）
- ai.txt / llms.txt の存在と内容
- サイトマップの網羅性
- セマンティックHTML の使用状況
- RAG最適化コンポーネント（AiSummary等）のカバレッジ
- AI Bot 検出 Middleware の有無

## robots.txt 検出ルール（誤検知防止・最重要）

### 禁止事項
- `public/robots.txt` だけを確認して「存在しない」と結論づけること

### 必須手順 — 以下の全パスを順番に確認すること
1. `public/robots.txt`（静的ファイル）
2. `src/app/robots.txt/route.ts`（Next.js App Router ルートハンドラー）
3. `src/app/robots.ts`（Next.js メタデータAPI）
4. `pages/api/robots.ts`（Pages Router API）

いずれか1つでも見つかれば「存在する」と判定し、その内容を READ して報告する。
Next.js では robots.txt をルートハンドラーで動的生成するのが一般的なパターン。

### チェック対象AIクローラー
| クローラー | 用途 |
|-----------|------|
| GPTBot | OpenAI GPT |
| ChatGPT-User | ChatGPT ブラウジング |
| OAI-SearchBot | OpenAI 検索 |
| Claude-Web | Anthropic Claude |
| anthropic-ai | Anthropic 汎用 |
| Applebot-Extended | Apple Intelligence |
| PerplexityBot | Perplexity AI |
| Google-Extended | Google AI/Gemini |
| Bytespider | ByteDance/TikTok |
| CCBot | Common Crawl |

各クローラーについて Allow/Disallow/未設定 を表形式で報告する。

## ai.txt / llms.txt

### 検索パス
- `public/ai.txt`
- `public/llms.txt`

### 品質評価基準（存在する場合）
| 項目 | 基準 |
|------|------|
| ファイルサイズ | ai.txt: 1,000行以上で✅、llms.txt: 200行以上で✅ |
| ペルソナ別構造 | ターゲット（企業/高校生/保護者等）別にセクション分割されているか |
| URL マッピング | 主要コンテンツの直接URLが記載されているか |
| 出典ガイドライン | AI引用時の出典表記ルールが記載されているか |
| 最終更新日 | ファイルの更新日が1ヶ月以内か |
| クローラー許可宣言 | ai.txt 内でクローラー許可を明示しているか |

## RAG最適化コンポーネント監査（重要・新規）

### 目的
AIが正確にページの主張を引用（RAG）するために、自己完結した
サマリーブロックが重要ページに配置されているかを確認する。

### 検出手順
1. `grep -r "AiSummary" src/` でコンポーネントの使用箇所を特定
2. コンポーネントが存在しない場合:
   - `<section aria-label` + 完全文の `<p>` タグの組み合わせを代替として検出
3. 使用箇所のページパスをリストアップ



### 品質チェック
AiSummary が存在する場合、以下を確認:
- `entityName`: エンティティ名が明確か
- `definition`: 主語+述語が完結した一文か（断片的な語句ではないか）
- `keyFacts`: 具体的な数値や実績を含むか
- `provider`: 提供者が明示されているか

## AI Bot Middleware 監査（新規）

### 目的
AIクローラーからのアクセスを検出・ログ収集・レスポンス最適化する
Middleware の有無を確認する。

### 検出手順
1. `src/middleware.ts` の存在確認
2. 存在する場合、User-Agent によるAIボット判定ロジックの有無
3. AIボット向けのレスポンスヘッダー調整の有無
4. ログ収集（console.log, 外部サービスへの送信等）の有無

### 評価基準
- Middleware でAIボットを検出+ログ収集: ✅ 良好
- robots.txt でのみ対応: ⚠️ 基本レベル（最低限OK）
- どちらもなし: ❌ 要対応

## サイトマップ網羅性チェック（誤検知防止・最重要）

### 禁止事項
- sitemap ファイルを部分的にしか読まずに「このページが不足」と結論づけること
- ハードコードされたURLだけを数えて「N件のみ」と結論づけること

### 必須手順
1. `src/app/sitemap.ts` を最初から最後まで完全に READ する（長い場合は分割して全行読む）
2. sitemap に登録されている全URLをリスト化する
3. `glob` で全 `page.tsx` を取得する
4. 両者を突合し、実際に不足しているページだけを報告する
5. dashboard/, test-*, api/ 等の意図的な除外は「正しく除外」として報告する

### 動的生成パターンの検出（必須）
sitemap.ts 内で以下のパターンを見逃さないこと:
- `array.map()` でURLを動的生成している箇所（配列からの展開）
- `generateStaticParams` の結果をsitemapに反映している箇所
- スプレッド構文 `...` でURLを展開している箇所
→ これらの動的パターンが生成するURL数を正確にカウントし、合計に加算すること。
→ sitemap を途中まで読んで「この先にはないだろう」と推測しないこと。

## セマンティックHTML 検出ルール（誤検知防止・重要）

### 禁止事項
- 定量データなしで「セマンティックHTMLが弱い」と定性的に判断すること

### 必須手順
grep の count モードで各タグの出現回数を計測する:
```
<article, <section, <time, <figure, <figcaption, <aside, <nav, <header, <footer, <main
```
比較として `<div` の出現回数も計測する。

### レイアウト経由のカバー判定
- layout.tsx で `<main>`, `<header>`, `<footer>`, `<nav>` が定義されていれば全ページカバー済み
- 共有 Header/Footer コンポーネント内の使用もカバー済み
- `<article>`, `<time>`, `<figure>` は個別ページ単位で確認する

## 出力フォーマット
- robots.txt: AIクローラー許可状況の表
- ai.txt / llms.txt: 存在有無、サイズ、品質評価（上記基準の表）
