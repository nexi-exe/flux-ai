import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prefix commands
    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        latency = round(ctx.bot.latency * 1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{latency}ms`", color=discord.Color.yellow())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, user: discord.User = None):
        target = user or ctx.author
        embed = discord.Embed(title=f"Avatar for {target.display_name}", color=discord.Color.blurple())
        embed.set_image(url=target.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["guildinfo", "server"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.green())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["commands", "cmds"])
    async def help(self, ctx):
        embed = discord.Embed(
            title="📚 Nexi-Exe Bot Help",
            description="**Here are all available commands.**\nUse either prefix `!` or `/` for slash commands. Music is controlled with buttons!",
            color=discord.Color.orange()
        )
        embed.add_field(name="Music", value="`!play <query>` / `/play <query>` - Play music\n`!join` / `/join` - Join voice\n`!leave` / `/leave` - Leave voice\nButtons for pause, resume, skip, stop.", inline=False)
        embed.add_field(name="Utility", value="`!ping` / `/ping` - Bot latency\n`!avatar [user]` / `/avatar [user]` - Show avatar\n`!serverinfo` / `/serverinfo` - Server info", inline=False)
        embed.add_field(name="Owner", value="`!addnoprefix <user>` / `!removenoprefix <user>`", inline=False)
        embed.add_field(name="AI", value="Mention the bot to chat with AI.", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    # Slash commands
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(interaction.client.latency * 1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: `{latency}ms`", color=discord.Color.yellow())
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Shows your avatar or another user's avatar")
    async def avatar_slash(self, interaction: discord.Interaction, user: discord.User = None):
        target = user or interaction.user
        embed = discord.Embed(title=f"Avatar for {target.display_name}", color=discord.Color.blurple())
        embed.set_image(url=target.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Shows info about the server")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.green())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Show all bot commands")
    async def help_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 Nexi-Exe Bot Help",
            description="**Here are all available commands.**\nUse either prefix `!` or `/` for slash commands. Music is controlled with buttons!",
            color=discord.Color.orange()
        )
        embed.add_field(name="Music", value="`/play <query>` - Play music\n`/join` - Join voice\n`/leave` - Leave voice\nButtons for pause, resume, skip, stop.", inline=False)
        embed.add_field(name="Utility", value="`/ping` - Bot latency\n`/avatar [user]` - Show avatar\n`/serverinfo` - Server info", inline=False)
        embed.add_field(name="Owner", value="`!addnoprefix <user>` / `!removenoprefix <user>`", inline=False)
        embed.add_field(name="AI", value="Mention the bot to chat with AI.", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
