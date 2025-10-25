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

        # Only reply to mention
        if self.bot.user in message.mentions:
            content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not content:
                reply = (
                    "**__Flux__ AI Chat Bot here**!\n"
                    "An intelligent AI chat assistant designed to provide accurate,helpful and engaging conversations instantly,"
                    "Just mention me and ask your question."
                )
            else:
                reply = await self.generate_ai_reply(content)

            # Reply with just the user's display name, NOT a ping, and no 'Requested by'
            await message.channel.send(f"{message.author.display_name}, {reply}")

    async def generate_ai_reply(self, user_message):
        try:
            response = await self.model.generate_content_async(user_message)
            # Gemini SDK response may have .text or .parts[0].text
            if hasattr(response, "text"):
                return response.text.strip()
            elif hasattr(response, "parts"):
                return response.parts[0].text.strip()
            else:
                return "Sorry, the AI returned no text."
        except Exception as e:
            print(f"Gemini error: {e}")
            return "Sorry, I couldn't generate a reply right now."

async def setup(bot):
    await bot.add_cog(AI(bot))
