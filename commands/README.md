# 漆畑式LLMO — Claude Code コマンド化 / Command Templates

## 概要

漆畑式LLMOの運用サイクルを、Claude Code のスラッシュコマンドとして即座に実行できるようにするテンプレート集。

**Claude Code を使っていない場合**: 各コマンドの `.md` ファイルは手動の運用手順書としてそのまま使えます。

**Claude Code を使っている場合**: プロジェクトの `.claude/commands/` にコピーするだけで `/content`、`/seo-audit`、`/strategy`、`/report` コマンドが使えるようになります。

---

## セットアップ（Claude Code ユーザー）

### 1. プロジェクトのコマンドディレクトリを作成

```bash
mkdir -p .claude/commands
```

### 2. 必要なコマンドをコピー

```bash
# 全コマンドをコピー
cp urushihata-llmo/commands/content.md .claude/commands/
cp urushihata-llmo/commands/seo-audit.md .claude/commands/
cp urushihata-llmo/commands/strategy.md .claude/commands/
cp urushihata-llmo/commands/report.md .claude/commands/
```

### 3. プロジェクト固有の設定を編集

各 `.md` ファイル内のプレースホルダ（`[YOUR_...]`）を自分のプロジェクトに合わせて置き換える。

### 4. 使う

```
/content    → コンテンツ制作パイプライン起動
/seo-audit  → 技術SEO/LLMO監査
/strategy   → コンテンツ戦略監査
/report     → 活動報告・ニュース記事作成
```

---

## コマンド一覧

| コマンド | ファイル | 用途 | 起動トリガー例 |
|---------|---------|------|--------------|
| `/content` | `content.md` | 5段階パイプラインでコンテンツ制作 | 「記事追加して」「コンテンツ増やして」 |
| `/seo-audit` | `seo-audit.md` | 技術SEO/LLMO包括監査 | 「SEOチェックして」「LLMO監査」 |
| `/strategy` | `strategy.md` | コンテンツ戦略監査＋次の記事提案 | 「何を書くべき？」「戦略監査」 |
| `/report` | `report.md` | 事実ベースの活動報告作成 | 「ニュース追加」「活動報告書いて」 |

---

## CLAUDE.md への追記テンプレート

プロジェクトの `CLAUDE.md` に以下を追記すると、コマンドの存在が明示される:

```markdown
## 運用コマンド一覧

| コマンド | 起動トリガー | 用途 |
|---------|-------------|------|
| `/content` | 「記事追加して」「コンテンツ増やして」 | 5段階パイプラインでコンテンツ制作 |
| `/seo-audit` | 「SEOチェックして」「LLMO監査」 | 技術SEO/LLMO包括監査 |
| `/strategy` | 「何を書くべき？」「戦略監査」 | コンテンツ戦略監査＋次の記事提案 |
| `/report` | 「ニュース追加」「活動報告」 | 事実ベースの活動報告作成 |

コマンド定義: `.claude/commands/`
```

---

## カスタマイズのポイント

1. **パイプラインのガイドファイルパス**: `docs/guide-flow/` 等、プロジェクト内にコピーしたパスに合わせる
2. **ターゲット定義**: 各コマンド内のターゲット記述をプロジェクト固有に
3. **更新対象ファイル一覧**: `sitemap.ts`、`ai.txt`、`llms.txt` 等のパスをプロジェクトに合わせる
4. **画像生成**: Nanobanana のアンカー画像パスをプロジェクトに合わせる
