#!/usr/bin/env python3
"""
漆畑式LLMO — Search Console 月次レポート取得 / SC Monthly Report

Google Search Console API からSEOデータを取得し、
Markdown + JSON で出力する。

使い方:
  python fetch-search-console-report.py --config config.json [--month 2026-03] [--json]

config.json の例:
  {
    "search_console_site": "sc-domain:example.com",
    "credentials_path": "~/.config/google-cloud/service-account.json",
    "output_dir": "./reports/"
  }
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def get_client(credentials_path):
    creds = service_account.Credentials.from_service_account_file(
        os.path.expanduser(credentials_path), scopes=SCOPES
    )
    return build("searchconsole", "v1", credentials=creds)


def get_date_range(month_str):
    if month_str:
        year, month = map(int, month_str.split("-"))
    else:
        today = date.today()
        first_of_this_month = today.replace(day=1)
        last_of_prev_month = first_of_this_month - timedelta(days=1)
        year, month = last_of_prev_month.year, last_of_prev_month.month

    start = date(year, month, 1)
    end = date(year + (1 if month == 12 else 0),
               1 if month == 12 else month + 1, 1) - timedelta(days=1)
    return start.isoformat(), end.isoformat()


def fetch_query_data(service, site_url, start_date, end_date, limit=100):
    """キーワード別パフォーマンス"""
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": limit,
    }
    result = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = []
    for row in result.get("rows", []):
        rows.append({
            "query": row["keys"][0],
            "clicks": row["clicks"],
            "impressions": row["impressions"],
            "ctr": round(row["ctr"] * 100, 1),
            "position": round(row["position"], 1),
        })
    return rows


def fetch_page_data(service, site_url, start_date, end_date, limit=50):
    """ページ別パフォーマンス"""
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": limit,
    }
    result = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = []
    for row in result.get("rows", []):
        rows.append({
            "page": row["keys"][0],
            "clicks": row["clicks"],
            "impressions": row["impressions"],
            "ctr": round(row["ctr"] * 100, 1),
            "position": round(row["position"], 1),
        })
    return rows


def fetch_device_data(service, site_url, start_date, end_date):
    """デバイス別パフォーマンス"""
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["device"],
    }
    result = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = []
    for row in result.get("rows", []):
        rows.append({
            "device": row["keys"][0],
            "clicks": row["clicks"],
            "impressions": row["impressions"],
            "ctr": round(row["ctr"] * 100, 1),
            "position": round(row["position"], 1),
        })
    return rows


def generate_markdown(start_date, end_date, data):
    lines = [
        f"# Search Console 月次レポート: {start_date[:7]}",
        f"\n期間: {start_date} 〜 {end_date}\n",
    ]

    if data.get("queries"):
        lines.append("## キーワード TOP 30\n")
        lines.append("| キーワード | クリック | 表示 | CTR | 順位 |")
        lines.append("|-----------|---------|------|-----|------|")
        for q in data["queries"][:30]:
            lines.append(f"| {q['query']} | {q['clicks']} | {q['impressions']} | "
                         f"{q['ctr']}% | {q['position']} |")

    if data.get("pages"):
        lines.append("\n## ページ TOP 20\n")
        lines.append("| ページ | クリック | 表示 | CTR | 順位 |")
        lines.append("|--------|---------|------|-----|------|")
        for p in data["pages"][:20]:
            lines.append(f"| {p['page']} | {p['clicks']} | {p['impressions']} | "
                         f"{p['ctr']}% | {p['position']} |")

    if data.get("devices"):
        lines.append("\n## デバイス別\n")
        lines.append("| デバイス | クリック | 表示 | CTR | 順位 |")
        lines.append("|---------|---------|------|-----|------|")
        for d in data["devices"]:
            lines.append(f"| {d['device']} | {d['clicks']} | {d['impressions']} | "
                         f"{d['ctr']}% | {d['position']} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search Console月次レポート取得")
    parser.add_argument("--config", required=True, help="設定ファイル")
    parser.add_argument("--month", help="対象月（YYYY-MM）。省略時は前月")
    parser.add_argument("--json", action="store_true", help="JSON生データも出力")
    args = parser.parse_args()

    config = load_config(args.config)
    start_date, end_date = get_date_range(args.month)
    month_str = start_date[:7]
    output_dir = Path(config.get("output_dir", "."))
    output_dir.mkdir(parents=True, exist_ok=True)

    site_url = config["search_console_site"]
    service = get_client(config["credentials_path"])
    print(f"データ取得中: {month_str} ({site_url})")

    data = {
        "queries": fetch_query_data(service, site_url, start_date, end_date),
        "pages": fetch_page_data(service, site_url, start_date, end_date),
        "devices": fetch_device_data(service, site_url, start_date, end_date),
    }

    md = generate_markdown(start_date, end_date, data)
    md_path = output_dir / f"{month_str}-search-console-report.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"レポート: {md_path}")

    if args.json:
        json_path = output_dir / f"{month_str}-search-console-data.json"
        json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSONデータ: {json_path}")


if __name__ == "__main__":
    main()
