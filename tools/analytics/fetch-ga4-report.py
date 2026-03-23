#!/usr/bin/env python3
"""
漆畑式LLMO — GA4 月次レポート取得 / GA4 Monthly Report

Google Analytics 4 Data API からトラフィックデータを取得し、
Markdown + JSON で出力する。

使い方:
  python fetch-ga4-report.py --config config.json [--month 2026-03] [--json]

config.json の例:
  {
    "ga4_property_id": "123456789",
    "credentials_path": "~/.config/google-cloud/service-account.json",
    "output_dir": "./reports/",
    "content_filter_path": "/blog/",
    "conversion_event": "form_submit"
  }
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, FilterExpression, Filter,
    Metric, RunReportRequest, OrderBy,
)


def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)


def get_client(credentials_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser(credentials_path)
    return BetaAnalyticsDataClient()


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


def run_report(client, property_id, start_date, end_date, dimensions, metrics,
               limit=50, dimension_filter=None, order_by_metric=None, order_desc=True):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        limit=limit,
    )
    if dimension_filter:
        request.dimension_filter = dimension_filter
    if order_by_metric:
        request.order_bys = [OrderBy(
            metric=OrderBy.MetricOrderBy(metric_name=order_by_metric),
            desc=order_desc
        )]

    response = client.run_report(request)
    rows = []
    for row in response.rows:
        entry = {}
        for i, dim in enumerate(dimensions):
            entry[dim] = row.dimension_values[i].value
        for i, met in enumerate(metrics):
            entry[met] = row.metric_values[i].value
        rows.append(entry)
    return rows


def fetch_traffic_overview(client, config, start_date, end_date):
    return run_report(client, config["ga4_property_id"], start_date, end_date,
                      [], ["activeUsers", "sessions", "screenPageViews",
                           "averageSessionDuration", "bounceRate"])


def fetch_top_pages(client, config, start_date, end_date):
    return run_report(client, config["ga4_property_id"], start_date, end_date,
                      ["pagePath"], ["screenPageViews", "activeUsers"],
                      limit=30, order_by_metric="screenPageViews")


def fetch_traffic_sources(client, config, start_date, end_date):
    return run_report(client, config["ga4_property_id"], start_date, end_date,
                      ["sessionSource"], ["sessions", "activeUsers"],
                      limit=20, order_by_metric="sessions")


def fetch_ai_referrals(client, config, start_date, end_date):
    """AI関連の流入元を取得"""
    all_sources = run_report(client, config["ga4_property_id"], start_date, end_date,
                             ["sessionSource"], ["sessions"],
                             limit=100, order_by_metric="sessions")
    ai_keywords = ["chatgpt", "gemini", "perplexity", "claude", "copilot", "bing.com/chat"]
    return [s for s in all_sources
            if any(kw in s.get("sessionSource", "").lower() for kw in ai_keywords)]


def generate_markdown(config, start_date, end_date, data):
    lines = [
        f"# GA4 月次レポート: {start_date[:7]}",
        f"\n期間: {start_date} 〜 {end_date}\n",
    ]

    if data.get("overview"):
        lines.append("## トラフィック概要\n")
        ov = data["overview"][0] if data["overview"] else {}
        lines.append(f"| 指標 | 値 |")
        lines.append(f"|------|-----|")
        lines.append(f"| アクティブユーザー | {ov.get('activeUsers', 'N/A')} |")
        lines.append(f"| セッション | {ov.get('sessions', 'N/A')} |")
        lines.append(f"| ページビュー | {ov.get('screenPageViews', 'N/A')} |")

    if data.get("top_pages"):
        lines.append("\n## ページ別PV TOP 20\n")
        lines.append("| ページ | PV | ユーザー |")
        lines.append("|--------|-----|---------|")
        for p in data["top_pages"][:20]:
            lines.append(f"| {p.get('pagePath', '')} | {p.get('screenPageViews', '')} | "
                         f"{p.get('activeUsers', '')} |")

    if data.get("sources"):
        lines.append("\n## 流入元 TOP 10\n")
        lines.append("| ソース | セッション |")
        lines.append("|--------|-----------|")
        for s in data["sources"][:10]:
            lines.append(f"| {s.get('sessionSource', '')} | {s.get('sessions', '')} |")

    if data.get("ai_referrals"):
        lines.append("\n## AI流入\n")
        lines.append("| ソース | セッション |")
        lines.append("|--------|-----------|")
        for s in data["ai_referrals"]:
            lines.append(f"| {s.get('sessionSource', '')} | {s.get('sessions', '')} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="GA4月次レポート取得")
    parser.add_argument("--config", required=True, help="設定ファイル")
    parser.add_argument("--month", help="対象月（YYYY-MM）。省略時は前月")
    parser.add_argument("--json", action="store_true", help="JSON生データも出力")
    args = parser.parse_args()

    config = load_config(args.config)
    start_date, end_date = get_date_range(args.month)
    month_str = start_date[:7]
    output_dir = Path(config.get("output_dir", "."))
    output_dir.mkdir(parents=True, exist_ok=True)

    client = get_client(config["credentials_path"])
    print(f"データ取得中: {month_str}")

    data = {
        "overview": fetch_traffic_overview(client, config, start_date, end_date),
        "top_pages": fetch_top_pages(client, config, start_date, end_date),
        "sources": fetch_traffic_sources(client, config, start_date, end_date),
        "ai_referrals": fetch_ai_referrals(client, config, start_date, end_date),
    }

    # Markdown出力
    md = generate_markdown(config, start_date, end_date, data)
    md_path = output_dir / f"{month_str}-ga4-report.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"レポート: {md_path}")

    # JSON出力
    if args.json:
        json_path = output_dir / f"{month_str}-ga4-data.json"
        json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSONデータ: {json_path}")


if __name__ == "__main__":
    main()
