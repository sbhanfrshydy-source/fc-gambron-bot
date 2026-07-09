
import asyncio
import hashlib
import json
import os
import re
from pathlib import Path
from telethon import TelegramClient, events
from loguru import logger
import config

logger.remove()
logger.add(lambda msg: print(msg, end=""), level="INFO")

user_client = TelegramClient("session_user", int(os.getenv("API_ID", "0")), os.getenv("API_HASH"))
bot_client = TelegramClient("session_bot", int(os.getenv("API_ID", "0")), os.getenv("API_HASH")).start(bot_token=os.getenv("BOT_TOKEN"))

def load_seen():
    if Path("seen.json").exists():
        return set(json.loads(Path("seen.json").read_text()))
    return set()

def save_seen(seen):
    Path("seen.json").write_text(json.dumps(list(seen)))

seen = load_seen()

def msg_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if config.SIGNATURE:
        text = text + config.SIGNATURE
    return text.strip()

@user_client.on(events.NewMessage(chats=config.SOURCE_CHANNELS))
async def handler(event):
    text = event.message.text or ""
    if not text or len(text) < config.MIN_TEXT_LENGTH:
        return
    h = msg_hash(text)
    if config.DUPLICATE_CHECK and h in seen:
        return
    seen.add(h)
    save_seen(seen)
    cleaned = clean_text(text)
    for ch in config.TARGET_CHANNELS:
        try:
            await bot_client.send_message(ch.strip(), cleaned)
            await asyncio.sleep(config.SEND_DELAY)
        except Exception as e:
            logger.error(str(e))

async def main():
    await user_client.start(phone=os.getenv("PHONE_NUMBER"))
    logger.info("Bot started")
    await asyncio.gather(user_client.run_until_disconnected(), bot_client.run_until_disconnected())

asyncio.run(main())
