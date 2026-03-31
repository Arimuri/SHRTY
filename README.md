# SHRTY

EYESY visual synth for macOS.
Based on [EYESY_OS](https://github.com/critterandguitari/EYESY_OS) by Critter & Guitari (BSD 3-Clause License).

## Setup

```bash
cd ITBS_EYESY
./run.sh
```

Initial setup creates a Python venv and installs dependencies automatically.
Requires Python 3.9+.

### Dependencies

- pygame
- sounddevice + numpy
- mido + python-rtmidi
- psutil

### Audio Input

SHRTYはシステムデフォルトのオーディオ入力（マイク / ライン入力）を使用します。
オーディオインターフェースの設定は環境によって異なるため、各自のセットアップに合わせて適宜設定してください。

DAWの再生音をSHRTYに送りたい場合は、ループバック機能やBlackHole等の仮想オーディオデバイスを活用すると便利です。

---

## Controls

### EYESY Buttons (Number Keys)

| Key | Function |
|-----|----------|
| 1 | OSD表示 (Shift+1 = メニュー) |
| 2 | Shift (押しながら他キー) |
| 3 | Auto Clear / Persist切替 |
| 4 | Mode prev |
| 5 | Mode next |
| 6 | Scene prev |
| 7 | Scene next |
| 8 | Scene保存 (長押し = 削除) |
| 9 | スクリーンショット |
| 0 | トリガー (押し続けるとシミュレート音声) |

### Shift + Keys

| Key | Function |
|-----|----------|
| Shift + 1 | メニュー |
| Shift + 4/5 | FGパレット prev/next |
| Shift + 6/7 | BGパレット prev/next |
| Shift + 8 | シーン更新 |
| Shift + 9 | ノブシーケンス再生/停止 |
| Shift + 0 | ノブシーケンス録音 |
| Shift + Knob1 (Q/A) | オーディオゲイン |

### Knobs

| Up | Down | Parameter |
|----|------|-----------|
| Q | A | Knob 1 |
| W | S | Knob 2 |
| E | D | Knob 3 |
| R | F | Knob 4 |
| T | G | Knob 5 |

### Dual Mode (SHRTY独自)

| Key | Function |
|-----|----------|
| TAB | Dual Mode ON/OFF |
| Z | Mode B prev |
| X | Mode B next |
| C | ブレンド切替 (Add / Multiply / Crossfade) |
| V | Mix: A寄り |
| B | Mix: B寄り |

2つのモードを同時実行し、ブレンドして表示する。
画面上部に緑バーでモード名・ブレンド方式・ミックス比率が表示される。

### MIDI Learn (SHRTY独自)

| Key | Function |
|-----|----------|
| M | MIDI Learn ON/OFF |
| LEFT / RIGHT | アサイン対象パラメータ選択 |
| MIDIノブを動かす | 選択中パラメータにCCをアサイン (自動で次へ進む) |
| M or ESC | 終了 |

画面下部に黄色バーで対象パラメータ・現在のCC番号が表示される。
アサインは `data/System/config.json` に自動保存。

アサイン可能パラメータ: Knob 1-5, Auto Clear, FG Palette, BG Palette, Mode

### 録画

| Key | Function |
|-----|----------|
| P | 録画 開始/停止 |

`data/Recordings/` にMP4で保存される。録画中は右上に赤い **REC** インジケーターが表示される。
ffmpegが必要（`brew install ffmpeg`）。

### その他

| Key | Function |
|-----|----------|
| ESC | 終了 (MIDI Learn中はLearn終了) |

---

## Modes

### 命名規則

- `S -` Scope: オーディオ波形リアクティブ
- `T -` Texture: テクスチャ・パターン生成
- `U -` Utility
- `ITBS -` オリジナルモード

### モード一覧 (ITBS)

#### ITBS - S - VHS Drift
ローファイVHS風。波形をRGB分離描画 + スキャンライン + フィルムグレイン。

| Knob | Parameter |
|------|-----------|
| 1 | スキャンライン強度 |
| 2 | RGB分離幅 (クロマチック収差) |
| 3 | グレイン量 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Block Glitch
ビートでブロック画面崩壊。オーディオバーを基盤に、ビート検出で画面の一部を切り取りずらして貼る。

| Knob | Parameter |
|------|-----------|
| 1 | グリッチ強度 |
| 2 | ブロックサイズ |
| 3 | 水平 ↔ 垂直バイアス |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Scanline Melt
走査線が音声で水平にずれ、画面が溶けたテレビのように歪む。

| Knob | Parameter |
|------|-----------|
| 1 | メルト量 |
| 2 | 速度 |
| 3 | 線の太さ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Torn Edge
破れた紙のような境界線が呼吸する空。青→シアン→淡色の境界を点描で描画。

| Knob | Parameter |
|------|-----------|
| 1 | 境界位置 |
| 2 | 荒さ |
| 3 | 粒子密度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Letter Scatter
「S H R T Y」がビートで四方に飛散し、ゴムバンドでホームに戻る。点線コネクション付き。

| Knob | Parameter |
|------|-----------|
| 1 | 飛散力 |
| 2 | 引き戻し強度 |
| 3 | 文字サイズ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - DVD Bounce
あのDVDスクリーンセーバーのパロディ。「DVD」ロゴが壁で跳ね返り、コーナーヒットで「CORNER!」フラッシュ。右上にヒットカウンター表示。

| Knob | Parameter |
|------|-----------|
| 1 | 速度 |
| 2 | ロゴサイズ |
| 3 | トレイルの長さ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Derpy Dog
オーディオに反応するアホ犬。音量で舌が伸び、体が揺れ、大音量で「BORK BORK!」と吠える。よだれ・吠えパーティクル付き。耳は物理演算でぶらぶら揺れる。

| Knob | Parameter |
|------|-----------|
| 1 | 犬のサイズ |
| 2 | 反応の感度 |
| 3 | 揺れの強さ |
| 4 | foreground color (よだれ・吠え) |
| 5 | background color |

#### ITBS - S - Screaming Face
オーディオレベルに応じて表情が変わる顔。静かなら「...」、大音量で口が開いて「AAAAA!」と叫ぶ。口の中に音声波形が見える。汗・叫びパーティクル付き。

| Knob | Parameter |
|------|-----------|
| 1 | 顔のサイズ |
| 2 | 反応の感度 |
| 3 | 揺れの強さ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Silly Matrix
マトリックス風の文字雨。コードではなくASCII記号が降ってくる。先頭文字は白く光り、トリガーで全文字がシャッフル＋フラッシュ。

| Knob | Parameter |
|------|-----------|
| 1 | 密度 |
| 2 | 文字サイズ |
| 3 | 残像の強さ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Neon Pulse
中心から放射状に伸びるネオンライン。各ラインの長さがオーディオ周波数帯に対応し、先端に白い光点。グロウレイヤー付き。

| Knob | Parameter |
|------|-----------|
| 1 | ライン本数 |
| 2 | ラインの太さ |
| 3 | 回転速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Laser Grid
シンセウェイブ風パースペクティブグリッド。消失点に向かう縦線と手前にスクロールする横線がオーディオで歪む。地平線上に太陽グロウ。

| Knob | Parameter |
|------|-----------|
| 1 | グリッド密度 |
| 2 | ワープ量 |
| 3 | スクロール速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Ribbon Dance
なめらかなリボンがオーディオ周波数帯に合わせて波打つ。複数のサイン波を重ね、グロウ＋白い芯線で描画。残像で軌跡が残る。

| Knob | Parameter |
|------|-----------|
| 1 | リボン本数 |
| 2 | 振幅 |
| 3 | なめらかさ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Wave Stack
波形を奥行き付きで積み重ね表示。各レイヤーがオーディオバッファの異なる帯域をサンプリングし、パララックス効果で奥の波はゆっくり動く。

| Knob | Parameter |
|------|-----------|
| 1 | 波の本数 |
| 2 | 振幅 |
| 3 | 間隔 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Strobe Cut
ビートで幾何学図形（矩形・三角・円・線）がフラッシュ＋回転しながら出現。ハイコントラストでストロボ的な演出。

| Knob | Parameter |
|------|-----------|
| 1 | 図形の数 |
| 2 | 最大サイズ |
| 3 | 回転速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Dancing Kaomoji
顔文字 `(^_^)` `\(^o^)/` `m(_ _)m` 等がトリガーで出現し、物理演算で跳ねて踊る。壁・床で反射。

| Knob | Parameter |
|------|-----------|
| 1 | 出現数 (1〜5個) |
| 2 | サイズ |
| 3 | 重力 (ふわふわ〜ずっしり) |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Emoji Party
ASCII顔文字が中心から全方向に爆発。トリガーごとにセット（happy / sad / crazy / cool / symbols）がランダム切替。オーディオで地面の顔文字が再び跳ねる。

| Knob | Parameter |
|------|-----------|
| 1 | 出現数 |
| 2 | サイズ |
| 3 | 重力 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Pop Rings
ビート検出で中心から同心円リングが拡大。ポップアートカラーでグロウ付き。リングの太さと速度は音量で変動。

| Knob | Parameter |
|------|-----------|
| 1 | リングの太さ |
| 2 | 拡大速度 |
| 3 | リング最大数 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Pixel Rain
レトロなドット絵風ピクセルが雨のように降る。各ピクセルの落下速度はオーディオ帯域に連動。ドロップシャドウ＋ハイライト付き。

| Knob | Parameter |
|------|-----------|
| 1 | ピクセルサイズ |
| 2 | 落下速度 |
| 3 | 密度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Bubble Pop
カラフルな泡が下から浮上し、ビートで弾ける。泡は半透明でハイライト付き。弾けるとリング状のポップアニメーション。

| Knob | Parameter |
|------|-----------|
| 1 | 泡のサイズ |
| 2 | 浮上速度 |
| 3 | 密度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Hex Grid
六角形グリッドの各セルがオーディオに反応してサイズ変動。セルごとにパレットから色を取得し、半透明で重なる。

| Knob | Parameter |
|------|-----------|
| 1 | 六角形サイズ |
| 2 | 間隔 |
| 3 | 反応度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Star Burst
ビートで中心から星型パーティクルが放射状に飛散。残像でカレイドスコープ的な軌跡パターンが生まれる。中心にグロウ。

| Knob | Parameter |
|------|-----------|
| 1 | 飛散力 |
| 2 | 星の数 |
| 3 | トレイルの長さ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Sine Prism
複数のサイン波をプリズムのように色分解して重ねる。各レイヤーが異なる位相・周波数で波打ち、グロウ＋白い光点で描画。残像で干渉模様が浮かぶ。

| Knob | Parameter |
|------|-----------|
| 1 | 波の本数 |
| 2 | 振幅 |
| 3 | 周波数 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Dot Grid Pulse
ミニマルなドットグリッドがオーディオで呼吸する。中心から波紋が広がり、各ドットの半径がオーディオ帯域に連動してリズミカルに膨縮。

| Knob | Parameter |
|------|-----------|
| 1 | グリッドサイズ |
| 2 | ドット最大半径 |
| 3 | 波紋の速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Iso Blocks
アイソメトリックブロックがビートで積み上がる。3面シェーディング＋白アウトライン。着地後もオーディオで微妙にバウンス。

| Knob | Parameter |
|------|-----------|
| 1 | ブロックサイズ |
| 2 | 列数 |
| 3 | 落下速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Candy Tiles
カラフルな角丸タイルがオーディオでスケールする。チェッカーボード風の配色で、音量が大きいタイルが明るくハイライト。

| Knob | Parameter |
|------|-----------|
| 1 | グリッドサイズ |
| 2 | 角丸の丸み |
| 3 | リアクション強度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Micro Waves
極小ドットで波形をプロットするポップなオシロスコープ。複数レイヤーの波形を散らし、音量が大きい箇所は白く光る。

| Knob | Parameter |
|------|-----------|
| 1 | ドットサイズ |
| 2 | 波形の数 |
| 3 | 散らし量 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - T - Confetti Machine
ビートでミニマルな幾何学コンフェティ（矩形・円・三角・ダイヤ）が舞い散る。回転＋フラッター物理演算付き。

| Knob | Parameter |
|------|-----------|
| 1 | パーティクル数 |
| 2 | サイズ |
| 3 | 重力 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Ring Pulse
波形データで同心円リングの半径が変わるミニマルなパルスリング。各リングがオーディオで有機的に変形し、残像で催眠的なパターンに。

| Knob | Parameter |
|------|-----------|
| 1 | リング数 |
| 2 | 太さ |
| 3 | 回転速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Dot Orbit
ドットが軌道上を周回。各軌道の半径がオーディオ帯域で脈動し、音量が大きいドットは白く光る。グロウ付き。

| Knob | Parameter |
|------|-----------|
| 1 | 軌道数 |
| 2 | ドット数/軌道 |
| 3 | 速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Pixel Scope
太ピクセルで波形を描画するレトロポップなオシロスコープ。中心から上下にバーが伸び、ミラーリフレクション付き。

| Knob | Parameter |
|------|-----------|
| 1 | ピクセルサイズ |
| 2 | 波形の高さ |
| 3 | ミラー量 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Mirror Sine
サイン波を四方にミラーリングして万華鏡的なシンメトリーを生成。残像で複雑な干渉パターンが浮かぶ。

| Knob | Parameter |
|------|-----------|
| 1 | 波の本数 |
| 2 | 振幅 |
| 3 | 速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Pluck String
弦楽器のように張られた線がオーディオ帯域で振動。各弦が異なる帯域に対応し、両端のブリッジで固定。エレガントで音楽的。

| Knob | Parameter |
|------|-----------|
| 1 | 弦の数 |
| 2 | テンション (振幅) |
| 3 | 減衰 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Spectrum Bars
スタイリッシュなスペクトラムバー。角丸＋グロウ＋リフレクション。スムージング付きで滑らかに動く。

| Knob | Parameter |
|------|-----------|
| 1 | バー数 |
| 2 | バー幅 |
| 3 | リフレクション量 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Arc Reactor
円弧が重なり合い、オーディオで弧の長さと半径が変化。端に白い光点。残像で多層的なパターン。

| Knob | Parameter |
|------|-----------|
| 1 | 弧の数 |
| 2 | 太さ |
| 3 | 回転速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Bounce Line
波形が上下のエッジで跳ね返り続ける弾性物理演算。残像でリボン状の軌跡が生まれる。

| Knob | Parameter |
|------|-----------|
| 1 | 線の数 |
| 2 | 弾力 |
| 3 | 残像 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Helix Spin
二重螺旋がオーディオで膨張・収縮しながら回転。横棒でDNA風。2色の螺旋＋グロウ。

| Knob | Parameter |
|------|-----------|
| 1 | 巻き数 |
| 2 | 半径 |
| 3 | 回転速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Waveform Grid
波形を行ごとに格子状に並べて面的に展開。各行で位相をずらし、うねりのあるオーディオサーフェスに。

| Knob | Parameter |
|------|-----------|
| 1 | 行数 |
| 2 | 振幅 |
| 3 | 位相ずれ |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Polar Flower
波形を極座標で描画し、花のようなパターンを生成。3レイヤー重ねでフィル＋アウトライン。

| Knob | Parameter |
|------|-----------|
| 1 | 花弁数 |
| 2 | 半径 |
| 3 | 回転速度 |
| 4 | foreground color |
| 5 | background color |

#### ITBS - S - Glitch Bars
水平バーが波形データで左右にずれるデジタルグリッチ。ビートで色反転＋スキャンラインノイズ。

| Knob | Parameter |
|------|-----------|
| 1 | バー数 |
| 2 | ずれ量 |
| 3 | ノイズ量 |
| 4 | foreground color |
| 5 | background color |

### 純正モード

Critter & Guitariの[EYESY_Modes_OSv3](https://github.com/critterandguitari/EYESY_Modes_OSv3)から108モード同梱。

---

## Persist (Auto Clear)

3キーでON/OFF。OFFにすると前フレームの描画が消えず重なっていく。フィードバック的な効果が得られる。

---

## ファイル構成

```
ITBS_EYESY/
  shrty.py          — メインエントリポイント
  sound_mac.py      — macOS音声入力 (sounddevice)
  midi_mac.py       — macOS MIDI入力 (python-rtmidi)
  eyesy.py          — EYESYエンジン (状態管理)
  osd.py            — OSD/メニュー描画
  run.sh            — 起動スクリプト
  data/
    Modes/          — ビジュアルモード
    Grabs/          — スクリーンショット保存先
    Scenes/         — シーン保存先
    System/         — config.json等
```

## モードの作り方

`data/Modes/ITBS - S - MyMode/main.py` を作成:

```python
import pygame

def setup(screen, etc):
    # 初回のみ呼ばれる
    pass

def draw(screen, etc):
    # 毎フレーム呼ばれる (30fps)
    w, h = screen.get_width(), screen.get_height()

    # etc.knob1 ~ etc.knob5: 0.0 ~ 1.0
    # etc.audio_in[0:99]: 音声バッファ (-32768 ~ 32767)
    # etc.audio_peak: ピーク値
    # etc.color_picker(t): パレットから色取得 (t: 0.0~1.0)
    # etc.color_picker_bg(t): 背景パレットから色取得
    # etc.trig: トリガー (True/False)
    # etc.midi_notes[0:127]: MIDIノート状態

    screen.fill((0, 0, 0))
    color = etc.color_picker(etc.knob4)
    # ... draw something ...
```

---

## License

EYESY engine: BSD 3-Clause License (Critter & Guitari)
ITBS modes: original
