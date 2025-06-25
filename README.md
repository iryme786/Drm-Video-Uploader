# DRM-Video-Uploader-Bot

A Telegram bot that reads DRM `.m3u8` video links from a text file, auto-extracts the decryption key, decrypts the video using FFmpeg, and uploads it to a Telegram channel.

## 🔧 Setup

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Add environment variables
Create a `.env` file (use `.env.example` as a template)

### 3. Run the bot
```bash
python main.py
```

Make sure your bot is added as admin to the target Telegram channel.

## 🤖 Bot Commands

This bot is currently auto-run based (non-interactive), but you can extend it using Pyrogram command handlers.

### Included Features (as of now)
| Functionality | How it works |
|---------------|--------------|
| 🔄 Auto Read DRM links | Reads `.m3u8` links from `drm_links.txt` at runtime |
| 🧠 Auto Key Extraction | Extracts AES decryption key from `#EXT-X-KEY` in the playlist |
| 🔓 Decryption | Uses `ffmpeg` to decrypt video to `.mp4` |
| 📤 Auto Upload | Uploads to the Telegram channel defined in `.env` |

### 📌 Future Telegram Commands (if added)
If converted to interactive mode (on-message command-based), here are suggestions:
| Command | Purpose |
|---------|---------|
| `/start` | Greet the user and show usage |
| `/uploadall` | Starts processing all DRM links from the file |
| `/uploadone <m3u8>` | Process and upload just one link |
| `/status` | Show total processed and pending |
| `/clear` | Reset or clear processed log |
