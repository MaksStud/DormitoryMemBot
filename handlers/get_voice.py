from aiogram import F, types
from aiogram import Router

router = Router()


@router.message(F.voice)
async def get_voice_id(message: types.Message):
    file_id = message.voice.file_id
    await message.answer(f"Твій ID для settings.py:\n\n<code>{file_id}</code>", parse_mode="HTML")
    print(f"Отримано ID: {file_id}")
