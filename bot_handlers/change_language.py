from typing import Union
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommandScopeChat
from translations.transtate import with_translation, get_translator


def language_handlers(dp):
    @dp.message(Command("language"))
    @dp.callback_query(lambda c: c.data == "language")
    @with_translation
    async def show_language(event: Union[Message, CallbackQuery], state: FSMContext, _):
        text = _("Please choose your language:")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
                    InlineKeyboardButton(text="🇪🇪 Eesti keel", callback_data="lang:et"),
                ]
            ]
        )

        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.edit_text(text, reply_markup=keyboard)
        else:
            await event.answer(text, reply_markup=keyboard)

    @dp.callback_query(lambda c: c.data and c.data.startswith("lang:"))
    async def process_language(cb, state: FSMContext):
        from main import bot, get_bot_commands

        lang = cb.data.split(":", 1)[1]
        await state.update_data(language=lang)
        _ = get_translator(lang)
        commands = get_bot_commands(_)
        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=cb.from_user.id))
        await cb.answer()
        await cb.message.edit_text(_("Language has been changed!"))
