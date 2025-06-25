import os
import subprocess
import requests
from urllib.parse import urljoin
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("21563841")),
API_HASH = os.environ.get("aa468717ecb3153d47dba2d9be6eb90d"),
BOT_TOKEN = os.environ.get("8157490670:AAH96od7VTsjHmMP-4f4tOHewpHTAqWKEv8"),
CHANNEL_ID = os.environ.get("-1002556958706")

bot = Client("drm_uploader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("👋 Welcome! Use /uploadall to process and upload videos & PDFs from `drm_links.txt`")

@bot.on_message(filters.command("uploadall"))
async def upload_all(client, message: Message):
    await message.reply_text("📦 Starting to process links from `drm_links.txt`...")

    try:
        with open("drm_links.txt", "r") as file:
            lines = file.readlines()

        for index, url in enumerate(lines):
            url = url.strip()
            if not url:
                continue

            try:
                if url.endswith(".pdf"):
                    await message.reply(f"📄 Downloading PDF ({index + 1})")
                    pdf_filename = f"file_{index + 1}.pdf"
                    response = requests.get(url)
                    with open(pdf_filename, "wb") as f:
                        f.write(response.content)
                    await bot.send_document(CHANNEL_ID, document=pdf_filename, caption=f"📄 PDF {index + 1}")
                    os.remove(pdf_filename)

                elif url.endswith(".m3u8"):
                    await message.reply(f"🎞️ Processing video ({index + 1})")
                    key_hex = extract_key(url)
                    if not key_hex:
                        await message.reply(f"❌ Key not found for {url}")
                        continue
                    video_file = f"video_{index + 1}.mp4"
                    decrypt_video(url, key_hex, video_file)
                    await bot.send_video(CHANNEL_ID, video=video_file, caption=f"📽️ Video {index + 1}")
                    os.remove(video_file)

                else:
                    await message.reply(f"⚠️ Unknown file type: {url}")

            except Exception as e:
                await message.reply(f"⚠️ Error with {url}:{str(e)}")

        await message.reply("✅ All files processed.")

    except FileNotFoundError:
        await message.reply("❌ File `drm_links.txt` not found.")

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

bot.run()
