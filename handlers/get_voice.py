import logging
from aiogram import F, types
from aiogram import Router

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.voice)
async def get_voice_id(message: types.Message):
    """
    Extract and return the voice file_id.

    :param message: Telegram message with voice.
    """
    file_id = message.voice.file_id
    await message.answer(f"ID for voice message:\n\n<code>{file_id}</code>", parse_mode="HTML")
    logger.info(f"ID for voice message: {file_id}")
