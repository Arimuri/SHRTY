"""
SHRTY — macOS audio input via sounddevice (replaces ALSA sound.py)
Captures system audio input (mic/line-in) and writes to shared buffers.
"""
from multiprocessing import Process, Array, Value, Lock
from ctypes import c_float
import sounddevice as sd
import time

BUFFER_SIZE = 100
max_peak = 0
max_peak_r = 0

def audio_processing(shared_buffer, shared_buffer_r, write_index, gain, peak, peak_r, lock):
    global max_peak, max_peak_r

    rate = 32000
    blocksize = 128

    def callback(indata, frames, time_info, status):
        global max_peak, max_peak_r
        if status:
            print(f"sounddevice status: {status}")

        g = gain.value if gain.value > 0 else 1.0
        actual_channels = indata.shape[1] if len(indata.shape) > 1 else 1

        for i in range(0, frames, 16):
            if i + 16 <= frames:
                # Left channel average
                if actual_channels > 1:
                    avg_l = sum(indata[i:i+16, 0]) / 16 * 32767 * g
                else:
                    avg_l = sum(indata[i:i+16, 0]) / 16 * 32767 * g

                avg_l = max(-32768, min(32767, avg_l))

                # Right channel (or duplicate left if mono)
                if actual_channels >= 2:
                    avg_r = sum(indata[i:i+16, 1]) / 16 * 32767 * g
                else:
                    avg_r = avg_l
                avg_r = max(-32768, min(32767, avg_r))

                if abs(avg_l) > abs(max_peak):
                    max_peak = avg_l
                if abs(avg_r) > abs(max_peak_r):
                    max_peak_r = avg_r

                with lock:
                    shared_buffer[write_index.value] = avg_l
                    shared_buffer_r[write_index.value] = avg_r
                    write_index.value = (write_index.value + 1) % BUFFER_SIZE

                    if write_index.value == 0:
                        peak.value = max_peak
                        peak_r.value = max_peak_r
                        max_peak = 0
                        max_peak_r = 0

    # Detect how many input channels the default device supports
    try:
        dev_info = sd.query_devices(sd.default.device[0], 'input')
        max_ch = dev_info['max_input_channels']
        channels = min(2, max_ch)
        print(f"Available audio devices:")
        print(sd.query_devices())
        print(f"Default input: {dev_info['name']} ({max_ch}ch max, using {channels}ch)")
    except Exception:
        channels = 1

    try:
        with sd.InputStream(
            samplerate=rate,
            channels=channels,
            blocksize=blocksize,
            callback=callback,
            dtype='float32'
        ):
            print(f"SHRTY audio: capturing at {rate}Hz, {channels}ch")
            while True:
                time.sleep(1)
    except Exception as e:
        print(f"Audio error ({channels}ch): {e}")
        if channels > 1:
            try:
                with sd.InputStream(
                    samplerate=rate,
                    channels=1,
                    blocksize=blocksize,
                    callback=callback,
                    dtype='float32'
                ):
                    print(f"SHRTY audio: capturing at {rate}Hz, 1ch (fallback)")
                    while True:
                        time.sleep(1)
            except Exception as e2:
                print(f"Audio fallback also failed: {e2}")
        else:
            print("SHRTY audio: no audio input available")
