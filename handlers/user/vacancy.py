from aiogram import types
from utils.db.mongo import BaseMongo
import keyboards
import keyboards.default
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
db = BaseMongo.get_data_base()


async def bot_vacancy_list(msg: types.Message):
    txt = [
        'Выберите подходящую вакансию.'
    ]
    vacancies_list = []

    for Vacancies in await db.Vacancies.find({'order': {'$lt': 100}}).sort('order').to_list(length=100):
        vacancies_list.append(Vacancies)

    kb = keyboards.inline.Users.vacancy_list(vacancies_list)
    await msg.answer('\n'.join(txt), reply_markup=kb, reply=not msg.chat.type == 'private')


async def bot_vacancy(query: types.CallbackQuery, callback_data: dict, bot):
    vacancy = await db.Vacancies.find_one({"order": int(callback_data['order'])})
    kb = keyboards.inline.Users.to_interview(int(callback_data['order']))
    await bot.send_message(query['from']['id'], reply_markup=kb, text='\n'.join(vacancy['description']))
    await query.answer()
