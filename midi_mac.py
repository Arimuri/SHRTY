"""
SHRTY — macOS MIDI input via mido + python-rtmidi
Replaces the Linux ttymidi + USB MIDI setup.
"""
import time
import traceback
import platform
import mido

def _excluded_port_prefixes():
    """Return port name prefixes that represent virtual/system ports to skip."""
    prefixes = ["System"]
    if platform.system() == "Linux":
        # ALSA loopback port present on most Linux systems
        prefixes.append("Midi Through")
    elif platform.system() == "Windows":
        # Windows built-in software synth (output-only, but guard just in case)
        prefixes.append("Microsoft MIDI Mapper")
        prefixes.append("Microsoft GS Wavetable Synth")
    return tuple(prefixes)

input_port_usb = None
midi_clock_count = 0

def _handle_note(eyesy, message):
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        num = message.note
        val = message.velocity
        if val > 0 and message.type == "note_on":
            eyesy.midi_notes[num] = 1
            if eyesy.config["trigger_source"] == 1 or eyesy.config["trigger_source"] == 2:
                eyesy.trig = True
            if eyesy.config["notes_change_mode"] == 1:
                eyesy.mode_index = num % len(eyesy.mode_names)
                eyesy.set_mode_by_index(eyesy.mode_index)
        else:
            eyesy.midi_notes[num] = 0

def _handle_control_change(eyesy, message):
    # MIDI Learn: intercept any CC and assign it
    if eyesy.midi_learn_active:
        eyesy.midi_learn_assign(message.control)
        return

    if (message.channel + 1) == eyesy.config["midi_channel"]:
        if not eyesy.menu_mode:
            if message.control == eyesy.config["knob1_cc"]: eyesy.knob_hardware[0] = message.value / 127.
            if message.control == eyesy.config["knob2_cc"]: eyesy.knob_hardware[1] = message.value / 127.
            if message.control == eyesy.config["knob3_cc"]: eyesy.knob_hardware[2] = message.value / 127.
            if message.control == eyesy.config["knob4_cc"]: eyesy.knob_hardware[3] = message.value / 127.
            if message.control == eyesy.config["knob5_cc"]: eyesy.knob_hardware[4] = message.value / 127.
        if message.control == eyesy.config["auto_clear_cc"]:
            eyesy.auto_clear = message.value > 64
        if message.control == eyesy.config["fg_palette_cc"]:
            eyesy.fg_palette = message.value % len(eyesy.palettes)
        if message.control == eyesy.config["bg_palette_cc"]:
            eyesy.bg_palette = message.value % len(eyesy.palettes)
        if message.control == eyesy.config["mode_cc"]:
            eyesy.mode_index = message.value % len(eyesy.mode_names)
            eyesy.set_mode_by_index(eyesy.mode_index)

def _handle_program_change(eyesy, message):
    if (message.channel + 1) == eyesy.config["midi_channel"]:
        if f"pgm_{message.program + 1}" in eyesy.config["pc_map"]:
            scene = eyesy.config["pc_map"][f"pgm_{message.program + 1}"]
            print(f"attempting to load scene {scene}")
            eyesy.recall_scene_by_name(scene)

def _handle_clock(eyesy, message):
    global midi_clock_count
    ts = eyesy.config["trigger_source"]
    if ts > 2:
        if ts == 3 and (midi_clock_count % 6) == 0: eyesy.trig = True
        elif ts == 4 and (midi_clock_count % 12) == 0: eyesy.trig = True
        elif ts == 5 and (midi_clock_count % 24) == 0: eyesy.trig = True
        elif ts == 6 and (midi_clock_count % 96) == 0: eyesy.trig = True
    midi_clock_count += 1

def init():
    global input_port_usb
    input_ports = mido.get_input_names()
    print(f"SHRTY MIDI: available ports: {input_ports}")
    excluded = _excluded_port_prefixes()
    valid_port = next((port for port in input_ports if not port.startswith(excluded)), None)
    if valid_port:
        try:
            print(f"SHRTY MIDI: opening {valid_port}")
            input_port_usb = mido.open_input(valid_port)
        except Exception as e:
            print(f"SHRTY MIDI: error opening {valid_port}: {e}")
            input_port_usb = None
    else:
        print("SHRTY MIDI: no MIDI devices found (will work without)")

def close():
    global input_port_usb
    if input_port_usb:
        try:
            input_port_usb.close()
            print("SHRTY MIDI: closed")
        except Exception as e:
            print(f"SHRTY MIDI: error closing: {e}")

def recv(eyesy):
    global input_port_usb
    if not input_port_usb:
        return
    try:
        for message in input_port_usb.iter_pending():
            try:
                if message.type == 'clock':
                    _handle_clock(eyesy, message)
                elif message.type in ('note_on', 'note_off'):
                    _handle_note(eyesy, message)
                elif message.type == 'control_change':
                    _handle_control_change(eyesy, message)
                elif message.type == 'program_change':
                    _handle_program_change(eyesy, message)
            except Exception as e:
                print(f"SHRTY MIDI: error processing {message}: {e}")
    except Exception as e:
        print(f"SHRTY MIDI: error receiving: {e}")
