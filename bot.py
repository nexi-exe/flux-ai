import discord
from discord.ext import commands
import config
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
initial_extensions = ["cogs.ai"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Set status to DND and activity to Streaming
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Streaming(
            name="Your Mom",
            url="https://twitch.tv/discord"
        )
    )

async def main():
    async with bot:
        for ext in initial_extensions:
            await bot.load_extension(ext)
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
