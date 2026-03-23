# アナリティクス＆分析 / Analytics & Analysis

GA4 Data API + Search Console API からデータを取得し、ビジネスファネル起点の分析を行う。

## フロー

### Phase 1: データ取得

```bash
# GA4レポート取得
python fetch-ga4-report.py --config config.json --month 2026-03

# Search Consoleレポート取得
python fetch-search-console-report.py --config config.json --month 2026-03
```

出力:
- `YYYY-MM-ga4-report.md` — Markdownレポート
- `YYYY-MM-ga4-data.json` — 生データ（二次分析用）
- `YYYY-MM-search-console-report.md`
- `YYYY-MM-search-console-data.json`

### Phase 2: 分析

[`analysis-framework.md`](analysis-framework.md) に従って分析を実行。

```
1. ビジネスファネル分析 → ボトルネック特定
2. 鳥の目 → 全体構造診断
3. 虫の目 → ボトルネックの原因パターン深掘り
4. 魚の目 → 時流・季節性・新兆候
5. ACTION決定 → ファネル詰まりに直結するもの3個以下
```

### Phase 3: 前月比較（2回目以降）

前月のJSONデータが存在する場合:
- ファネル各段階の前月比を算出
- 前月ACTIONの効果を検証
- KW順位の変動を確認

## 設定ファイル（config.json）

```json
{
  "ga4_property_id": "123456789",
  "search_console_site": "sc-domain:example.com",
  "credentials_path": "~/.config/google-cloud/service-account.json",
  "output_dir": "./reports/",
  "content_filter_path": "/blog/",
  "conversion_event": "form_submit"
}
```

## サイト設定テンプレート

[`site-config.example.md`](site-config.example.md) を複製して、自社サイトのファネル定義・ターゲット区分・狙いKW等を定義する。分析フレームワークはこの設定に基づいて分析を行う。

## セットアップ

1. Google Cloud Console で GA4 Data API と Search Console API を有効化
2. サービスアカウントを作成し、JSON鍵をダウンロード
3. GA4プロパティにサービスアカウントを閲覧者として追加
4. Search Console にサービスアカウントを追加
5. `config.json` を作成
