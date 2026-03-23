"""
Nanobanana — AI Image Generator

Google Gemini の画像生成APIを使い、テキストプロンプトまたは参照画像から
スタイル統一された画像を自動生成する。

使い方:
  テキストのみ:
    python generate_image.py "プロンプト" --out output.png --ratio 3:2

  参照画像あり（スタイル統一）:
    python generate_image.py "プロンプト" --ref anchor.png --out output.png --ratio 3:2

  4K解像度:
    python generate_image.py "プロンプト" --4k --out output.png

オプション:
  --ref     : 参照画像（最大14枚）。スタイル統一のアンカーとして使用
  --out     : 出力ファイル名
  --ratio   : アスペクト比（1:1, 16:9, 9:16, 3:2, 4:3 等）
  --4k      : 4K解像度で生成

セットアップ:
  1. Google AI Studio で Gemini API キーを取得
  2. .env ファイルに GOOGLE_API_KEY=your-key を設定
  3. pip install google-genai python-dotenv Pillow
"""

import os
import sys
import io
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


def generate_image(prompt, output_filename=None, aspect_ratio="1:1", use_4k=False):
    """テキストプロンプトから画像を生成する

    Args:
        prompt: 画像生成プロンプト
        output_filename: 出力ファイル名（省略時はタイムスタンプ）
        aspect_ratio: アスペクト比
        use_4k: 4K解像度を使用するか
    """

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("エラー: GOOGLE_API_KEY が設定されていません。")
        print(".env ファイルに GOOGLE_API_KEY=your-key を設定してください。")
        return None

    client = genai.Client(api_key=api_key)

    print(f"プロンプト: {prompt[:100]}...")
    print(f"アスペクト比: {aspect_ratio}")
    if use_4k:
        print("解像度: 4K")
    print("生成中...")

    image_config_params = {"aspect_ratio": aspect_ratio}
    if use_4k:
        image_config_params["image_size"] = "4K"

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(**image_config_params),
        ),
    )

    return _save_response_image(response, output_filename)


def generate_with_reference(prompt, reference_images, output_filename=None,
                            aspect_ratio="1:1", use_4k=False):
    """参照画像を使ってスタイル統一された画像を生成する

    アンカー画像方式: 1枚の基準画像を参照することで、
    全ての生成画像のスタイル（色調・タッチ・雰囲気）を統一する。

    Args:
        prompt: 画像生成プロンプト
        reference_images: 参照画像のファイルパスリスト（最大14枚）
        output_filename: 出力ファイル名
        aspect_ratio: アスペクト比
        use_4k: 4K解像度を使用するか
    """

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("エラー: GOOGLE_API_KEY が設定されていません。")
        return None

    client = genai.Client(api_key=api_key)

    # 参照画像を読み込み（最大14枚）
    images = []
    for ref in reference_images[:14]:
        if isinstance(ref, str):
            if not os.path.exists(ref):
                print(f"エラー: 参照画像 '{ref}' が見つかりません。")
                return None
            images.append(Image.open(ref))
        else:
            images.append(ref)

    print(f"プロンプト: {prompt[:100]}...")
    print(f"参照画像: {len(images)}枚")
    print(f"アスペクト比: {aspect_ratio}")
    if use_4k:
        print("解像度: 4K")
    print("生成中...")

    contents = [prompt] + images

    image_config_params = {"aspect_ratio": aspect_ratio}
    if use_4k:
        image_config_params["image_size"] = "4K"

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(**image_config_params),
        ),
    )

    return _save_response_image(response, output_filename)


def _save_response_image(response, output_filename):
    """APIレスポンスから画像を取得・保存する"""
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data is not None:
            image_data = part.inline_data.data

            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"generated_{timestamp}.png"
            elif not output_filename.endswith(".png"):
                output_filename += ".png"

            image = Image.open(io.BytesIO(image_data))
            image.save(output_filename)
            print(f"保存しました: {output_filename}")
            return output_filename

    print("画像の生成に失敗しました")
    return None


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    prompt = sys.argv[1]
    use_4k = "--4k" in sys.argv

    if "--ref" in sys.argv:
        ref_index = sys.argv.index("--ref")
        reference_images = []
        for i in range(ref_index + 1, len(sys.argv)):
            arg = sys.argv[i]
            if arg.startswith("--"):
                break
            reference_images.append(arg)

        output = None
        if "--out" in sys.argv:
            out_index = sys.argv.index("--out")
            if out_index + 1 < len(sys.argv):
                output = sys.argv[out_index + 1]

        ratio = "1:1"
        if "--ratio" in sys.argv:
            ratio_index = sys.argv.index("--ratio")
            if ratio_index + 1 < len(sys.argv):
                ratio = sys.argv[ratio_index + 1]

        generate_with_reference(prompt, reference_images, output, ratio, use_4k)
    else:
        output = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
        ratio = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else "1:1"

        generate_image(prompt, output, ratio, use_4k)
