# 漆畑式LLMO Technical Audit — Agent 4: パフォーマンス・技術監査ガイド

## 調査対象
- next.config の最適化設定（画像、圧縮、バンドル）
- Image コンポーネントの使用状況（fill + sizes）
- フォント最適化
- サードパーティスクリプトの読み込み方法
- CSS の最適化状態
- コード分割の使用状況
- RSC / Client コンポーネントの比率と妥当性

## next.config 確認項目
- 画像最適化（formats, cache TTL, remotePatterns）
- 圧縮設定（compress）
- バンドル最適化（chunk splitting）
- poweredByHeader
- polyfill除去

## Image fill+sizes 監査（誤検知防止・最重要）

### 禁止事項
- 一部のファイルだけを調べて「合計N箇所」と概算すること
- 単一行 grep だけで fill+sizes の有無を判定すること

### JSX multiline props の注意
JSXでは `fill` と `sizes` が別の行に書かれることが多い:
```tsx
<Image
  src={...}
  fill                    ← この行だけ見ると sizes がないように見える
  sizes="(max-width: 768px) 100vw, 33vw"   ← 次の行にある
  className="object-cover"
/>
```

### 必須手順 — 全数調査

#### Phase 1: fill を含むファイルの特定
```
grep -rn "fill" src/ --include="*.tsx"
```
この結果から:
- SVG の `fill` 属性（`fill="currentColor"`, `fill="none"` 等）を除外
- CSS の `fill` プロパティ（`className="fill-current"` 等）を除外
- next/image の Image コンポーネントで `fill` を prop として使っているファイルのみ抽出

#### Phase 2: 各ファイルの sizes 有無確認
各ファイルについて:
1. `fill` がある Image コンポーネントの前後5行を READ する
2. 同じ Image コンポーネント内に `sizes` prop があるか確認
3. ない場合は「fill without sizes」としてリストに追加

#### Phase 3: .map() 内の処理
`.map()` 内の Image は1つのコード箇所だが、複数回レンダーされる。
- コード箇所数: 1
- レンダー数: 配列の要素数
→ 両方を報告する（例: 「1箇所（3アイテムの.mapで3回レンダー）」）

#### Phase 4: 漏れやすいディレクトリの確認
以下は特に注意して確認すること:
- src/components/

### 出力: fill+sizes の正確なリスト
各エントリに以下を含める:
- ファイルパス
- 行番号
- Image の src（特定用）
- 親コンテナのレイアウト（grid-cols-N 等）
- 推奨 sizes 値

## RSC / Client コンポーネント比率監査（重要・新規）

### 目的
不要な `'use client'` がパフォーマンスを劣化させていないかを確認する。
AIクローラーの中にはJSを実行しないものがあり、RSCの活用度はLLMOにも影響する。

### 手順
1. `grep -rl "'use client'" src/app/` で Client コンポーネントの全数を取得
2. `glob` で `src/app/**/*.tsx` の全ファイル数を取得
3. Client 比率 = Client 数 / 全 tsx 数

### 不要な 'use client' の検出
各 Client コンポーネントについて:
1. `useState`, `useEffect`, `useRef`, `useCallback`, `useContext` のimport有無
2. `onClick`, `onChange`, `onSubmit` 等のイベントハンドラ有無
3. `window`, `document`, `localStorage` 等のブラウザAPI使用有無
4. 上記がいずれもない場合 → **不要な 'use client'** として報告

### 特に確認すべきディレクトリ

### 評価基準
- Client 比率 5% 以下: ✅ 良好
- Client 比率 5-15%: ⚠️ 確認推奨
- Client 比率 15% 以上: ❌ 調査必須
- 不要な 'use client' が1件でもある: ⚠️ 報告

## パフォーマンス監査の正確性ルール

### next/dynamic
- `grep` で `next/dynamic` や `dynamic(` を検索
- page.tsx だけでなくクライアントコンポーネント（*Client.tsx 等）も検索対象
- 「未使用」と判定する前に実際のインポート箇所を確認

### raw `<img>`
- next/image の代わりに `<img>` を使っている箇所を報告
- 外部URL表示やユーザー入力画像など正当な理由がある場合はその旨も併記
- OG画像生成ルート（api/og/route.tsx）内の `<img>` は Satori 用なので除外

## フォント最適化チェック
- next/font の使用有無
- display: 'swap' の設定
- preload 設定
- fallback フォント

## サードパーティスクリプト
- Google Analytics の読み込み方法（defer / async / 遅延読み込み）
- Microsoft Clarity の読み込み方法
- その他のサードパーティスクリプト

## コード分割
- `next/dynamic` の使用箇所
- `React.lazy` の使用箇所

## 出力フォーマット
- next.config 設定サマリー
- fill+sizes: 問題箇所数（正確な全数）と詳細リスト
- RSC/Client 比率: Client X件 / 全体Y件 (Z%)
  - 不要な 'use client' 一覧（あれば）
- フォント最適化状況
- スクリプト読み込み状況
- コード分割使用状況
- raw `<img>` 使用箇所
- 改善推奨事項（ファイルパス・行番号付き）
- スコア: X/10
