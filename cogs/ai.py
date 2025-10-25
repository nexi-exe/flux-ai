import discord
from discord.ext import commands
import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel("gemini-pro")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not content:
                reply = (
                    "**__Flux__ AI chat bot here!**\n"
                    "Tag me and ask your question."
                )
            else:
                reply = await self.generate_ai_reply(content)

            # Tag the interaction user
            await message.channel.send(f"{message.author.mention} {reply}\n\n*Requested by {message.author.display_name}*")

    async def generate_ai_reply(self, user_message):
        try:
            response = await self.model.generate_content_async(user_message)
            return response.text.strip()
        except Exception:
            return "Sorry, I couldn't generate a reply right now."

async def setup(bot):
    await bot.add_cog(AI(bot))
