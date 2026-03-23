"""
Nanobanana — バッチ画像生成サンプル / Batch Image Generation Example

アンカー画像を参照しながら、複数の画像を統一スタイルで一括生成する。
自分のプロジェクトに合わせてIMAGES辞書を編集して使う。

使い方:
  python batch_example.py
"""

import os
import sys
import time

# generate_image.py から関数をインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_image import generate_with_reference

# ============================================================
# 設定 — プロジェクトに合わせて変更すること
# ============================================================

OUTPUT_DIR = "./output"          # 出力先ディレクトリ
ANCHOR = "./anchor.png"          # アンカー画像（スタイル基準）
SLEEP_SECONDS = 3                # API呼び出し間隔（レート制限対策）

# 共通スタイルプロンプト — 全画像に適用
STYLE = (
    "Modern flat illustration, no outlines, soft shadows, matte finish, "
    "warm and approachable style, 5.5-head proportion characters, "
    "clean white background, "
    "color palette: coral (#FF6B6B), warm green (#22C55E), soft orange (#FB923C), "
    "light teal (#2DD4BF), warm yellow (#FACC15), soft pink (#F9A8D4), "
    "minimal detail, geometric shapes, professional yet friendly, "
    "no text, no watermark, no border."
)


def p(scene):
    """スタイルプロンプト + シーンプロンプトを結合"""
    return STYLE + " " + scene


# ============================================================
# 画像定義 — ここを自分のプロジェクトに合わせて編集
# ============================================================

IMAGES = {
    # ファイル名: { prompt: "...", ratio: "..." }

    "eyecatch-getting-started": {
        "prompt": p(
            "A friendly guide character welcoming a newcomer. "
            "The guide holds a map and points forward. "
            "The newcomer looks curious and hopeful. "
            "Warm green tones, inviting atmosphere."
        ),
        "ratio": "3:2",
    },

    "eyecatch-best-practices": {
        "prompt": p(
            "Three workers collaborating around a table, "
            "each contributing a different colored puzzle piece. "
            "A lightbulb glows above the completed puzzle. "
            "Teamwork and achievement atmosphere."
        ),
        "ratio": "3:2",
    },

    "eyecatch-troubleshooting": {
        "prompt": p(
            "A person examining a tangled rope with a magnifying glass. "
            "They find the key knot and start to untangle it. "
            "A small sparkle appears where the solution is found. "
            "Problem-solving atmosphere, calm and methodical."
        ),
        "ratio": "3:2",
    },
}


# ============================================================
# 実行ロジック（基本的に変更不要）
# ============================================================

def generate_all():
    """全画像を一括生成"""
    if not os.path.exists(ANCHOR):
        print(f"エラー: アンカー画像が見つかりません: {ANCHOR}")
        print("先にアンカー画像を生成してください:")
        print(f'  python generate_image.py "{STYLE} A character standing..." --out {ANCHOR}')
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(IMAGES)
    print(f"アンカー画像: {ANCHOR}")
    print(f"生成対象: {total}枚")
    print(f"出力先: {OUTPUT_DIR}")
    print("=" * 60)

    generated = 0
    skipped = 0

    for i, (name, info) in enumerate(IMAGES.items(), 1):
        out_path = os.path.join(OUTPUT_DIR, f"{name}.png")

        if os.path.exists(out_path):
            print(f"[{i}/{total}] {name} は既に存在 — スキップ")
            skipped += 1
            continue

        print(f"\n[{i}/{total}] {name} を生成中...")

        try:
            result = generate_with_reference(
                info["prompt"],
                [ANCHOR],
                out_path,
                info.get("ratio", "3:2"),
            )
            if result:
                print(f"  -> OK: {out_path}")
                generated += 1
            else:
                print(f"  -> FAILED")
        except Exception as e:
            print(f"  -> ERROR: {e}")

        # レート制限対策
        if i < total:
            time.sleep(SLEEP_SECONDS)

    print("\n" + "=" * 60)
    print(f"完了! 生成: {generated}枚 / スキップ: {skipped}枚 / 合計: {total}枚")

    # 出力ディレクトリの内容を表示
    files = sorted(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png"))
    for f in files:
        print(f"  {f}")


if __name__ == "__main__":
    generate_all()
