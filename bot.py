import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
initial_extensions = ["cogs.ai"]

async def main():
    async with bot:
        for ext in initial_extensions:
            await bot.load_extension(ext)
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
