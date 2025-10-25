import discord
import openai
import config

openai.api_key = config.OPENAI_API_KEY

class AI(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not content:
                reply = (
                    "**Professional AI chat bot at your service!**\n"
                    "Tag me and ask your question."
                )
            else:
                reply = await self.generate_ai_reply(content)

            await message.channel.send(f"{reply}\n\n*Requested by {message.author.display_name}*")

    async def generate_ai_reply(self, user_message):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional AI assistant for Discord. Reply with clear, concise, and well-formatted markdown."},
                    {"role": "user", "content": user_message}
                ]
            )
            return resp.choices[0].message['content'].strip()
        except Exception:
            return "Sorry, I couldn't generate a reply right now."

async def setup(bot):
    await bot.add_cog(AI(bot))
