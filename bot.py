import discord
from discord.ext import commands
import config
import db
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = ["cogs.music", "cogs.utility", "cogs.owner", "cogs.ai"]

async def is_no_prefix(user_id):
    if user_id == config.OWNER_ID:
        return True
    whitelist = await db.get_whitelist()
    return user_id in whitelist

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # AI mention handling is in cogs/ai.py
    # No-prefix for music/utilities/owner
    if await is_no_prefix(message.author.id):
        ctx = await bot.get_context(message)
        if ctx.valid and ctx.command:  # Only for music/utility/owner commands
            await bot.invoke(ctx)
    else:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(e)

for ext in initial_extensions:
    bot.load_extension(ext)

bot.run(config.DISCORD_TOKEN)
