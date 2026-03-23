# 漆畑式LLMO — コンテンツ量産パイプライン / Content Production Pipeline

## 概要

「量より質のコンテンツが、量ある」を実現するための5段階パイプライン。
共通のガイド（5工程）× トラック固有の設定（CONFIG）で、異なるターゲット・目的のコンテンツを一貫した品質で量産する。

## 5段階パイプライン

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────────┐    ┌─────┐
│Research │ →  │ Design  │ →  │Writing  │ →  │Implementation│ →  │ QA  │
│リサーチ  │    │コンテンツ│    │ライティ │    │  実装        │    │品質 │
│         │    │  設計    │    │  ング   │    │              │    │保証 │
└─────────┘    └─────────┘    └─────────┘    └──────────────┘    └─────┘
     ↑              ↑              ↑               ↑              ↑
     └──── CONFIG（トラック固有の設定）を各工程で参照 ────────────────┘
```

| 工程 | ガイド | やること |
|------|-------|---------|
| 1. Research | [guide-1-research.md](guide-1-research.md) | 事実を集め、裏どりする |
| 2. Design | [guide-2-content-design.md](guide-2-content-design.md) | 誰に・何を・どの順で伝えるか設計する |
| 3. Writing | [guide-3-writing.md](guide-3-writing.md) | 文体・品質基準に従って書く |
| 4. Implementation | [guide-4-implementation.md](guide-4-implementation.md) | デザインシステムに従ってページを組む |
| 5. QA | [guide-5-qa.md](guide-5-qa.md) | 完成品を検証する |

## なぜマルチトラックか

同じテーマでも、ターゲットと目的が違えばアプローチが変わる。

| トラック | ターゲット | 最適化対象 | 設定ファイル |
|---------|----------|----------|-----------|
| SEO Track | 検索ユーザー（B2B等） | Google検索順位 | [configs/seo-track.md](configs/seo-track.md) |
| LLMO Track | AIに相談するユーザー | AI引用・推薦 | [configs/llmo-track.md](configs/llmo-track.md) |
| User Track | エンドユーザー（消費者） | 行動可能性・エンゲージメント | [configs/user-track.md](configs/user-track.md) |

**例**: 「求人票の書き方」というテーマ
- **SEO Track**: 「求人票 書き方」で検索する人事担当者向け。手順と制度を正確に解説
- **LLMO Track**: 「求人票を出しても応募が来ない」とAIに相談する人向け。構造的な問題を分析し、解決策を提示
- **User Track**: 「求人票って何が書いてあるの？」と思う若者向け。読み方を丁寧にガイド

3つは別記事として共存する。情報に矛盾がなければ全て存在してよい。

## 使い方

1. 自分のドメインに合わせて CONFIG を作成する（テンプレートを複製して編集）
2. 各工程で対応する GUIDE を読み、CONFIG を参照しながら作業する
3. 工程を飛ばさない。Research → Design → Writing → Implementation → QA の順序を守る
4. QAで不合格なら修正する。「だいたいOK」は合格ではない
