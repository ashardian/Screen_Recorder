# Kooha-Style Screen Recorder

A minimal **screen recording tool** inspired by [Kooha](https://apps.gnome.org/Kooha/), built in Python with PyQt6. It offers a slim bar-style GUI that stays at the top of your screen with features like pause/resume, audio selection, format selection, and a directory selector.

## ✨ Features

- ✅ Record full screen with FFmpeg backend
- ✅ Choose between `mp4`, `mkv`, and `webm` formats
- ✅ Audio on/off toggle
- ✅ Start / Pause / Resume / Stop buttons
- ✅ Directory picker for saving files
- ✅ Auto‑naming for recordings (no overwrite)
- ✅ Floating slim bar with transparency and rounded corners
- ✅ Close button that stops background processes

## 📦 Requirements

Install Python 3.9+ and run:

```bash
pip install -r requirements.txt
```

Also make sure FFmpeg is installed on your system:

**Linux (Debian/Ubuntu):**

```bash
sudo apt install ffmpeg
```

**Windows:**

- Download from [FFmpeg.org](https://ffmpeg.org/download.html)
- Add `ffmpeg.exe` to your system `PATH`

**Mac:**

```bash
brew install ffmpeg
```

## 🚀 Usage

Run the app:

```bash
python3 screenrecorder.py
```

1. Select a directory to save recordings.
2. Choose your desired format and audio option.
3. Click **Start** to begin recording.
4. Use **Pause/Resume** as needed.
5. Click **Stop** to finish and save.
6. **Close** button will terminate the app and recording if active.

## 🛠 Notes

- Ensure FFmpeg is in your PATH.
- GUI is transparent with rounded corners and will not appear in recordings.
- The bar stays always on top for easy access.

## 📜 License

MIT License. Feel free to modify and enhance!

---

Happy recording! 🎥✨

