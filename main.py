from aiogram import Bot, Dispatcher
from config.config import load_config, Config
from db import create_database
import handlers
import logging.config
import asyncio

create_database()


async def main():
    logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info('Starting bot...')

    config: Config = load_config()

    bot = Bot(config.bot.token)
    dp = Dispatcher(storage=handlers.storage)

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
