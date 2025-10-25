# Flux AI discord bot

A professional, modular Discord bot with:
- **AI Chat:** Mention the bot to talk with AI (OpenAI GPT, message replies).
- **Music:** Play, join, leave, pause/resume/skip/stop with buttons. Prefix and slash commands. Scalable with Lavalink/wavelink.
- **Utilities:** Avatar, server info, ping, help. Prefix and slash commands, all replies are embeds.
- **Owner/Whitelist:** No prefix required for owner and whitelisted users. Use MongoDB.
- **Handy, professional, and easy to use.**

## Setup

1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set these environment variables:
   - `DISCORD_TOKEN` — your bot token
   - `OPENAI_API_KEY` — your OpenAI key
   - `MONGODB_URI` — MongoDB URI
   - `OWNER_ID` — your Discord user ID
   - `LAVALINK_HOST` — Lavalink host (default `localhost`)
   - `LAVALINK_PORT` — Lavalink port (default `2333`)
   - `LAVALINK_PASSWORD` — Lavalink password (default `youshallnotpass`)
3. Run your Lavalink server ([Lavalink setup guide](https://github.com/freyacodes/Lavalink#server-setup)).
4. Run the bot:
   ```
   python bot.py
   ```

## Features

### AI Chat
- Mention the bot in any message to get an AI response.

### Music (Prefix & Slash)
- `!play <query>` / `/play <query>` — Play music
- `!join` / `/join` — Join your voice channel
- `!leave` / `/leave` — Leave voice channel
- Music control buttons: Pause, Resume, Skip, Stop

### Utilities (Prefix & Slash)
- `!ping` / `/ping` — Bot latency
- `!avatar [user]` / `/avatar [user]` — Show avatar
- `!serverinfo` / `/serverinfo` — Server info
- `!help` / `/help` — Full help embed

### Owner
- `!addnoprefix <user>` — Add user to no-prefix list
- `!removenoprefix <user>` — Remove user from no-prefix list

## Deployment

- Supports Railway, Heroku, Docker, or any Python host.
- Set environment variables for secrets.
- Run `python bot.py`.

## License

MIT
