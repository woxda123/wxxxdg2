import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllGroupChats
from config import BOT_TOKEN
from database import Database
from localization import load_translations
from middlewares import DatabaseMiddleware
from handlers import start, game, profile, language, shop, welcome

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    db = Database("wox_mafia.db")
    await db.init()
    load_translations()

    dp.update.middleware(DatabaseMiddleware(db))

    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(shop.router)
    dp.include_router(game.router)
    dp.include_router(profile.router)
    dp.include_router(welcome.router)

    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Начать"),
            BotCommand(command="profile", description="Профиль"),
            BotCommand(command="shop", description="Магазин"),
            BotCommand(command="language", description="Сменить язык"),
            BotCommand(command="help", description="Помощь"),
        ],
        scope=BotCommandScopeDefault()
    )

    await bot.set_my_commands(
        commands=[
            BotCommand(command="game", description="Начать регистрацию"),
            BotCommand(command="leave", description="Покинуть игру"),
            BotCommand(command="profile", description="Профиль"),
            BotCommand(command="help", description="Помощь"),
        ],
        scope=BotCommandScopeAllGroupChats()
    )

    print("Wox Mafia запущен!")
    await dp.start_polling(
        bot,
        allowed_updates=["message", "callback_query", "pre_checkout_query", "my_chat_member"]
    )

if __name__ == "__main__":
    asyncio.run(main())
