from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from keyboards import shop_main_kb, gems_kb, money_kb

router = Router()

@router.message(Command("shop"))
async def cmd_shop(message: Message, db):
    await db.create_user(message.from_user.id, message.from_user.full_name)
    await message.answer(
        "🛒 <b>Магазин Wox Mafia</b>\n\nОплата через Telegram Stars ⭐",
        reply_markup=shop_main_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "shop_gems")
async def cb_shop_gems(callback: CallbackQuery, db):
    await callback.message.edit_text(
        "💎 Какое кол-во камней вы хотите приобрести?\n\nОплата через Telegram Stars ⭐",
        reply_markup=gems_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "shop_money")
async def cb_shop_money(callback: CallbackQuery, db):
    await callback.message.edit_text(
        "💰 Какое кол-во денег вы хотите приобрести?\n\nОплата через Telegram Stars ⭐",
        reply_markup=money_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "shop_back")
async def cb_shop_back(callback: CallbackQuery, db):
    await callback.message.edit_text(
        "🛒 <b>Магазин Wox Mafia</b>\n\nОплата через Telegram Stars ⭐",
        reply_markup=shop_main_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy_gems_"))
async def cb_buy_gems(callback: CallbackQuery, db):
    _, _, gems, stars = callback.data.split("_")
    gems, stars = int(gems), int(stars)
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"💎 {gems} камней",
        description=f"Покупка {gems} камней в Wox Mafia",
        payload=f"gems_{gems}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"{gems} камней", amount=stars)],
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy_money_"))
async def cb_buy_money(callback: CallbackQuery, db):
    _, _, money, stars = callback.data.split("_")
    money, stars = int(money), int(stars)
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"💰 {money} денег",
        description=f"Покупка {money} денег в Wox Mafia",
        payload=f"money_{money}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"{money} денег", amount=stars)],
    )
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def on_successful_payment(message: Message, db):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    if payload.startswith("gems_"):
        gems = int(payload.split("_")[1])
        await db.add_gems(user_id, gems)
        await message.answer(f"✅ Оплата прошла! Начислено 💎 {gems} камней.")
    elif payload.startswith("money_"):
        money = int(payload.split("_")[1])
        await db.add_money(user_id, money)
        await message.answer(f"✅ Оплата прошла! Начислено 💰 {money} денег.")
