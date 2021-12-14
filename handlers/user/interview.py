from aiogram import types
from states.user import FormInterview
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo

async def bot_interview(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    """
    Callback for for the beginning of the form
    """

    async with state.proxy() as data:
        data['vacancy_order'] = int(callback_data['order'])

    txt = [
        'Пожалуйста ответьте на вопросы.',
        'Ваше ФИО:',
    ]

    await FormInterview.name.set()
    await bot.send_message(query['from']['id'], text='\n'.join(txt), reply_markup=keyboards.default.MainMenu.cancel())
    await query.answer()


async def process_name(message: types.Message, state: FSMContext):
    """
    Callback for name processing
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await FormInterview.next()
    await message.reply("Какой у вас номер телефона? (пример - 9981234567)")


async def process_phone_invalid(message: types.Message):
    """
    Callback for invalid phone
    """
    return await message.reply("Ваш телефон некорректный (пример - 9981234567).\nКакой у вас номер телефона?")


async def process_phone(message: types.Message, state: FSMContext):
    """
    Callback for phone processing
    """
    async with state.proxy() as data:
        data['phone'] = message.text

    await FormInterview.next()
    await message.reply("Какой у вас email?")


async def process_email_invalid(message: types.Message):
    """
    Callback for invalid email
    """
    return await message.reply("Ваш email некорректный.\nКакой у вас email?")


async def process_email(message: types.Message, state: FSMContext):
    """
    Callback for email processing
    """
    async with state.proxy() as data:
        data['email'] = message.text

    await FormInterview.next()
    await message.reply("Отправьте ссылку на ваше резюме.")


async def process_resume_invalid(message: types.Message):
    """
    Callback for invalid resume
    """
    return await message.reply("Ваша ссылка некорректная.\nОтправьте ссылку на ваше резюме.")


async def process_resume(message: types.Message, state: FSMContext):
    """
    Callback for resume processing
    """
    async with state.proxy() as data:
        data['resume'] = message.text

    await FormInterview.next()


    await message.reply("Почему вас заинтересовала эта вакансия?")


async def process_motivation(message: types.Message, state: FSMContext):
    """
    Callback to process a message with motivation
    """
    async with state.proxy() as data:
        data['motivation'] = message.text

    await FormInterview.next()
    kb = keyboards.inline.Users.date_list(['01.01.2000', '02.01.2000', '02.01.2000'])
    await message.reply("Выбирите дату для собеседования", reply_markup=kb)


async def process_date(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    """
    Callback for handling a date button
    """
    async with state.proxy() as data:
        data['date'] = callback_data['date']

    txt_to_user = [
        'Спасибо!',
        'Запрос отправлен HR. Скоро придет отклик.',
    ]

    db = BaseMongo.get_data_base()

    vacancy = await db.Vacancies.find_one({"order": int(data['vacancy_order'])})

    result = await db.ApplicationForm.insert_one({
        "hr_telegram_id": vacancy['hr_telegram_id'],
        "name": data['name'],
        "phone": data['phone'],
        "email": data['email'],
        "resume": data['resume'],
        "motivation": data['motivation'],
        "date": data['date'],
        "vacancy_order": data['vacancy_order'],
        "vacancy_name": vacancy['name'],
        "username_telegram": query['from']['username'],
        "user_telegram_id": query['from']['id'],
        "status": "waiting"
    })

    txt_to_hr = [
        'Новый отклик!',
        'Вакансия: ' + vacancy['name'],
        'Username пользователя: ' + query['from']['username'],
        'ФИО в анкете: ' + data['name'],
        'Телефон: ' + data['phone'],
        'Email: ' + data['email'],
        'Резюме: ' + data['resume'],
        'Почему выбрал эту вакансию: ' + data['motivation'],
        'Выбраная дата: ' + data['date'],
    ]
    await bot.send_message(vacancy['hr_telegram_id'],
                           text='\n'.join(txt_to_hr),
                           reply_markup=keyboards.inline.HR.select_status(result.inserted_id))

    await state.finish()
    await bot.send_message(query['from']['id'],
                           text='\n'.join(txt_to_user),
                           reply_markup=keyboards.default.MainMenu.main_menu())
    await query.answer()


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await message.reply('Форма заркыта.', reply_markup=keyboards.default.MainMenu.main_menu())
