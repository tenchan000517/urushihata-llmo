#!/usr/bin/env python3
"""
漆畑式LLMO — インデックス登録自動化 / Indexing Automation

Google Indexing API でURLのインデックス登録を自動リクエストする。

仕組み:
  1. sitemap.xml からURL一覧を自動取得（ページ追加時に手動更新不要）
  2. 送信済み/除外URLは .indexing-progress.json で管理
  3. 1日20件上限で優先度順に送信

使い方:
  python request-indexing.py --config config.json           # URL送信
  python request-indexing.py --config config.json --status   # 進捗確認
  python request-indexing.py --config config.json --dry-run  # テスト
  python request-indexing.py --config config.json --sitemap  # サイトマップ送信
  python request-indexing.py --config config.json --limit 10 # 上限変更

config.json の例:
  {
    "site_url": "sc-domain:example.com",
    "sitemap_url": "https://example.com/sitemap.xml",
    "credentials_path": "~/.config/google-cloud/service-account.json",
    "exclude_patterns": ["/contact", "/terms", "/privacy"],
    "priority_patterns": [
      "^https://example\\\\.com/?$",
      "/services",
      "/blog/?$",
      "/blog/"
    ]
  }

セットアップ:
  1. Google Cloud Console で Indexing API + Search Console API を有効化
  2. サービスアカウントを作成し、JSON鍵をダウンロード
  3. Search Console でサービスアカウントを「オーナー」として追加
  4. config.json を作成
"""

import json
import os
import re
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

from google.oauth2 import service_account
from googleapiclient.discovery import build

DAILY_LIMIT = 20


def load_config(config_path):
    """設定ファイルを読み込む"""
    with open(config_path) as f:
        return json.load(f)


def fetch_sitemap_urls(sitemap_url):
    """sitemap.xml からURL一覧を取得"""
    try:
        with urlopen(sitemap_url, timeout=10) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]
        return urls
    except (URLError, ET.ParseError) as e:
        print(f"sitemap.xml 取得エラー: {e}")
        return []


def get_priority(url, priority_patterns):
    """URLの優先度を返す（小さいほど高優先）"""
    for i, pattern in enumerate(priority_patterns):
        if re.search(pattern, url):
            return i
    return len(priority_patterns)


def is_excluded(url, exclude_patterns):
    """除外対象かどうか"""
    return any(p in url for p in exclude_patterns)


def submit_sitemap(config):
    """サイトマップをSearch Consoleに送信"""
    creds_path = os.path.expanduser(config["credentials_path"])
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=["https://www.googleapis.com/auth/webmasters"]
    )
    service = build("searchconsole", "v1", credentials=creds)

    sitemap_url = config["sitemap_url"]
    site_url = config["site_url"]

    try:
        service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        print(f"サイトマップ送信完了: {sitemap_url}")
    except Exception as e:
        print(f"サイトマップ送信エラー: {e}")
        return

    try:
        result = service.sitemaps().get(siteUrl=site_url, feedpath=sitemap_url).execute()
        print(f"\n=== サイトマップステータス ===")
        print(f"URL:        {result.get('path', 'N/A')}")
        print(f"最終送信:   {result.get('lastSubmitted', 'N/A')}")
        contents = result.get("contents", [])
        for c in contents:
            print(f"  {c.get('type', '?')}: 送信{c.get('submitted', '?')}件 / "
                  f"インデックス済み{c.get('indexed', '?')}件")
    except Exception as e:
        print(f"ステータス取得エラー: {e}")


def load_progress(progress_file):
    if progress_file.exists():
        with open(progress_file) as f:
            return json.load(f)
    return {"submitted": {}, "skipped": {}, "daily_date": None, "daily_count": 0}


def save_progress(progress, progress_file):
    with open(progress_file, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="漆畑式LLMO インデックス登録自動化")
    parser.add_argument("--config", required=True, help="設定ファイル（config.json）")
    parser.add_argument("--status", action="store_true", help="進捗を表示")
    parser.add_argument("--dry-run", action="store_true", help="テスト実行")
    parser.add_argument("--limit", type=int, default=DAILY_LIMIT, help=f"1日の上限")
    parser.add_argument("--reset", action="store_true", help="進捗をリセット")
    parser.add_argument("--sitemap", action="store_true", help="サイトマップ送信")
    args = parser.parse_args()

    config = load_config(args.config)
    progress_file = Path(args.config).parent / ".indexing-progress.json"
    progress = load_progress(progress_file)

    if args.reset:
        save_progress({"submitted": {}, "skipped": {}, "daily_date": None, "daily_count": 0},
                      progress_file)
        print("進捗をリセットしました。")
        return

    if args.sitemap:
        submit_sitemap(config)
        return

    # sitemap.xml からURL取得
    print("sitemap.xml を取得中...")
    all_urls = fetch_sitemap_urls(config["sitemap_url"])
    if not all_urls:
        print("URLが取得できませんでした。")
        return

    exclude = config.get("exclude_patterns", [])
    priority = config.get("priority_patterns", [])

    all_urls = [u for u in all_urls if not is_excluded(u, exclude)]
    all_urls.sort(key=lambda u: get_priority(u, priority))

    done_urls = set(progress.get("submitted", {}).keys()) | set(progress.get("skipped", {}).keys())
    pending = [u for u in all_urls if u not in done_urls]

    if args.status:
        submitted = len(progress.get("submitted", {}))
        skipped = len(progress.get("skipped", {}))
        print(f"\nsitemap上のURL:  {len(all_urls)}件")
        print(f"API送信済み:     {submitted}件")
        print(f"スキップ済み:    {skipped}件")
        print(f"残り:            {len(pending)}件")
        if pending:
            days = (len(pending) + args.limit - 1) // args.limit
            print(f"完了見込み:     あと{days}日（1日{args.limit}件）")
            print(f"\n次に送信するURL（先頭5件）:")
            for u in pending[:5]:
                print(f"  {u}")
        return

    if not pending:
        print(f"全URL送信済み（{len(all_urls)}件）")
        return

    # 日次カウント
    today = date.today().isoformat()
    if progress.get("daily_date") != today:
        progress["daily_count"] = 0
        progress["daily_date"] = today

    remaining = args.limit - progress["daily_count"]
    if remaining <= 0 and not args.dry_run:
        print(f"本日の上限に達しています。明日再実行してください。")
        return

    # API初期化
    service = None
    if not args.dry_run:
        creds_path = os.path.expanduser(config["credentials_path"])
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=["https://www.googleapis.com/auth/indexing"]
        )
        service = build("indexing", "v3", credentials=creds)

    batch = pending[:remaining] if not args.dry_run else pending[:args.limit]
    sent = 0

    print(f"\n送信開始（最大{len(batch)}件 / 残り{len(pending)}件）\n")

    for url in batch:
        if args.dry_run:
            print(f"  [DRY] {url}")
            sent += 1
            continue

        try:
            service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            print(f"  OK {url}")
            progress.setdefault("submitted", {})[url] = datetime.now().isoformat()
            progress["daily_count"] += 1
            sent += 1
        except Exception as e:
            err = str(e)
            if "429" in err:
                print(f"\n  RATE LIMIT — 日次上限到達。明日再実行してください。")
                break
            elif "403" in err:
                print(f"  ERROR 403: Indexing APIが有効でないか、サービスアカウントがオーナーでない")
                break
            else:
                print(f"  ERROR: {url} — {e}")

    if not args.dry_run:
        save_progress(progress, progress_file)

    done_total = len(progress.get("submitted", {}))
    skip_total = len(progress.get("skipped", {}))
    new_pending = len(all_urls) - done_total - skip_total
    print(f"\n完了: 今回{sent}件 / API送信済み{done_total}件")
    if new_pending > 0:
        print(f"残り{new_pending}件")


if __name__ == "__main__":
    main()
