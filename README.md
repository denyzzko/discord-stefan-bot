# Štefan – Discord pet fish bot

A Discord bot for your household pet fish. Czech cute tone, daily feeding reminders at 12:00, weekly filter cleaning with rotation, and monthly tank cleaning with rotation. Reactions ✅ (done) and ❌ (skip / reassign). Vacation mode supported per user.

## Features
- Posts in channel **#pets** (or by `pets_channel_id`) in timezone from config (default Europe/Prague).
- **Feeding**: every day at 12:00 sends: “Heeej kluci, jsem hladnej! …”. Adds ✅. Whoever adds ✅ marks feeding as done. If not done, hourly reminders get progressively spicier.
- **Filter (weekly)**: every **Monday** at `filter_clean.post_time` assigns to the next eligible user in rotation. Adds ✅ and ❌. ✅ marks done; ❌ reassigns to the next non‑vacation user.
- **Tank (monthly)**: every **1st of the month** at `tank_clean.post_time`, same mechanics as filter.
- **Vacation**: `/pet-vacation @user on|off` toggles vacation (skips from rotation).  
- **Status**: `/pet-status` shows today’s feeding and current weekly/monthly assignees.

## Quick start
1. Create a new Discord application & bot, invite it to your server with permissions to:
   - Read/Send Messages, Add Reactions
   - Read Message History
   - Manage Nicknames (optional, to set “Štefan” automatically)
2. Create channel **#pets** or note its ID.
3. Copy `config.example.json` to `config.json` and fill your values.
4. Install and run:
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DISCORD_BOT_TOKEN=YOUR_TOKEN   # or put token in config.json
python -m src.main
```
## Config
See `config.example.json`. Important fields:
- `guild_id`: your server ID (enables nickname setting and faster channel lookup)
- `pets_channel_name` or `pets_channel_id`: where the bot posts
- `timezone`: e.g., `Europe/Prague`
- `feeding.time`: daily feeding time (HH:MM)
- `filter_clean.rotation_user_ids`: list of Discord user IDs in order
- `tank_clean.rotation_user_ids`: list of Discord user IDs in order

## Data
Runtime state is stored in `data/pets_data.json`. Safe to delete if you want to reset all progress (assignments start again from index 0).

## Notes
- Make sure the bot can add reactions in #pets.
- The bot only accepts ✅ by the *assigned* user for weekly/monthly tasks. Feeding can be ✅ by anyone.
- “Aggressive” reminders are cheeky but family‑friendly. You can tune lines in `src/utils/strings.py`.
