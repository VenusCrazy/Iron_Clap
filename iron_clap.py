#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import subprocess
import time
import threading
import queue

CLAP_THRESHOLD = 0.4
SAMPLE_RATE = 44100
COOLDOWN_SECONDS = 2

last_clap_time = 0
clap_queue = queue.Queue()

def detect_clap(indata, frames, time_info, status):
    global last_clap_time
    volume = np.linalg.norm(indata) / np.sqrt(frames)
    current_time = time.time()
    
    if volume > CLAP_THRESHOLD and (current_time - last_clap_time) > COOLDOWN_SECONDS:
        print(f"Clap detected! Volume: {volume:.2f}")
        last_clap_time = current_time
        clap_queue.put(True)

def action_worker():
    while True:
        clap_queue.get()
        trigger_action()

def trigger_action():
    print("Opening VS Code and playing Back in Black...")
    subprocess.run(["open", "-a", "Visual Studio Code"])
    time.sleep(0.5)
    subprocess.run(["open", "https://www.youtube.com/watch?v=qRrElw4TSB4&autoplay=1"])
    time.sleep(0.5)
    subprocess.run(["open", "-a", "OpenCode"])

def main():
    print("Listening for claps... (Press Ctrl+C to stop)")
    print(f"Threshold: {CLAP_THRESHOLD}, Sample rate: {SAMPLE_RATE}")
    
    worker_thread = threading.Thread(target=action_worker, daemon=True)
    worker_thread.start()
    
    try:
        with sd.InputStream(callback=detect_clap, channels=1, samplerate=SAMPLE_RATE):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
