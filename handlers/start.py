from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from keyboards import start_kb
from localization import get_text
from handlers.game import games

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, command: CommandObject, db):
    await db.create_user(message.from_user.id, message.from_user.full_name)
    lang = await db.get_language(message.from_user.id)

    if command.args and command.args.startswith("join_"):
        try:
            chat_id = int(command.args.split("_")[1])
        except Exception:
            await message.answer("Неверная ссылка.")
            return
        game = games.get(chat_id)
        if game and game.state == "registration":
            added = game.add_player(message.from_user.id, message.from_user.full_name)
            if added:
                await message.answer("✅ Ты добавлен в игру!")
                try:
                    await message.bot.send_message(
                        chat_id,
                        f"✅ {message.from_user.full_name} присоединился к игре!\nУчастников: {len(game.players)}"
                    )
                except Exception:
                    pass
            else:
                await message.answer("Ты уже в игре.")
        else:
            await message.answer("Игра не найдена или регистрация закрыта.")
        return

    text = get_text(lang, "start")
    if message.chat.type == "private":
        await message.answer(text, reply_markup=start_kb(), parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help(message: Message, db):
    lang = await db.get_language(message.from_user.id)
    await message.answer(get_text(lang, "help"), parse_mode="HTML")
