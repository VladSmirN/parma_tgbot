from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo
db = BaseMongo.get_data_base()

async def bot_word_learning(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):

    topic = await db.Topics.find_one({"order": int(callback_data['order'])})
    word = await db.Contents_dictionaries.find_one({"id_Topic": topic['_id']})

    txt = f'Eng: {word["Name"]} \nRus: {word["Translate"]}'

    photo = open(f'images/{topic["order"]}.jpg', 'rb')

    await bot.send_photo(query['from']['id'] , photo,  caption=txt)

