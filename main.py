import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from handlers.inline import router as inline_router
from handlers.get_voice import router as voice_router

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_SECRET_KEY)


async def main() -> None:
    """
    Entry point for the bot.

    Initializes routers and starts long-polling.
    """
    dp = Dispatcher()
    dp.include_router(inline_router)
    dp.include_router(voice_router)

    logger.info("The bot is up and running!")

    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == '__main__':
    """
    Script execution.

    Runs the main loop and handles KeyboardInterrupt.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
