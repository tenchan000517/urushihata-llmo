# 漆畑式LLMO — 運用ツール / Operations Tools

漆畑式LLMOの運用サイクルを支えるツール群。

```
設計 → 制作 → 登録 → 計測 → 監査 → 次の制作
         ↑                              │
         └──────────────────────────────┘
```

## ツール一覧

### インデックス登録 (`indexing/`)
Google Indexing API でURLのインデックス登録を自動化。
- sitemap.xml からURL一覧を自動取得
- 優先度に基づいた段階的送信（1日20件上限）
- 進捗管理（`.indexing-progress.json`）

→ [詳細](indexing/README.md)

### アナリティクス＆分析 (`analytics/`)
GA4 + Search Console のデータ取得と、ビジネスファネル起点の分析。
- GA4 Data API からトラフィック・AI流入・コンバージョンを取得
- Search Console API からKW順位・CTR・表示回数を取得
- 鳥→虫→魚の3視点分析フレームワーク

→ [詳細](analytics/README.md)

## セットアップ

### 前提条件
- Python 3.10+
- Google Cloud プロジェクト
- サービスアカウント（GA4 Data API + Search Console API + Indexing API）

### インストール
```bash
pip install google-analytics-data google-auth google-api-python-client
```

### 認証設定
1. Google Cloud Console でサービスアカウントを作成
2. JSON鍵をダウンロードし、安全な場所に配置
3. GA4プロパティ・Search Consoleにサービスアカウントのメールを閲覧者として追加
