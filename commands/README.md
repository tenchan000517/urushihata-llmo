# 漆畑式LLMO — プロジェクトへのコマンド化ガイド

## この章の目的

漆畑式LLMOは**汎用フレームワーク**だ。そのままでは動かない。
あなたのプロジェクト固有の設定（ターゲット・ブランドボイス・ファイル構造）と結合して初めて動く。

このガイドでは、**漆畑式LLMOを自分のプロジェクトに組み込み、3つのコマンドで回る状態にする方法**を解説する。

---

## 3つのコマンド — これだけで回る

```
/audit    → 何を作るべきか判断する
/content  → 作る
/index    → 届ける
```

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  /audit  │ ──→ │ /content │ ──→ │  /index  │
│ 判断する  │     │  作る    │     │  届ける   │
└──────────┘     └──────────┘     └──────────┘
      ↑                                 │
      └─────────── 計測 ────────────────┘
```

| コマンド | 統合している機能 | やること |
|---------|----------------|---------|
| `/audit` | 戦略監査 + 技術監査 + GA4/SC計測 | データを見て「次に何を作るべきか」を判断する |
| `/content` | 5段階パイプライン + 画像生成 | AGENT-CONFIGに従ってコンテンツを制作する |
| `/index` | インデックス登録 + サイトマップ送信 | 作ったものをGoogleに届ける |

**入り口は3つだけ。** 機能が多くても、ユーザーが叩くコマンドは3つ。

---

## 全体像: 汎用→固有への変換パターン

```
漆畑式LLMO（汎用）              あなたのプロジェクト（固有）
──────────────────────         ──────────────────────────

pipeline/                      docs/guide-flow/
├── guide-1-research.md   →    ├── AGENT-GUIDE-1-research.md（コピー or カスタマイズ）
├── guide-2-...           →    ├── AGENT-GUIDE-2-...
├── guide-3-...           →    ├── AGENT-GUIDE-3-...
├── guide-4-...           →    ├── AGENT-GUIDE-4-...（画像パス・ファイル構成を固有化）
├── guide-5-...           →    ├── AGENT-GUIDE-5-...
└── configs/                   │
    ├── seo-track.md           ├── AGENT-CONFIG.md ← ★ここが最重要
    ├── llmo-track.md          │   ターゲット・ブランドボイス・
    └── user-track.md          │   品質基準・カテゴリ・CTA・URL構造
                               │   全てプロジェクト固有に書き下す
                               └── anchors/（画像生成用アンカー画像）

                               .claude/commands/
                               ├── audit.md    ← 判断する
                               ├── content.md  ← 作る
                               └── index.md    ← 届ける
```

**核心**: 5段階ガイドは汎用のままでも使える。しかし **AGENT-CONFIG は100%プロジェクト固有** で書かなければ意味がない。そしてコマンド定義（`.claude/commands/*.md`）がそれらを繋ぐ接着剤になる。

---

## Step 1: プロジェクト内にガイドを配置する

漆畑式LLMOの `pipeline/` を、プロジェクトの `docs/` 配下にコピーする。

```bash
mkdir -p docs/guide-flow
cp urushihata-llmo/pipeline/guide-*.md docs/guide-flow/
```

ガイド 1〜3（リサーチ・設計・ライティング）はほぼそのまま使える。
ガイド 4（実装）はファイル構成・画像パス・データ登録先をプロジェクトに合わせて編集する。

---

## Step 2: AGENT-CONFIG を書く（最重要）

ここが漆畑式LLMOの真価。テンプレートからコピーするのではなく、**自分のプロジェクトの哲学を書き下す**。

`docs/guide-flow/AGENT-CONFIG.md` を新規作成し、以下のセクションを定義する:

### 必須セクション

```markdown
# エージェント設定 — [プロジェクト名]

## ターゲット定義
誰に向けて書くか。年齢・心理状態・検索行動まで具体的に。

## ブランドボイス
世界観・哲学・口調ルール。OK例とNG例を必ず添える。

## 品質基準
「完成したらこの問いに全てYesと言えること」を4-5個。

## カテゴリ体系
コンテンツのカテゴリ分け。テーマ色・対象キーワード群も定義。

## 構成パターン
カテゴリごとのセクション構成テンプレート。

## CTA・導線
各コンテンツの末尾で読者をどこに導くか。

## URL・配置
ファイルの置き場所・URL構造。

## データ登録
コンテンツ追加時に必ず更新するファイル一覧。

## 画像生成
Nanobananaのアンカー画像パス・スタイルプロンプト。
```

### 実例: SingHD のAGENT-CONFIG（抜粋）

SingHDは「RPGの冒険」をブランド世界観に持つ採用サイト。そのAGENT-CONFIGは:

- **ターゲット**: 20代前半。「安定は大事だけど、このままでいいのか」
- **ブランドボイス**: 人生=冒険、仕事=クエスト、成長=レベルアップ。ただしRPG要素は「装飾」ではなく「体験」として機能させる
- **品質基準**: ① 読んだ後に「次に何をすべきか」わかるか ② Singの哲学が自然に体現されているか ③ RPG要素が体験の骨格として機能しているか ④ 一般論になっていないか ⑤ 冒険診断/エントリーに進みたくなる感情の流れがあるか
- **口調**: 見出しは語りかけ調（「〜ではないか？」）、本文はです/ます体。取って付けた「レベルアップ！」は禁止

**このレベルの具体性で書くこと。** 「ターゲットは20代です」だけでは使えない。

---

## Step 3: 3つのコマンドを定義する（Claude Code ユーザー）

```bash
mkdir -p .claude/commands
```

### `/audit` — 判断する

```markdown
# SEO/LLMO 監査

戦略監査 + 技術監査 + パフォーマンスデータを統合し、
「次に何を作るべきか」を判断する。

---

## 手順

### Phase 1: データ取得
GA4/Search Console の最新データを取得する。
（tools/analytics/ のスクリプトを使用）

### Phase 2: 戦略監査（並列4エージェント）
| Agent | 分析対象 |
|-------|---------|
| 1 | LLMO/AI引用コンテンツのカバレッジ |
| 2 | SEO権威性（KW支配度） |
| 3 | ユーザー向けコンテンツの的確さ |
| 4 | 地域カバレッジ＋トラック間連動 |

### Phase 3: 技術監査（並列5エージェント）
| Agent | 監査領域 |
|-------|---------|
| 1 | メタデータ |
| 2 | 構造化データ |
| 3 | LLMO対策 |
| 4 | パフォーマンス |
| 5 | セキュリティ |

### Phase 4: 統合レポート + AI推薦テスト
→ 「次に書くべき記事 TOP 5」を提案

## 注意
- 読み取り専用（コードの変更を行わない）
- 全提案にデータの根拠を付ける
```

### `/content` — 作る

```markdown
# コンテンツ制作

5段階パイプラインでコンテンツを制作する。

---

## 手順

**まず `docs/guide-flow/` 以下のドキュメントを読み込むこと。**

1. `docs/guide-flow/AGENT-CONFIG.md` を読む
2. 以下の5段階パイプラインを順に実行する:

| 工程 | ガイド | ユーザー承認 |
|------|--------|-------------|
| 1. リサーチ | `AGENT-GUIDE-1-research.md` | 不要 |
| 2. 構成設計 | `AGENT-GUIDE-2-content-design.md` | **必要** |
| 3. 執筆 | `AGENT-GUIDE-3-writing.md` | **必要** |
| 4. 実装 | `AGENT-GUIDE-4-implementation.md` | 不要 |
| 5. QA | `AGENT-GUIDE-5-qa.md` | 不要 |

## 更新するファイル
（AGENT-CONFIG.md の「データ登録」セクション参照）
```

### `/index` — 届ける

```markdown
# インデックス登録

作ったコンテンツをGoogleに届ける。

---

## コマンド

# URL登録（20件/日）
python scripts/request-indexing.py --config config.json

# サイトマップ送信（デプロイ後に実行）
python scripts/request-indexing.py --config config.json --sitemap

# 進捗確認
python scripts/request-indexing.py --config config.json --status
```

### ポイント

1. **コマンドファイル自体にはロジックを書かない。** ガイドファイルへの参照で構成する
2. **`/audit` が最も重要。** ここでデータに基づいて「何を作るか」を決めるから、`/content` の品質が決まる
3. **サイクルを回す。** `/audit` → `/content` → `/index` → （計測）→ `/audit` → ...

---

## Step 4: CLAUDE.md にコマンド一覧を追記する

```markdown
## 運用コマンド

| コマンド | 用途 |
|---------|------|
| `/audit` | 何を作るべきか判断する（戦略＋技術＋計測） |
| `/content` | 5段階パイプラインでコンテンツ制作 |
| `/index` | インデックス登録＋サイトマップ送信 |

コマンド定義: `.claude/commands/`
```

---

## Claude Code を使わない場合

上記の構造はそのまま手動の運用手順書として機能する。

1. `docs/guide-flow/AGENT-CONFIG.md` をプロジェクトの設計書として使う
2. `AGENT-GUIDE-1〜5` を工程ごとのチェックリストとして使う
3. AI（ChatGPT、Claude等）に各ガイドを渡して工程ごとに実行させる

コマンド化は便利だが、本質はガイドとCONFIGの分離構造にある。

---

## コマンド化完了後のファイル構成

```
your-project/
├── CLAUDE.md                          ← コマンド一覧を追記
├── .claude/
│   └── commands/
│       ├── audit.md                   ← /audit（判断する）
│       ├── content.md                 ← /content（作る）
│       └── index.md                   ← /index（届ける）
├── docs/
│   └── guide-flow/
│       ├── AGENT-CONFIG.md            ← ★ プロジェクト固有設定（最重要）
│       ├── AGENT-GUIDE-1-research.md
│       ├── AGENT-GUIDE-2-content-design.md
│       ├── AGENT-GUIDE-3-writing.md
│       ├── AGENT-GUIDE-4-implementation.md
│       ├── AGENT-GUIDE-5-qa.md
│       └── anchors/                   ← Nanobananaアンカー画像
├── public/
│   ├── ai.txt                         ← 漆畑式4層 Layer 1
│   └── llms.txt                       ← 漆畑式4層 Layer 2
├── src/
│   └── lib/
│       └── structured-data.ts         ← 漆畑式4層 Layer 3
└── ...
```
