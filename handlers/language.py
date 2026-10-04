import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import language_kb, LANG_NAMES, start_kb
from localization import get_text

router = Router()

@router.message(Command("language"))
async def cmd_language(message: Message, db):
    await db.create_user(message.from_user.id, message.from_user.full_name)
    lang = await db.get_language(message.from_user.id)
    await message.answer(get_text(lang, "language_choose"), reply_markup=language_kb())

@router.callback_query(F.data == "open_langs")
async def cb_open_langs(callback: CallbackQuery, db):
    await db.create_user(callback.from_user.id, callback.from_user.full_name)
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "language_choose"),
        reply_markup=language_kb()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("lang_"))
async def cb_set_language(callback: CallbackQuery, db):
    code = callback.data.split("_")[1]
    await db.set_language(callback.from_user.id, code)
    lang_name = LANG_NAMES.get(code, code)
    await callback.message.edit_text(get_text(code, "language_set", lang=lang_name))
    await callback.answer("✅")
    await asyncio.sleep(1.5)
    try:
        await callback.message.answer(
            get_text(code, "start"),
            reply_markup=start_kb(),
            parse_mode="HTML"
        )
    except Exception:
        pass

@router.callback_query(F.data == "back_to_start")
async def cb_back_to_start(callback: CallbackQuery, db):
    lang = await db.get_language(callback.from_user.id)
    await callback.message.edit_text(
        get_text(lang, "start"),
        reply_markup=start_kb(),
        parse_mode="HTML"
    )
    await callback.answer()
