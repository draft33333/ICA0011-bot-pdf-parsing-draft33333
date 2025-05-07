import gettext
from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

LANGUAGES = ["en", "et"]

translations = {
    lang: gettext.translation(
        "messages", localedir="translations", languages=[lang], fallback=True)
    for lang in LANGUAGES
}

def get_translator(lang: str):
    """ Get translator object for given language, fallback to English """
    return translations.get(lang, translations["en"]).gettext

def with_translation(func):
    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
        data = await state.get_data()
        lang = data.get("language") or message.from_user.language_code or "en"
        _ = get_translator(lang)
        return await func(message, state, _, *args, **kwargs)
    return wrapper