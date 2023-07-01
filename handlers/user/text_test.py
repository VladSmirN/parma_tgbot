from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo
import datetime as dt
db = BaseMongo.get_data_base()

async def bot_text_test(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    topic = await db.Topics.find_one({"order": int(callback_data['order'])})
    text_test = await db.Text_tests.find_one({"id_Topic": topic['_id']})

    txt = [
        f' {text_test["text"]}.',
        '',
        'Выберите верное утверждение:'
    ]
    for id, answer in enumerate(text_test["answers"]):
        txt.append(f'{id+1}) {answer}' )

    async with state.proxy() as data:
        data['id_text_test'] = text_test['_id']

    kb = keyboards.inline.Users.text_answer_list(text_test["answers"])

    await bot.send_message(query['from']['id'], reply_markup=kb, text='\n'.join(txt))
    await query.answer()

async def bot_text_test_end(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    async with state.proxy() as data:
        user = await db.Users.find_one({"telegram_id": query['from']['id']})
        text_test = await db.Text_tests.find_one({"_id": data['id_text_test']})

        if int(callback_data['order']) != int(text_test['correct_answer']):
            status = 0
            txt = [
                f'Ответ не верный (.'
            ]
        else:
            status = 1
            txt = [
                f'Ответ верный, отличный результат.'
            ]

        await db.Text_tests_statistics.insert_one({
            "id_text_test": text_test['_id'],
            "id_user": user["_id"],
            "date": dt.datetime.now(),
            "status": status,
            "choose": callback_data['order']
        })
        await state.finish()
        await bot.send_message(query['from']['id'],
                               text='\n'.join(txt),
                               reply_markup=keyboards.default.MainMenu.main_menu())

