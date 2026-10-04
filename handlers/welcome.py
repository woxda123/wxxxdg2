from aiogram import Router
from aiogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER

router = Router()

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def on_bot_promoted(event: ChatMemberUpdated):
    await event.answer(
        "🙏 Спасибо что сделал админом!\n\n"
        "Теперь я могу:\n"
        "• Удалять сообщения ночью\n"
        "• Блокировать чат во время игры\n"
        "• Банить нарушителей\n\n"
        "Напиши /game чтобы начать!"
    )

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def on_bot_added(event: ChatMemberUpdated):
    await event.answer(
        "🎭 <b>Привет! Я Wox Mafia</b> — бот-ведущий для игры в Мафию.\n\n"
        "Я помогу вам играть в классическую Мафию прямо в этом чате:\n\n"
        "🎭 13 ролей (Дон, Мафия, Комиссар, Доктор, Маньяк и другие)\n"
        "🌙 Ночные действия и дневное голосование\n"
        "👤 Профили, статистика и магазин\n"
        "🌍 26 языков\n\n"
        "<b>Как начать:</b>\n"
        "1. Сделай меня администратором (чтобы я мог управлять чатом ночью)\n"
        "2. Напиши /game\n"
        "3. Игроки нажимают «Присоединиться»\n"
        "4. Создатель пишет /start\n\n"
        "👇 <b>Сделай меня админом, чтобы всё работало корректно:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🛡 Сделать админом",
                url=f"https://t.me/{event.bot.username}?startgroup=true&admin=delete_messages+restrict_members+pin_messages+invite_users"
            )]
        ]),
        parse_mode="HTML"
    )
