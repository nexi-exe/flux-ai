import discord
from discord.ext import commands
import config
import db

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addnoprefix", aliases=["addnp"])
    async def add_no_prefix(self, ctx, user: discord.User):
        if ctx.author.id == config.OWNER_ID:
            await db.add_to_whitelist(user.id)
            await ctx.send(f"{user.mention} added to no-prefix list.")
        else:
            await ctx.send("You do not have permission.")

    @commands.command(name="removenoprefix", aliases=["removenp"])
    async def remove_no_prefix(self, ctx, user: discord.User):
        if ctx.author.id == config.OWNER_ID:
            await db.remove_from_whitelist(user.id)
            await ctx.send(f"{user.mention} removed from no-prefix list.")
        else:
            await ctx.send("You do not have permission.")

async def setup(bot):
    await bot.add_cog(Owner(bot))
