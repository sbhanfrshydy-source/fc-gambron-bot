import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHANNELS = os.getenv("TARGET_CHANNELS", "@your_channel").split(",")
JOIN_CHANNEL = os.getenv("JOIN_CHANNEL", "@your_channel")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

SOURCE_CHANNELS = [
    "@League3Football_Ir",
    "@League2Football_Ir",
    "@dsport1",
    "@dsport_lig2",
]

CLEAN_LEVEL = 2

BANNED_WORDS = ["advertisement", "subscribe our channel", "our channel", "subscribe"]
EXTRA_HASHTAGS = ["#football", "#sport"]
SIGNATURE = "\n\n📢 @your_channel"
REMOVE_HASHTAGS = ["#ads", "#ad", "#spam", "#channel"]

DUPLICATE_CHECK = True
FORWARD_MEDIA = True
MIN_TEXT_LENGTH = 10
SEND_DELAY = 1
