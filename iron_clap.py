#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import subprocess
import time
import threading
import queue
import platform

CLAP_THRESHOLD = 0.4
SAMPLE_RATE = 44100
COOLDOWN_SECONDS = 2

last_clap_time = 0
clap_queue = queue.Queue()

VSCODE_APPS = {
    "Darwin": "Visual Studio Code",
    "Linux": "code",
    "Windows": "Code"
}

OPENCODE_APPS = {
    "Darwin": "OpenCode"
}

def get_os():
    return platform.system()

def open_app(app_name, os_specific_names=None):
    os_name = get_os()
    
    if os_specific_names and app_name in os_specific_names:
        app_name = os_specific_names[app_name]
    
    if os_name == "Darwin":
        subprocess.run(["open", "-a", app_name])
    elif os_name == "Linux":
        subprocess.run(["xdg-open", app_name])
    elif os_name == "Windows":
        subprocess.run(["start", "", app_name], shell=True)

def open_url(url):
    os_name = get_os()
    
    if os_name == "Darwin":
        subprocess.run(["open", url])
    elif os_name == "Linux":
        subprocess.run(["xdg-open", url])
    elif os_name == "Windows":
        subprocess.run(["start", "", url], shell=True)

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
    os_name = get_os()
    print(f"Detected OS: {os_name}")
    print("Opening VS Code and playing Back in Black...")
    
    open_app("VSCode", VSCODE_APPS)
    time.sleep(0.5)
    open_url("https://www.youtube.com/watch?v=qRrElw4TSB4&autoplay=1")
    
    if os_name == "Darwin":
        time.sleep(0.5)
        open_app("OpenCode", OPENCODE_APPS)

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
