from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import asyncio, random
from keyboards import join_game_kb, vote_kb
from roles import Role, ROLE_KEYS, get_roles_for_player_count
from localization import get_text
from config import BOT_USERNAME

router = Router()
games = {}

class Game:
    def __init__(self, chat_id, creator_id):
        self.chat_id = chat_id
        self.creator_id = creator_id
        self.players = {}
        self.state = "registration"
        self.round_num = 0
        self.night_actions = {}
        self.day_votes = {}

    def add_player(self, uid, name):
        if uid not in self.players:
            self.players[uid] = {"name": name, "alive": True, "role": None}
            return True
        return False

    def assign_roles(self):
        roles = get_roles_for_player_count(len(self.players))
        random.shuffle(roles)
        for (uid, data), role in zip(self.players.items(), roles):
            data["role"] = role

    def alive_players(self):
        return [(uid, d["name"]) for uid, d in self.players.items() if d["alive"]]

    def get_role(self, uid):
        return self.players.get(uid, {}).get("role")

    def kill(self, uid):
        if uid in self.players:
            self.players[uid]["alive"] = False

    def check_win(self):
        mafia = sum(1 for d in self.players.values() if d["alive"] and d["role"] in (Role.DON, Role.MAFIA))
        maniac = sum(1 for d in self.players.values() if d["alive"] and d["role"] == Role.MANYAK)
        town = sum(1 for d in self.players.values() if d["alive"] and d["role"] not in (Role.DON, Role.MAFIA, Role.MANYAK, Role.SAMOUBIYTSA))
        if mafia == 0 and maniac == 0: return "town"
        if mafia >= town + maniac: return "mafia"
        if maniac >= town + mafia: return "maniac"
        return None

@router.message(Command("game"))
async def cmd_game(message: Message, db):
    chat_id = message.chat.id
    if chat_id in games and games[chat_id].state != "ended": return
    if message.chat.type == "private":
        await message.answer("Эту команду нужно писать в групповом чате.")
        return
    await db.create_user(message.from_user.id, message.from_user.full_name)
    lang = await db.get_language(message.from_user.id)
    game = Game(chat_id, message.from_user.id)
    game.add_player(message.from_user.id, message.from_user.full_name)
    games[chat_id] = game
    await message.answer(get_text(lang, "registration_open"), reply_markup=join_game_kb())

@router.callback_query(F.data == "join_game")
async def cb_join(callback: CallbackQuery, db):
    chat_id = callback.message.chat.id
    game = games.get(chat_id)
    if not game or game.state != "registration":
        await callback.answer("Регистрация закрыта.", show_alert=True)
        return
    if callback.from_user.id in game.players:
        await callback.answer("Ты уже в игре.", show_alert=True)
        return
    await callback.answer(
        text="Переходим в бота для подтверждения...",
        url=f"https://t.me/{BOT_USERNAME}?start=join_{chat_id}"
    )

@router.message(Command("leave"))
async def cmd_leave(message: Message, db):
    chat_id = message.chat.id
    game = games.get(chat_id)
    if not game:
        await message.answer("Игра не идёт.")
        return
    if message.from_user.id in game.players and game.state == "registration":
        del game.players[message.from_user.id]
        await message.answer(f"❌ {message.from_user.full_name} покинул игру.")
    else:
        await message.answer("Нельзя выйти сейчас.")

@router.message(Command("start"))
async def cmd_start_game(message: Message, db):
    chat_id = message.chat.id
    game = games.get(chat_id)
    if not game: return
    lang = await db.get_language(message.from_user.id)
    if message.from_user.id != game.creator_id:
        await message.answer(get_text(lang, "only_creator")); return
    if len(game.players) < 4:
        await message.answer(get_text(lang, "need_players")); return
    game.assign_roles()
    game.state = "night"
    game.round_num = 1
    for uid, data in game.players.items():
        try:
            ul = await db.get_language(uid)
            role = data["role"]
            rn = get_text(ul, ROLE_KEYS[role])
            desc = get_text(ul, f"desc_{role.value}")
            await message.bot.send_message(uid, get_text(ul, "role_your", role=rn, desc=desc), parse_mode="HTML")
        except Exception: pass
    cl = await db.get_language(game.creator_id)
    await message.answer(get_text(cl, "night_start", round=game.round_num))

@router.callback_query(F.data.startswith("vote_"))
async def cb_vote(callback: CallbackQuery, db):
    chat_id = callback.message.chat.id
    game = games.get(chat_id)
    lang = await db.get_language(callback.from_user.id)
    if not game or game.state != "voting":
        await callback.answer(get_text(lang, "vote_not_time")); return
    if not game.players.get(callback.from_user.id, {}).get("alive"):
        await callback.answer(get_text(lang, "vote_dead")); return
    target = int(callback.data.split("_")[1]) if callback.data != "vote_skip" else None
    game.day_votes[callback.from_user.id] = target
    await callback.answer(get_text(lang, "vote_accepted"))
