import asyncio
import logging
import os

import discord
from discord.ext import commands

from src.utils.config_manager import ConfigManager
from src.utils.pet_schedule_manager import PetScheduleManager
from src.cogs.pets import PetsCog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("stefan-bot")

class StefanBot(commands.Bot):
    def __init__(self, config):
        logger.info("Initializing StefanBot")
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.reactions = True

        super().__init__(
            command_prefix=config.get("prefix","!"),
            intents=intents
        )
        self.config_manager = ConfigManager()
        self.pet_schedule = PetScheduleManager(self.config_manager.get_data_file())
        logger.info(f"Bot initialization completed")

    async def setup_hook(self):
        logger.info("Setting up bot hook")
        await self.add_cog(PetsCog(self))
        try:
            await self.tree.sync()
            logger.info("Commands synced")
        except Exception as e:
            logger.exception("Failed to sync commands: %s", e)

    async def on_ready(self):
        logger.info("Logged in as %s (%s)", self.user, self.user.id)
        # Try to set nickname
        try:
            desired = self.config_manager.get_desired_nickname()
            gid = self.config_manager.get_guild_id()
            if gid:
                guild = self.get_guild(gid)
                if guild:
                    me = guild.me
                    if me and me.nick != desired:
                        await me.edit(nick=desired, reason="Set by Štefan bot on startup")
                        logger.info("Nickname set to %s", desired)
        except Exception as e:
            logger.warning("Could not set nickname: %s", e)

def load_config():
    logger.info("Loading configuration from config.json")
    path = "config.json"
    if not os.path.exists(path):
        logger.error("Missing config.json. Copy config.example.json and edit it.")
        return {}
    import json
    with open(path,"r",encoding="utf-8") as f:
        return json.load(f)

async def main():
    logger.info("🚀 Starting Discord Pet Bot")
    logger.info("Loading configuration")
    try:
        cfg = load_config()
    except Exception as e:
        logger.critical(f"Failed to start bot due to configuration error: {e}")
        return
    token = os.getenv("DISCORD_BOT_TOKEN", cfg.get("token"))
    if not token:
        logger.critical("Bot token not provided (env DISCORD_BOT_TOKEN or config.json 'token').")
        return

    bot = StefanBot(cfg)
    logger.info("🎬 Starting bot...")
    try:
        await bot.start(token)
    except discord.LoginFailure:
        logger.critical("❌ Invalid bot token. Please check your DISCORD_BOT_TOKEN environment variable.")
    except Exception as e:
        logger.critical(f"Error starting bot: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("Script executed directly")
    asyncio.run(main())
