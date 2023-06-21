from aiogram import types
from utils.db.mongo import BaseMongo
import keyboards
import keyboards.default
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
db = BaseMongo.get_data_base()


async def bot_topics_list_test(msg: types.Message):
    txt = ['Выбери категорию, по какой хочешь пройти тест:']
    topics_list = []

    for topic in await db.Topics.find({'order': {'$lt': 10}}).sort('order').to_list(length=10):
        topics_list.append(topic)

    kb = keyboards.inline.Users.topics_test_list(topics_list)
    await msg.answer('\n'.join(txt), reply_markup=kb, reply=not msg.chat.type == 'private')

async def bot_topics_list_learning(msg: types.Message):
    txt = ['Выбери категорию, откуда хочешь изучать новое слово:.']
    topics_list = []

    for topic in await db.Topics.find({'order': {'$lt': 10}}).sort('order').to_list(length=10):
        topics_list.append(topic)

    kb = keyboards.inline.Users.topics_learning_list(topics_list)
    await msg.answer('\n'.join(txt), reply_markup=kb, reply=not msg.chat.type == 'private')


async def bot_topics_list_test_text(msg: types.Message):
    txt = ['Выбери категорию, по которой хотите прочитать текст и выбрать правильное утверждение:']
    topics_list = []

    for topic in await db.Topics.find({'order': {'$lt': 10}}).sort('order').to_list(length=10):
        topics_list.append(topic)

    kb = keyboards.inline.Users.topics_test_text_list(topics_list)
    await msg.answer('\n'.join(txt), reply_markup=kb, reply=not msg.chat.type == 'private')


async def bot_topic(query: types.CallbackQuery, callback_data: dict, bot):
    topic = await db.Topics.find_one({"order": int(callback_data['order'])})
    # kb = keyboards.inline.Users.to_interview(int(callback_data['order']))

    await bot.send_message(query['from']['id'],  text='\n'.join(topic['Name']))
    # await query.answer()
