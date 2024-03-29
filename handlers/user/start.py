from aiogram import types
from contextlib import suppress
from utils.db.mongo import BaseMongo
from loguru import logger
import keyboards
from aiogram.dispatcher import FSMContext
import keyboards.default
import states.user


async def bot_start(msg: types.Message, bot , state: FSMContext):
    db = BaseMongo.get_data_base()
    user = await db.Users.find_one({
        "telegram_id": msg.from_user.id
    })

    if not user:
        result = await db.Users.insert_one({
            "telegram_id": msg.from_user.id,
            "first_name": msg.from_user.first_name,
            "last_name": msg.from_user.last_name,
            "username": msg.from_user.username
        })
        logger.info(
            f"/start user_id={msg.from_user.id} insert_one result={result.acknowledged} id={result.inserted_id}")

        txt = [f'Привет, {msg.from_user.full_name}! Это чат-бот EngLearn. Я буду твоим помощником в изучении английкого языка!',
               'Со мной ты можешь:',
               f'изучать новые слова по категория, ',
               f'проходить тестирование по изученным словам,',
               'читать тексты, в которых есть изучаемые тобой слова и отвечать на вопросы по ним'
               ]
        photo = open(f'images/start.jpg', 'rb')
        await bot.send_photo(msg.from_user.id, photo, caption='\n'.join(txt))


    await msg.answer(f'Главное меню', reply_markup=keyboards.default.MainMenu.main_menu())

