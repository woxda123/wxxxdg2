from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORTED_LANGS, BOT_USERNAME

LANG_NAMES = {
    "ru":"🇷🇺 Русский","en":"🇬🇧 English","uk":"🇺🇦 Українська","be":"🇧🇾 Беларуская",
    "kk":"🇰🇿 Қазақша","uz":"🇺🇿 O'zbekcha","de":"🇩🇪 Deutsch","fr":"🇫🇷 Français",
    "es":"🇪🇸 Español","it":"🇮🇹 Italiano","pt":"🇵🇹 Português","tr":"🇹🇷 Türkçe",
    "pl":"🇵🇱 Polski","cs":"🇨🇿 Čeština","sk":"🇸🇰 Slovenčina","hu":"🇭🇺 Magyar",
    "ro":"🇷🇴 Română","bg":"🇧🇬 Български","sr":"🇷🇸 Srpski","hr":"🇭🇷 Hrvatski",
    "nl":"🇳🇱 Nederlands","sv":"🇸🇪 Svenska","no":"🇳🇴 Norsk","da":"🇩🇰 Dansk",
    "fi":"🇫🇮 Suomi","el":"🇬🇷 Ελληνικά",
}

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить игру в чат", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="open_langs")],
    ])

def join_game_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Присоединиться", callback_data="join_game")]
    ])

def vote_kb(players: list):
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"vote_{pid}")] for pid, name in players]
    buttons.append([InlineKeyboardButton(text="⏭ Пропустить", callback_data="vote_skip")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def profile_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить камни", callback_data="shop_gems")],
        [InlineKeyboardButton(text="💰 Купить деньги", callback_data="shop_money")],
        [InlineKeyboardButton(text="🏆 Статистика", callback_data="stats")],
    ])

def language_kb():
    buttons, row = [], []
    for code in SUPPORTED_LANGS:
        row.append(InlineKeyboardButton(text=LANG_NAMES.get(code, code), callback_data=f"lang_{code}"))
        if len(row) == 2:
            buttons.append(row); row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def shop_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить камни", callback_data="shop_gems")],
        [InlineKeyboardButton(text="💰 Купить деньги", callback_data="shop_money")],
    ])

GEM_PACKAGES = [(1,20),(5,90),(10,165),(15,225),(30,400),(50,580)]
MONEY_PACKAGES = [(10000,20),(55000,90),(120000,165),(200000,225),(450000,400),(800000,580)]

def gems_kb():
    buttons = []
    for gems, stars in GEM_PACKAGES:
        buttons.append([InlineKeyboardButton(
            text=f"💎 {gems} = {stars} ⭐",
            callback_data=f"buy_gems_{gems}_{stars}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="shop_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def money_kb():
    buttons = []
    for money, stars in MONEY_PACKAGES:
        text = f"💰 {money:,} = {stars} ⭐".replace(",", " ")
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"buy_money_{money}_{stars}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="shop_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
