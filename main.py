import os
import subprocess
import requests
from urllib.parse import urljoin
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # Format: -100xxxxxxxxxx

bot = Client("drm_uploader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_key(m3u8_url):
    m3u8_text = requests.get(m3u8_url).text
    for line in m3u8_text.splitlines():
        if line.startswith("#EXT-X-KEY"):
            parts = line.split("URI=")
            if len(parts) >= 2:
                key_url = parts[1].split('"')[1]
                key_url = urljoin(m3u8_url, key_url)
                key_bin = requests.get(key_url).content
                return key_bin.hex()
    return None

def decrypt_video(m3u8_url, key_hex, output_file):
    cmd = [
        "ffmpeg", "-loglevel", "quiet",
        "-allowed_extensions", "ALL",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", m3u8_url,
        "-decryption_key", key_hex,
        "-c", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)

def process_txt_file():
    with open("drm_links.txt", "r") as file:
        lines = file.readlines()

    for index, url in enumerate(lines):
        url = url.strip()
        if not url:
            continue

        try:
            if url.endswith(".pdf"):
                print(f"📄 Downloading PDF {url}")
                pdf_filename = f"file_{index + 1}.pdf"
                response = requests.get(url)
                with open(pdf_filename, "wb") as f:
                    f.write(response.content)
                bot.send_document(CHANNEL_ID, document=pdf_filename, caption=f"📄 PDF {index + 1}")
                os.remove(pdf_filename)
                print("✅ Uploaded PDF")
            elif url.endswith(".m3u8"):
                print(f"🎞️ Processing DRM Video: {url}")
                key_hex = extract_key(url)
                if not key_hex:
                    print("❌ Key not found. Skipping.")
                    continue
                video_file = f"video_{index + 1}.mp4"
                decrypt_video(url, key_hex, video_file)
                bot.send_video(CHANNEL_ID, video=video_file, caption=f"📽️ Video {index + 1}")
                os.remove(video_file)
                print("✅ Uploaded Video")
            else:
                print(f"❓ Unknown file type: {url}")
        except Exception as e:
            print(f"⚠️ Error with {url}: {str(e)}")
            

with bot:
    process_txt_file()
