# インデックス登録自動化 / Indexing Automation

Google Indexing API を使ってURLのインデックス登録を自動化する。

## 仕組み

1. `sitemap.xml` からURL一覧を自動取得（ページ追加時に手動更新不要）
2. 優先度カテゴリに基づいて段階的に送信
3. 1日20件上限（Google API制限）
4. 送信済みURLは `.indexing-progress.json` で管理

## 使い方

```bash
# 日次のURL登録（20件ずつ、未登録を優先）
python request-indexing.py --config config.json

# サイトマップ送信（デプロイ後に実行）
python request-indexing.py --config config.json --sitemap

# 進捗確認
python request-indexing.py --config config.json --status

# テスト実行（APIは叩かない）
python request-indexing.py --config config.json --dry-run

# 上限変更
python request-indexing.py --config config.json --limit 10
```

## 設定ファイル（config.json）

```json
{
  "site_url": "sc-domain:example.com",
  "sitemap_url": "https://example.com/sitemap.xml",
  "credentials_path": "~/.config/google-cloud/service-account.json",
  "exclude_patterns": ["/contact", "/terms", "/privacy"],
  "priority_categories": [
    {"name": "Top & Service Pages", "patterns": ["/", "/about", "/services"]},
    {"name": "Content Hub Pages", "patterns": ["/blog", "/guides"]},
    {"name": "Individual Content", "patterns": ["/blog/*", "/guides/*"]},
    {"name": "Regional Pages", "patterns": ["/regions/*"]}
  ]
}
```

## セットアップ

1. Google Cloud Console で Indexing API を有効化
2. サービスアカウントを作成し、JSON鍵をダウンロード
3. Search Console でサービスアカウントのメールを所有者として追加
4. `config.json` を作成して設定を記入
