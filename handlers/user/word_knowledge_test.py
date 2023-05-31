from aiogram import types
from states.user import FormInterview
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo
from utils.calendar_helper import CalendarHelper
from bson.objectid import ObjectId
db = BaseMongo.get_data_base()
from bson.timestamp import Timestamp
import datetime as dt
import random
async def bot_word_knowledge_test(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    """
    Callback  for the beginning of the form test
    """
    topic = await db.Topics.find_one({"order": int(callback_data['order'])})

    #find priority word

    """
    TODO : тут выбор слова ,котрое давно выбирали и у которого высокий приотритет 
    """

    word = await db.Contents_dictionaries.find_one({"id_Topic": topic['_id']})

    # find choose words
    words = []
    for word_choose in await db.Contents_dictionaries.find({'order': {'$lt': 10}}).to_list(length=10):
        if word_choose["_id"] == word["_id"]:
            continue
        if len(words)>2:
            break
        if random.random() > 0.5:
            words.append(word_choose)
    midpoint = random.randint(0, 3)
    words = words[0:midpoint] + [word] + words[midpoint:]

    async with state.proxy() as data:
        data['id_word'] = word['_id']

    txt = [
        f'Пожалуйста, выберите перевод слова -{word["Name"]}.'
    ]
    print()
    kb = keyboards.inline.Users.word_list(words)
    await bot.send_message(query['from']['id'], reply_markup=kb, text='\n'.join(txt))
    await query.answer()


async def bot_word_knowledge_test_end(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    async with state.proxy() as data:

        choose_word = await db.Contents_dictionaries.find_one({"order": int(callback_data['order'])})
        user = await db.Users.find_one({"telegram_id": query['from']['id']})
        priority = 0
        if data['id_word'] != choose_word['_id']:
            priority = 1
            txt = [
                f'Ответ не верный (.'
            ]
        else:
            txt = [
                f'Ответ верный, отличный результат.'
            ]
            priority = 0

        old_dictionary = await db.Dictionary.find_one({"id_word": data['id_word'], "id_user": user["_id"]})

        if old_dictionary is None:
            await db.Dictionary.insert_one({
                "id_word": data['id_word'],
                "id_user": user["_id"],
                "date": dt.datetime.now(),
                "priority": priority
            })
        else:
            await db.Dictionary.update_one({'_id': old_dictionary['_id']}, {'$set': {'date': dt.datetime.now(),
                                                                                     "priority": priority}})


        await state.finish()
        await bot.send_message(query['from']['id'],
                               text='\n'.join(txt),
                               reply_markup=keyboards.default.MainMenu.main_menu())
