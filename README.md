# Iron Clap - Jarvis-Style Clap Activation

Trigger VS Code and "Back in Black" with a clap (like Iron Man!)

## Setup

1. Install required Python packages:
```bash
pip install sounddevice numpy scipy
```

2. Grant microphone access to Terminal/Python when prompted.

## Run

```bash
python3 iron_clap.py
```

The script will listen for loud sounds (claps). When detected, it:
- Opens VS Code
- Plays "Back in Black" in YouTube

## Tune Sensitivity

Adjust `CLAP_THRESHOLD` in the script:
- Lower (0.2-0.3): More sensitive, triggers on quiet sounds
- Higher (0.5-0.7): Only loud claps trigger it

## Note

The Spotify action may need your Apple ID logged in for track search to work. If it doesn't work, you can replace the Apple Script line with a specific Spotify URI or playlist.
