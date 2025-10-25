import discord
import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

class AI(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel("gemini-pro")

    @discord.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not content:
                reply = (
                    "**Professional Gemini AI chat bot at your service!**\n"
                    "Tag me and ask your question."
                )
            else:
                reply = await self.generate_ai_reply(content)

            await message.channel.send(f"{reply}\n\n*Requested by {message.author.display_name}*")

    async def generate_ai_reply(self, user_message):
        try:
            response = await self.model.generate_content_async(user_message)
            return response.text.strip()
        except Exception:
            return "Sorry, I couldn't generate a reply right now."

async def setup(bot):
    await bot.add_cog(AI(bot))
