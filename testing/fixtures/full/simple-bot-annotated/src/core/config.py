import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DatabaseConfig:
    path: str


@dataclass(frozen=True)
class CaptchaConfig:
    challenge_time: int = 15


@dataclass(frozen=True)
class AppConfig:
    tg_token: str
    bot_username: str | None
    db: DatabaseConfig
    captcha: CaptchaConfig
    debug_chats: list[int] = field(default_factory=list)
    owner_ids: list[int] = field(default_factory=list)
    proxy: str | None = None
    log_level: str = "INFO"
    log_file: str = "bot.log"


def load_config(path: str = "config.json") -> AppConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    db = DatabaseConfig(path=data.get("db", {}).get("path", "simple_bot.db"))
    captcha = CaptchaConfig(challenge_time=data.get("captcha", {}).get("challenge_time", 15))

    return AppConfig(
        tg_token=data["tg_token"],
        bot_username=data.get("bot_username"),
        db=db,
        captcha=captcha,
        debug_chats=data.get("debug_chats", []),
        owner_ids=data.get("owner_ids", []),
        proxy=data.get("proxy"),
        log_level=data.get("log_level", "INFO"),
        log_file=data.get("log_file", "bot.log"),
    )
