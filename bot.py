import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.utils import executor
from dotenv import load_dotenv
import subprocess
import uuid

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_url(message: types.Message):
    url = message.text.strip()

    # Unique file name
    video_id = str(uuid.uuid4())
    output_path = f"{video_id}.mp4"

    await message.reply("🔄 Downloading...")

    try:
        subprocess.run([
            "yt-dlp", url,
            "-o", output_path,
            "-f", "best"
        ], check=True)

        video = FSInputFile(output_path)
        await message.reply_video(video, caption="✅ Here is your video!")
        os.remove(output_path)

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
