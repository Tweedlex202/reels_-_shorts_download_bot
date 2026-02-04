import os
import io
import sys
import re
import shutil
import asyncio
import tempfile
import subprocess
import requests
import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ["TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "📎 Отправь мне ссылку на Instagram Reels или YouTube Shorts\n"
        "и я скачаю видео для тебя."
    )


def is_instagram_reels(url: str) -> bool:
    url = url.strip().rstrip("/")
    return "instagram.com/reel" in url or "instagram.com/p/" in url


def is_youtube_shorts(url: str) -> bool:
    url = url.strip().rstrip("/")
    return "youtube.com/shorts/" in url


def _extract_shortcode(url: str) -> str:
    match = re.search(r"(?:reel|p)/([A-Za-z0-9_-]+)", url)
    if not match:
        raise ValueError("Не удалось извлечь ID из ссылки")
    return match.group(1)


def _download_instagram(url: str) -> tuple[str, bytes]:
    shortcode = _extract_shortcode(url)
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    if not post.is_video:
        raise RuntimeError("Это не видео")

    title = post.caption.split("\n")[0][:50].strip() if post.caption else "video"
    title = re.sub(r"[^\w\s-]", "", title).strip() or "video"

    resp = requests.get(post.video_url)
    resp.raise_for_status()

    return title, resp.content


def _download_youtube(url: str) -> tuple[str, bytes]:
    # Скачивание во /tmp (tmpfs — RAM, не диск), после чтения папка удаляется
    tmp_dir = tempfile.mkdtemp()
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-o", os.path.join(tmp_dir, "%(title)s.%(ext)s"),
                "--format", "bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "--concurrent-fragments", "5",
                "--quiet", "--no-warnings", url,
            ],
            capture_output=True, timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode())

        files = os.listdir(tmp_dir)
        if not files:
            raise RuntimeError("Файл не загружен")

        title = re.sub(r"[^\w\s-]", "", os.path.splitext(files[0])[0])[:50].strip() or "video"

        with open(os.path.join(tmp_dir, files[0]), "rb") as f:
            return title, f.read()
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        await update.message.reply_text("📎 Отправь ссылку на Instagram Reels или YouTube Shorts")
        return

    url = text.strip()

    if is_youtube_shorts(url):
        download_fn = _download_youtube
    elif is_instagram_reels(url):
        download_fn = _download_instagram
    else:
        await update.message.reply_text("📎 Отправь ссылку на Instagram Reels или YouTube Shorts")
        return

    await update.message.reply_text("⬇️ Загружаю видео...")
    try:
        title, video_bytes = await asyncio.to_thread(download_fn, url)
        await update.effective_chat.send_video(
            video=io.BytesIO(video_bytes),
            filename=f"{title}.mp4",
        )
        await update.effective_chat.send_message(
            "✅ Готово!\n\n📎 Отправь ссылку на Instagram Reels или YouTube Shorts"
        )
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        await update.message.reply_text("❌ Ошибка загрузки. Проверь ссылку или попробуй снова.")


async def auto_update():
    while True:
        await asyncio.sleep(12 * 3600)
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "pip", "install", "--upgrade", "--quiet", "instaloader", "yt-dlp",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.communicate()
        print("instaloader, yt-dlp обновлены")


async def on_startup(_app):
    asyncio.create_task(auto_update())


app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("Бот запущен.")
    app.run_polling()
