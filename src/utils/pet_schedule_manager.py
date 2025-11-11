import json
import logging
from pathlib import Path
from datetime import datetime, date

logger = logging.getLogger("stefan-bot")

class PetScheduleManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
        Path(self.data_file).parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "feed":   {"date": None, "done": False, "message_id": None, "last_reminder_hour": None},
                "filter": {"week": None, "done": False, "message_id": None, "assignee_index": 0, "last_reminder_date": None, "reminder_step": 0},
                "tank":   {"month": None, "done": False, "message_id": None, "assignee_index": 0, "last_reminder_date": None, "reminder_step": 0},
                "vacation": {}
            }
        except Exception as e:
            logger.exception("Failed to load data file: %s", e)
            return {}

    def save(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # --- Feeding ---
    def reset_feed_for_today(self, today_str):
        self.data.setdefault("feed", {})
        self.data["feed"]["date"] = today_str
        self.data["feed"]["done"] = False
        self.data["feed"]["message_id"] = None
        self.data["feed"]["last_reminder_hour"] = None
        self.save()

    def mark_fed(self):
        self.data["feed"]["done"] = True
        self.save()

    # --- Filter ---
    def start_week(self, week_str):
        self.data["filter"]["week"] = week_str
        self.data["filter"]["done"] = False
        self.data["filter"]["message_id"] = None
        self.data["filter"]["last_reminder_date"] = None
        self.data["filter"]["reminder_step"] = 0
        self.save()

    def mark_filter_done(self):
        self.data["filter"]["done"] = True
        self.data["filter"]["reminder_step"] = 0
        self.save()

    # --- Tank ---
    def start_month(self, month_str):
        self.data["tank"]["month"] = month_str
        self.data["tank"]["done"] = False
        self.data["tank"]["message_id"] = None
        self.data["tank"]["last_reminder_date"] = None
        self.data["tank"]["reminder_step"] = 0
        self.save()

    def mark_tank_done(self):
        self.data["tank"]["done"] = True
        self.data["tank"]["reminder_step"] = 0
        self.save()

    # --- Rotation & Vacation ---
    def get_vacation(self, user_id: int) -> bool:
        return bool(self.data.get("vacation", {}).get(str(user_id), False))

    def set_vacation(self, user_id: int, on: bool):
        self.data.setdefault("vacation", {})
        self.data["vacation"][str(user_id)] = on
        self.save()

    def next_in_rotation(self, rotation_ids, current_index, is_valid_member):
        n = len(rotation_ids)
        if n == 0:
            return None, current_index
        for step in range(n):
            idx = (current_index + step) % n
            uid = rotation_ids[idx]
            if is_valid_member(uid):
                return uid, idx
        return None, current_index  # no eligible members

    def advance_rotation_index(self, key: str, n: int):
        self.data[key]["assignee_index"] = (self.data[key].get("assignee_index", 0) + 1) % max(1, n)
        self.save()
