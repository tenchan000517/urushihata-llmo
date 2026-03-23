# Nanobanana — AI アイキャッチ画像自動生成 / AI Eyecatch Image Generator

**コンテンツ量産のボトルネックは画像。** 記事を書けても、毎回アイキャッチを手作りしていたらスケールしない。

Nanobanana は Google Gemini の画像生成APIを使い、**アンカー画像1枚からスタイルを統一した画像を自動生成**するシステム。

## なぜこれが必要か

```
漆畑式LLMO パイプライン:

Research → Design → Writing → Implementation → QA
                                    ↑
                              ここで画像が必要
                              手動だとボトルネック
                              Nanobananaで自動化
```

1,300ページのサイトで画像を手作りするのは不可能。Nanobananaがあるから「量より質のコンテンツが、量ある」が成立する。

## コンセプト: アンカー画像方式

1. **アンカー画像**を1枚生成する（スタイルの基準になる画像）
2. 以降の全画像は**アンカーを参照して生成**する
3. → 色調・タッチ・雰囲気が自動的に統一される

```
anchor.png（基準）
    ↓ 参照
    ├── article-1.png（統一されたスタイル）
    ├── article-2.png（統一されたスタイル）
    ├── article-3.png（統一されたスタイル）
    └── ...（何枚でも）
```

## ファイル構成

| ファイル | 用途 |
|---------|------|
| `generate_image.py` | 画像生成コアモジュール（テキスト→画像 / 参照画像→画像） |
| `batch_example.py` | バッチ生成のサンプルスクリプト |
| `requirements.txt` | 依存パッケージ |

## セットアップ

### 1. Google AI Studio でAPIキーを取得
- https://aistudio.google.com/apikey
- Gemini API キーを取得

### 2. 環境変数を設定
```bash
# .env ファイルを作成
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

**⚠️ .env ファイルは絶対にgitにコミットしないこと。.gitignoreに含めること。**

### 3. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

## 使い方

### 基本: テキストから画像生成

```bash
python generate_image.py "A cute cat sitting on a desk" --out cat.png --ratio 3:2
```

### 参照画像を使った統一スタイル生成

```bash
# 1. アンカー画像を生成
python generate_image.py "Modern flat illustration, warm colors, a friendly office scene" --out anchor.png

# 2. アンカーを参照して統一スタイルで生成
python generate_image.py "Same style. A factory floor with workers" --ref anchor.png --out factory.png --ratio 3:2
```

### バッチ生成（大量画像の一括生成）

```python
# batch_example.py を参考に、自分のプロジェクト用バッチスクリプトを作成
python batch_example.py
```

## スタイルプロンプトのテンプレート

### フラットイラスト（ビジネス系サイト向け）

```python
STYLE = (
    "Modern flat illustration, no outlines, soft shadows, matte finish, "
    "warm and approachable style, 5.5-head proportion characters, "
    "clean white background, "
    "color palette: coral (#FF6B6B), warm green (#22C55E), soft orange (#FB923C), "
    "light teal (#2DD4BF), warm yellow (#FACC15), soft pink (#F9A8D4), "
    "minimal detail, geometric shapes, professional yet friendly, "
    "no text, no watermark, no border."
)
```

### 写真風（リアル系サイト向け）

```python
STYLE = (
    "Professional photograph, natural lighting, shallow depth of field, "
    "clean composition, modern office environment, "
    "no text overlay, no watermark."
)
```

### アニメ風（若者向けサイト向け）

```python
STYLE = (
    "Anime-style illustration, vibrant colors, detailed background, "
    "clean linework, expressive characters, "
    "no text, no watermark."
)
```

## 対応アスペクト比

| 比率 | 用途 |
|------|------|
| `1:1` | SNSアイコン、サムネイル |
| `3:2` | ブログアイキャッチ（推奨） |
| `16:9` | ヒーロー画像、OG画像 |
| `9:16` | ストーリーズ、縦長バナー |
| `4:3` | プレゼン資料 |

## パイプラインとの統合

`pipeline/guide-4-implementation.md` の実装工程で、Nanobanana を使って画像を生成する:

1. トラック CONFIG で定義されたスタイルプロンプトを確認
2. プロジェクトのアンカー画像を参照に指定
3. 記事テーマに合ったシーンプロンプトを作成
4. 生成 → 確認 → 画像ホスティングにアップロード

## 注意事項

- **APIキーは絶対に公開しない** — `.env` ファイルは `.gitignore` に含める
- **API利用制限** — Gemini API には日次/分次のレート制限がある。バッチ生成時は `time.sleep(3)` 等で間隔を空ける
- **生成品質** — プロンプトの質が画像の質を決める。STYLEプロンプトを練り込むこと
- **アンカー画像の選定** — 最初のアンカーが全体のスタイルを決める。納得いくまで試行する
