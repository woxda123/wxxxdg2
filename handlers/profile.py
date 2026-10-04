from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import profile_kb
from localization import get_text

router = Router()

@router.message(Command("profile"))
async def cmd_profile(message: Message, db):
    await db.create_user(message.from_user.id, message.from_user.full_name)
    lang = await db.get_language(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    money = user[3] if user else 0
    gems = user[4] if user else 0
    games_count = user[5] if user else 0
    wins = user[6] if user else 0
    text = get_text(lang, "profile",
                    money=f"{money:,}".replace(",", " "),
                    gems=gems, games=games_count, wins=wins)
    await message.answer(text, reply_markup=profile_kb(), parse_mode="HTML")

@router.callback_query(F.data == "stats")
async def cb_stats(callback: CallbackQuery, db):
    lang = await db.get_language(callback.from_user.id)
    user = await db.get_user(callback.from_user.id)
    games_count = user[5] if user else 0
    wins = user[6] if user else 0
    await callback.message.answer(get_text(lang, "stats", games=games_count, wins=wins))
    await callback.answer()
