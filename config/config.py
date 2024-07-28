from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    bot: TgBot
    api_id: str


def load_config() -> Config:
    env = Env()
    env.read_env()
    return Config(bot=TgBot(token=env.str("BOT_TOKEN")), api_id=env.str("API_ID"))

