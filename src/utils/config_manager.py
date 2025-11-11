import json
import logging
from pathlib import Path

logger = logging.getLogger("stefan-bot")

class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path
        self.config = self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("config.json not found. Copy config.example.json to config.json and fill values.")
            return {}
        except Exception as e:
            logger.exception("Failed to load config.json: %s", e)
            return {}

    def save(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    # Convenience getters
    def get_timezone(self):
        return self.config.get("timezone", "Europe/Prague")

    def get_channel_id(self):
        cid = self.config.get("pets_channel_id", 0)
        return cid if cid else None

    def get_channel_name(self):
        return self.config.get("pets_channel_name", "pets")

    def get_guild_id(self):
        return self.config.get("guild_id")

    def get_desired_nickname(self):
        return self.config.get("desired_nickname", "Štefan")

    def get_data_file(self):
        return self.config.get("data_file", "data/pets_data.json")

    def get_flatmates(self):
        return self.config.get("flatmates", [])

    def get_rotation(self, key):
        return self.config.get(key, {}).get("rotation_user_ids", [])

    def get_time(self, key, default):
        return self.config.get(key, {}).get("time", default)

    def get_post_time(self, key, default):
        return self.config.get(key, {}).get("post_time", default)
