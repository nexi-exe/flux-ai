import discord
from discord.ext import commands
from discord import app_commands
import wavelink
import config

EMOJIS = {
    "play": "▶️",
    "pause": "⏸️",
    "resume": "▶️",
    "stop": "⏹️",
    "skip": "⏭️",
    "queue": "📜",
    "leave": "👋",
}

class MusicControls(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=180)
        self.player = player

    @discord.ui.button(label="Pause", emoji=EMOJIS["pause"], style=discord.ButtonStyle.gray)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.is_playing():
            await self.player.pause()
            await interaction.response.send_message(f"{EMOJIS['pause']} Paused!", ephemeral=True)
        else:
            await interaction.response.send_message("No music is playing.", ephemeral=True)

    @discord.ui.button(label="Resume", emoji=EMOJIS["resume"], style=discord.ButtonStyle.green)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.is_paused():
            await self.player.resume()
            await interaction.response.send_message(f"{EMOJIS['resume']} Resumed!", ephemeral=True)
        else:
            await interaction.response.send_message("No music is paused.", ephemeral=True)

    @discord.ui.button(label="Skip", emoji=EMOJIS["skip"], style=discord.ButtonStyle.blurple)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.is_playing():
            await self.player.stop()
            await interaction.response.send_message(f"{EMOJIS['skip']} Skipped!", ephemeral=True)
        else:
            await interaction.response.send_message("No song to skip.", ephemeral=True)

    @discord.ui.button(label="Stop", emoji=EMOJIS["stop"], style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.is_playing() or self.player.is_paused():
            await self.player.stop()
            await interaction.response.send_message(f"{EMOJIS['stop']} Stopped!", ephemeral=True)
        else:
            await interaction.response.send_message("No music is playing.", ephemeral=True)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if not wavelink.NodePool.nodes:
            await wavelink.NodePool.create_node(
                bot=self.bot,
                host=config.LAVALINK_HOST,
                port=config.LAVALINK_PORT,
                password=config.LAVALINK_PASSWORD,
                https=False
            )

    # Prefix commands
    @commands.command(name="play", aliases=["p", "music"])
    async def play(self, ctx, *, search: str):
        await self._play(ctx, search)

    @commands.command(aliases=["j"])
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
            embed = discord.Embed(title=f"{EMOJIS['play']} Joined Voice Channel", description=f"Connected to `{ctx.author.voice.channel}`!", color=discord.Color.green())
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("You must be in a voice channel.")

    @commands.command(aliases=["stop", "st"])
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            embed = discord.Embed(title=f"{EMOJIS['leave']} Disconnected", description="Left the voice channel.", color=discord.Color.greyple())
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("I'm not connected to any voice channel.")

    # Slash commands
    @app_commands.command(name="play", description="Play music from a search or URL")
    async def play_slash(self, interaction: discord.Interaction, search: str):
        await self._play(interaction, search)

    @app_commands.command(name="join", description="Bot joins your voice channel")
    async def join_slash(self, interaction: discord.Interaction):
        if interaction.user.voice:
            await interaction.user.voice.channel.connect(cls=wavelink.Player)
            embed = discord.Embed(title=f"{EMOJIS['play']} Joined Voice Channel", description=f"Connected to `{interaction.user.voice.channel}`!", color=discord.Color.green())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You must be in a voice channel.", ephemeral=True)

    @app_commands.command(name="leave", description="Bot leaves the voice channel")
    async def leave_slash(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            embed = discord.Embed(title=f"{EMOJIS['leave']} Disconnected", description="Left the voice channel.", color=discord.Color.greyple())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("I'm not connected to any voice channel.", ephemeral=True)

    async def _play(self, ctx_or_inter, search):
        if isinstance(ctx_or_inter, commands.Context):
            author = ctx_or_inter.author
            guild = ctx_or_inter.guild
            send = ctx_or_inter.send
        else:
            author = ctx_or_inter.user
            guild = ctx_or_inter.guild
            send = ctx_or_inter.response.send_message

        if not guild.voice_client:
            if author.voice:
                vc = await author.voice.channel.connect(cls=wavelink.Player)
            else:
                await send("You must be in a voice channel.", ephemeral=True)
                return
        else:
            vc = guild.voice_client

        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        await vc.play(track)
        embed = discord.Embed(title=f"{EMOJIS['play']} Now Playing", description=f"**{track.title}**", color=discord.Color.purple())
        embed.set_footer(text=f"Requested by {author.display_name}")
        view = MusicControls(vc)
        await send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Music(bot))
