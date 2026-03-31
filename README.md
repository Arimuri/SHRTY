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

SHRTY uses the system default audio input (mic / line-in).

**Babyface Pro**: TotalMix FXでLoopbackをONにすれば、DAWの再生音をそのままSHRTYに送れる。

**BlackHole**: `brew install blackhole-2ch` でインストール後、Audio MIDI設定で「複数出力装置」を作成し、システム出力に設定。SHRTYの入力にBlackHoleを使用。

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

#### ITBS - S - DVD Bounce / Derpy Dog / Screaming Face / Silly Matrix
#### ITBS - T - Dancing Kaomoji / Emoji Party

オリジナルモード。

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
