from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultCachedVoice
from services.voice import VoiceService

router = Router()
voice_service: VoiceService = VoiceService()


@router.inline_query()
async def inline_handler(query: InlineQuery):
    found_voices = voice_service(query.query) 

    results = []
    for name, file_id in found_voices:
        results.append(
            InlineQueryResultCachedVoice(
                id=f"voice_{hash(name)}", 
                voice_file_id=file_id,
                title=str(name)
            )
        )

    await query.answer(
        results, 
        cache_time=1, 
        is_personal=True 
    )
