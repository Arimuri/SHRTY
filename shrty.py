#!/usr/bin/env python3
"""
SHRTY — EYESY visual synth for macOS
Based on EYESY_OS by Critter & Guitari (BSD 3-Clause License)
"""
import os
import sys
import time
import math
import traceback
import psutil
import pygame
from pygame.locals import *
from multiprocessing import Process, Array, Value, Lock
from ctypes import c_float

import eyesy as eyesy_mod
import sound_mac as sound
import midi_mac as midi
import osd
from screen_main_menu import ScreenMainMenu
from screen_test import ScreenTest
from screen_video_settings import ScreenVideoSettings
from screen_palette import ScreenPalette
from screen_wifi import ScreenWiFi
from screen_applogs import ScreenApplogs
from screen_midi_settings import ScreenMIDISettings
from screen_midi_pc_mapping import ScreenMIDIPCMapping

# --- Config ---
SHRTY_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SHRTY_DIR, "data")
WINDOW_SIZE = (1280, 720)

# --- Key mapping (keyboard → EYESY buttons) ---
# EYESY button functions:
#   1=OSD (shift+1=menu), 2=shift, 3=auto-clear toggle,
#   4=mode prev, 5=mode next, 6=scene prev, 7=scene next,
#   8=scene save, 9=screenshot, 10=trigger
KEY_MAPPING = {
    pygame.K_1: 1,   # OSD toggle (shift+1 = menu)
    pygame.K_2: 2,   # shift (hold)
    pygame.K_3: 3,   # auto-clear toggle
    pygame.K_4: 4,   # mode prev
    pygame.K_5: 5,   # mode next
    pygame.K_6: 6,   # scene prev
    pygame.K_7: 7,   # scene next
    pygame.K_8: 8,   # scene save (hold to delete)
    pygame.K_9: 9,   # screenshot
    pygame.K_0: 10,  # trigger (simulated sound)
}

# Knob control via Q/W/E/R/T and A/S/D/F/G
KNOB_KEYS_UP = {
    pygame.K_q: 0, pygame.K_w: 1, pygame.K_e: 2, pygame.K_r: 3, pygame.K_t: 4,
}
KNOB_KEYS_DOWN = {
    pygame.K_a: 0, pygame.K_s: 1, pygame.K_d: 2, pygame.K_f: 3, pygame.K_g: 4,
}
KNOB_STEP = 0.02

audio_process = None

def exitexit(code):
    global audio_process
    print("SHRTY: exiting...")
    pygame.display.quit()
    pygame.quit()
    if audio_process and audio_process.is_alive():
        audio_process.terminate()
        audio_process.join()
    midi.close()
    sys.exit(code)


# --- Dual mode blend ---
def blend_surfaces(surf_a, surf_b, blend_type, mix):
    """Composite two surfaces. blend_type: 0=add, 1=multiply, 2=crossfade"""
    if blend_type == 0:  # Additive
        result = surf_a.copy()
        surf_b_copy = surf_b.copy()
        surf_b_copy.set_alpha(int(mix * 255))
        result.blit(surf_b_copy, (0, 0), special_flags=pygame.BLEND_ADD)
        return result
    elif blend_type == 1:  # Multiply
        result = surf_a.copy()
        temp = surf_b.copy()
        white = pygame.Surface(temp.get_size())
        white.fill((255, 255, 255))
        white.set_alpha(int((1.0 - mix) * 255))
        temp.blit(white, (0, 0))
        result.blit(temp, (0, 0), special_flags=pygame.BLEND_MULT)
        return result
    else:  # Crossfade
        result = pygame.Surface(surf_a.get_size())
        result.fill((0, 0, 0))
        a_copy = surf_a.copy()
        a_copy.set_alpha(int((1.0 - mix) * 255))
        b_copy = surf_b.copy()
        b_copy.set_alpha(int(mix * 255))
        result.blit(a_copy, (0, 0))
        result.blit(b_copy, (0, 0))
        return result


def handle_key_events(ey):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitexit(0)

        if event.type == pygame.KEYDOWN:
            # ESC: exit MIDI learn first, then exit app
            if event.key == pygame.K_ESCAPE:
                if ey.midi_learn_active:
                    ey.midi_learn_active = False
                else:
                    exitexit(0)

            # M: toggle MIDI learn
            if event.key == pygame.K_m:
                ey.toggle_midi_learn()

            # MIDI learn param navigation
            if ey.midi_learn_active:
                if event.key == pygame.K_LEFT:
                    ey.midi_learn_prev_param()
                elif event.key == pygame.K_RIGHT:
                    ey.midi_learn_next_param()

            # D: toggle dual mode (Shift+D to avoid conflict with knob)
            # TAB: toggle dual mode (easy to find on JIS/US)
            if event.key == pygame.K_TAB:
                ey.toggle_dual_mode()

            # Dual mode controls: Z/X = mode B prev/next, C = blend, V/B = mix
            if ey.dual_mode:
                if event.key == pygame.K_z:
                    ey.prev_mode_b()
                elif event.key == pygame.K_x:
                    ey.next_mode_b()
                elif event.key == pygame.K_c:
                    ey.next_dual_blend()
                elif event.key == pygame.K_v:
                    ey.dual_mix = max(0.0, ey.dual_mix - 0.05)
                elif event.key == pygame.K_b:
                    ey.dual_mix = min(1.0, ey.dual_mix + 0.05)

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key = event.key
            v = 1 if event.type == pygame.KEYDOWN else 0

            # EYESY button mapping
            if key in KEY_MAPPING:
                ey.dispatch_key_event(KEY_MAPPING[key], v)

            # Knob control
            if event.type == pygame.KEYDOWN:
                if key in KNOB_KEYS_UP:
                    idx = KNOB_KEYS_UP[key]
                    ey.knob_hardware[idx] = min(1.0, ey.knob_hardware[idx] + KNOB_STEP)
                elif key in KNOB_KEYS_DOWN:
                    idx = KNOB_KEYS_DOWN[key]
                    ey.knob_hardware[idx] = max(0.0, ey.knob_hardware[idx] - KNOB_STEP)

    # Continuous knob adjustment while keys are held
    keys = pygame.key.get_pressed()
    for key_code, idx in KNOB_KEYS_UP.items():
        if keys[key_code]:
            ey.knob_hardware[idx] = min(1.0, ey.knob_hardware[idx] + KNOB_STEP)
    for key_code, idx in KNOB_KEYS_DOWN.items():
        if keys[key_code]:
            ey.knob_hardware[idx] = max(0.0, ey.knob_hardware[idx] - KNOB_STEP)

    # Continuous dual mix adjustment
    if ey.dual_mode:
        if keys[pygame.K_v]:
            ey.dual_mix = max(0.0, ey.dual_mix - 0.01)
        if keys[pygame.K_b]:
            ey.dual_mix = min(1.0, ey.dual_mix + 0.01)


def main():
    global audio_process

    print("=" * 40)
    print("  SHRTY — visual synth for macOS")
    print("  based on EYESY by Critter & Guitari")
    print("=" * 40)

    # Create data directories
    os.makedirs(os.path.join(DATA_DIR, "Modes"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "Grabs"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "Scenes"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "System"), exist_ok=True)

    # Create EYESY object
    ey = eyesy_mod.Eyesy()
    ey.GRABS_PATH = os.path.join(DATA_DIR, "Grabs") + "/"
    ey.MODES_PATH = os.path.join(DATA_DIR, "Modes") + "/"
    ey.SCENES_PATH = os.path.join(DATA_DIR, "Scenes") + "/"
    ey.SYSTEM_PATH = os.path.join(DATA_DIR, "System") + "/"

    try:
        # Load config
        ey.load_config_file()
        ey.load_palettes()

        # Init MIDI
        print("SHRTY: init MIDI...")
        midi.init()
        ey.usb_midi_device = midi.input_port_usb

        # Init audio
        print("SHRTY: init audio...")
        BUFFER_SIZE = 100
        shared_buffer = Array(c_float, BUFFER_SIZE, lock=True)
        shared_buffer_r = Array(c_float, BUFFER_SIZE, lock=True)
        write_index = Value('i', 0)
        gain = Value('f', 1.0)
        peak = Value('f', 0)
        peak_r = Value('f', 0)
        lock = Lock()

        audio_process = Process(
            target=sound.audio_processing,
            args=(shared_buffer, shared_buffer_r, write_index, gain, peak, peak_r, lock)
        )
        audio_process.start()

        # Init pygame
        pygame.init()
        pygame.display.set_caption("SHRTY")
        clocker = pygame.time.Clock()

        print(f"SHRTY: pygame {pygame.version.ver}")

        # Window
        hwscreen = pygame.display.set_mode(WINDOW_SIZE)
        ey.xres = hwscreen.get_width()
        ey.yres = hwscreen.get_height()
        print(f"SHRTY: window {ey.xres}x{ey.yres}")
        hwscreen.fill((0, 0, 0))
        pygame.display.flip()

        # Mode drawing surfaces
        mode_screen = pygame.Surface((ey.xres, ey.yres))
        mode_screen_b = pygame.Surface((ey.xres, ey.yres))
        ey.screen = mode_screen

        # Load modes
        if not ey.load_modes():
            print("SHRTY: no modes found in " + ey.MODES_PATH)
            osd.loading_banner(hwscreen, "No Modes found. Add mode folders to data/Modes/")
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        exitexit(0)
                time.sleep(1)

        # Run setup for all modes
        print("SHRTY: running mode setups...")
        for i in range(len(ey.mode_names)):
            try:
                ey.set_mode_by_index(i)
                mode = sys.modules[ey.mode]
            except AttributeError:
                print(f"  skip {ey.mode_names[i]} (not loaded)")
                continue
            try:
                osd.loading_banner(hwscreen, "Loading " + str(ey.mode))
                mode.setup(hwscreen, ey)
            except Exception:
                print(f"  error in setup for {ey.mode}")
                continue

        # Load grabs and scenes
        ey.load_grabs()
        ey.load_scenes()

        # Font
        font_path = os.path.join(SHRTY_DIR, "font.ttf")
        ey.font = pygame.font.Font(font_path, 16)

        # Memory
        ey.memory_used = min(psutil.virtual_memory()[2], 100)

        # Set initial mode
        ey.set_mode_by_index(0)
        mode = sys.modules[ey.mode]

        # Menu screens
        ey.menu_screens["home"] = ScreenMainMenu(ey)
        ey.menu_screens["test"] = ScreenTest(ey)
        ey.menu_screens["video_settings"] = ScreenVideoSettings(ey)
        ey.menu_screens["palette"] = ScreenPalette(ey)
        ey.menu_screens["wifi"] = ScreenWiFi(ey)
        ey.menu_screens["applogs"] = ScreenApplogs(ey)
        ey.menu_screens["midi_settings"] = ScreenMIDISettings(ey)
        ey.menu_screens["midi_pc_mapping"] = ScreenMIDIPCMapping(ey)
        ey.switch_menu_screen("home")

        # LFO for simulated sound
        undulate_p = 0

        start = time.time()

    except Exception as e:
        print(traceback.format_exc())
        print("SHRTY: init error")
        exitexit(1)

    # === MAIN LOOP ===
    print("SHRTY: running! Press ESC to quit.")
    print("  1: OSD (shift+1: menu)  2: shift(hold)  3: auto-clear")
    print("  4/5: mode prev/next  6/7: scene prev/next")
    print("  8: save scene  9: screenshot  0: trigger")
    print("  Q/W/E/R/T: knobs up, A/S/D/F/G: knobs down")
    print("  TAB: dual mode  Z/X: mode B prev/next  C: blend  V/B: mix")
    print("  M: MIDI learn  LEFT/RIGHT: param  ESC: exit learn")

    while True:
        try:
            handle_key_events(ey)
            ey.update_key_repeater()

            # MIDI
            midi.recv(ey)

            # Knobs
            ey.update_knobs_and_notes()
            ey.check_gain_knob()
            ey.knob_seq_run()
            ey.set_knobs()

            # FPS
            ey.frame_count += 1
            if (ey.frame_count % 30) == 0:
                now = time.time()
                ey.fps = 1 / ((now - start) / 30)
                start = now

            # Audio input
            if not ey.key10_status:
                with lock:
                    ey.audio_in[:] = shared_buffer[:]
                    ey.audio_in_r[:] = shared_buffer_r[:]
                    g = ey.config["audio_gain"]
                    gain.value = float((g * g * 50) + 1)
                    ey.audio_peak = peak.value
                    ey.audio_peak_r = peak_r.value
                    if (ey.config["trigger_source"] == 0 or ey.config["trigger_source"] == 2):
                        if (ey.audio_peak > 20000 or ey.audio_peak_r > 20000):
                            ey.trig = True
            else:
                # Simulated sound (key 0 held)
                if not ey.menu_mode:
                    undulate_p += .005
                    undulate = ((math.sin(undulate_p * 2 * math.pi) + 1) * 2) + .5
                    for i in range(len(ey.audio_in)):
                        ey.audio_in[i] = int(math.sin((i / 100) * 2 * math.pi * undulate) * 25000)
                        ey.audio_in_r[i] = ey.audio_in[i]
                    ey.audio_peak = 25000
                    ey.audio_peak_r = 25000

            # Set mode A
            try:
                mode = sys.modules[ey.mode]
            except:
                ey.error = f"Mode {ey.mode} not loaded."
                pygame.time.wait(200)

            # Screenshot
            if ey.screengrab_flag:
                ey.screengrab()

            ey.update_scene_save_key()

            # Auto clear
            if ey.auto_clear:
                mode_screen.fill(ey.bg_color)
                if ey.dual_mode:
                    mode_screen_b.fill(ey.bg_color)

            # Run setup if needed (mode reload)
            if ey.run_setup:
                ey.error = ''
                try:
                    mode.setup(hwscreen, ey)
                except Exception as e:
                    ey.error = traceback.format_exc()

            # Run setup for mode B if needed
            if ey.dual_mode and ey.run_setup_b:
                ey.run_setup_b = False
                try:
                    mode_b = sys.modules[ey.mode_b]
                    mode_b.setup(hwscreen, ey)
                except Exception as e:
                    print(f"SHRTY: error in mode B setup: {e}")

            # Draw
            if not ey.menu_mode:
                # Draw mode A
                try:
                    mode.draw(mode_screen, ey)
                except Exception as e:
                    ey.error = traceback.format_exc()
                    pygame.time.wait(200)

                if ey.dual_mode:
                    # Draw mode B
                    try:
                        mode_b = sys.modules[ey.mode_b]
                        mode_b.draw(mode_screen_b, ey)
                    except Exception as e:
                        ey.error = traceback.format_exc()
                        pygame.time.wait(200)

                    # Blend A + B
                    blended = blend_surfaces(mode_screen, mode_screen_b, ey.dual_blend, ey.dual_mix)
                    hwscreen.blit(blended, (0, 0))
                else:
                    hwscreen.blit(mode_screen, (0, 0))

            # OSD
            if ey.show_osd and not ey.menu_mode:
                try:
                    osd.render_overlay_480(hwscreen, ey)
                except Exception as e:
                    ey.error = traceback.format_exc()
                    pygame.time.wait(200)

            # Dual mode indicator (always show when active)
            if ey.dual_mode and not ey.menu_mode:
                osd.render_dual_mode(hwscreen, ey)

            # MIDI Learn overlay
            if ey.midi_learn_active:
                osd.render_midi_learn(hwscreen, ey)

            # Menu
            if ey.menu_mode:
                try:
                    ey.current_screen.handle_events()
                    ey.current_screen.render_with_title(hwscreen)
                except Exception as e:
                    ey.error = traceback.format_exc()
                    pygame.time.wait(200)
                if ey.restart:
                    print("SHRTY: restart requested")
                    exitexit(1)
                if not ey.menu_mode:
                    hwscreen.fill(ey.bg_color)

            pygame.display.flip()
            ey.clear_flags()

        except Exception as e:
            ey.clear_flags()
            ey.error = traceback.format_exc()
            print(f"SHRTY: main loop error: {ey.error}")
            pygame.time.wait(200)

        clocker.tick(30)


if __name__ == "__main__":
    main()
