import os
import time
import random
import discord
from dotenv import load_dotenv

load_dotenv()

# 控えめ版の鳩ネタbotです。
TRIGGERS = [
    "鳩", "はと", "ハト", "ドバト", "ハトポッポ", "はとぽっぽ"
]

RESPONSES = [
    "🕊️ デデーポーポー",
    "🕊️ うわぁ〜、鳩だあ〜？！",
    "🕊️ プルップウ……",
    "🕊️ くるっくー",
]

COOLDOWN_SECONDS = 10  # うっとおしいので時間つけた。もう少し長くてもいいかも。

# 指定チャンネルのみ反応します。
PIGEON_CHANNEL_ID = os.getenv("PIGEON_CHANNEL_ID", "").strip()
if not PIGEON_CHANNEL_ID.isdigit():
    raise SystemExit("PIGEON_CHANNEL_ID が未設定か不正です。チャンネルIDを .env に入れてください。")

PIGEON_CHANNEL_ID = int(PIGEON_CHANNEL_ID)

# こちらはDiscord 設定 
intents = discord.Intents.default()
intents.message_content = True  # 本文検知用です

client = discord.Client(intents=intents)

_last_reply_at = 0.0  # チャンネル限定で。

def cooldown_ok() -> bool:
    global _last_reply_at
    now = time.time()
    if now - _last_reply_at >= COOLDOWN_SECONDS:
        _last_reply_at = now
        return True
    return False

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (id={client.user.id})")
    print(f"✅ Pigeon channel id: {PIGEON_CHANNEL_ID}")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # 指定チャンネル以外なしで
    if message.channel.id != PIGEON_CHANNEL_ID:
        return

    content = message.content
    if any(t in content for t in TRIGGERS):
        if cooldown_ok():
            await message.channel.send(random.choice(RESPONSES))

token = os.getenv("DISCORD_TOKEN", "").strip()
if not token:
    raise SystemExit("DISCORD_TOKEN が未設定です。.env に入れてください。")

client.run(token)