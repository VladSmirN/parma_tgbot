from aiogram import types
from loguru import logger
from aiogram.dispatcher import FSMContext


async def bot_start(msg: types.Message, state: FSMContext):

    logger.info(f"/start HR user_id={msg.from_user.id}")
    await msg.answer(f'Привет, {msg.from_user.full_name}! Ожидайте откликов.')


