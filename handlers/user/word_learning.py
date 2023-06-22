from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo
db = BaseMongo.get_data_base()
import datetime as dt
async def bot_word_learning(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):

    topic = await db.Topics.find_one({"order": int(callback_data['order'])})
    word = await db.Contents_dictionaries.find_one({"id_Topic": topic['_id']})
    user = await db.Users.find_one({"telegram_id": query['from']['id']})

    learning_statistics = await db.Learning_statistics.find_one({"id_word": word['_id'], "id_user": user["_id"]})
    if  learning_statistics == None:
        await db.Learning_statistics.insert_one({
            "id_word": word['_id'],
            "id_user": user["_id"],
            "date": dt.datetime.now()
        })


    txt = f'Eng: {word["Name"]} \nRus: {word["Translate"]}'

    photo = open(f'images/{topic["order"]}.jpg', 'rb')

    await bot.send_photo(query['from']['id'] , photo,  caption=txt)

