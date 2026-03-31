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
