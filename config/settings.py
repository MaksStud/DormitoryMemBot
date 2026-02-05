from typing import Dict
import os
import dotenv
import json

BASE_DIR = os.path.dirname(__file__)
dotenv.load_dotenv()


BOT_SECRET_KEY = os.getenv("TELEGRAM_BOT_SECRET_KEY", "NOT_KEY")

voices_file_path = os.path.join(BASE_DIR, "voices.json")

with open(voices_file_path, "r", encoding="utf-8") as f:
    VOICES: Dict[str, str] = json.load(f)
