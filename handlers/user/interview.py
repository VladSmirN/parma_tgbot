from aiogram import types
from states.user import FormInterview
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo
from utils.calendar_helper import CalendarHelper


async def bot_interview(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    """
    Callback for for the beginning of the form
    """

    async with state.proxy() as data:
        data['vacancy_order'] = int(callback_data['order'])

    txt = [
        'Пожалуйста, ответьте на вопросы.',
        'Введите ФИО.',
    ]

    await FormInterview.name.set()
    await bot.send_message(query['from']['id'], text='\n'.join(txt), reply_markup=keyboards.default.MainMenu.cancel())
    await query.answer()

async def process_name_invalid(message: types.Message):
    """
    Callback for invalid name
    """
    return await message.reply("Ваш ФИО некорректный (пример - Иван Иванов Иванович).\nПожалуйста, введите еще раз.")

async def process_name(message: types.Message, state: FSMContext):
    """
    Callback for name processing
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await FormInterview.next()
    await message.reply("Какой у Вас номер телефона? (пример - 9981234567)")


async def process_phone_invalid(message: types.Message):
    """
    Callback for invalid phone
    """
    return await message.reply("Ваш телефон некорректный (пример - 9981234567).\nКакой у Вас номер телефона?")


async def process_phone(message: types.Message, state: FSMContext):
    """
    Callback for phone processing
    """
    async with state.proxy() as data:
        data['phone'] = message.text

    await FormInterview.next()
    await message.reply("Какой у Вас email?")


async def process_email_invalid(message: types.Message):
    """
    Callback for invalid email
    """
    return await message.reply("Ваш email некорректный.\nКакой у Вас email?")


async def process_email(message: types.Message, state: FSMContext):
    """
    Callback for email processing
    """
    async with state.proxy() as data:
        data['email'] = message.text

    await FormInterview.next()
    await message.reply("Отправьте ссылку на Ваше резюме.")


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

    await message.reply("Почему Вас заинтересовала эта вакансия?")


async def process_motivation_invalid(message: types.Message):
    """
    Callback for invalid motivation
    """
    return await message.reply("Вы написали слишком длинный текст, нужно уложиться в 256 символов.\nПожалуйста, введите еще раз.")


async def process_motivation(message: types.Message, state: FSMContext):
    """
    Callback to process a message with motivation
    """

    await FormInterview.next()
    async with state.proxy() as data:
        data['motivation'] = message.text

        date_list = []
        db = BaseMongo.get_data_base()
        vacancy = await db.Vacancies.find_one({"order": int(data['vacancy_order'])})
        hr = await db.HR.find_one({"telegram_id": vacancy['hr_telegram_id']})
        calendar_helper = CalendarHelper()
        weekly_free_time = await calendar_helper.weekly_free_time(hr['email_outlook'])
        data['email_outlook'] = hr['email_outlook']

        if not weekly_free_time:
            await state.finish()
            await message.reply('К сожалению, у HR сейчас '
                                'нет свободного времени, попробуйте отправить отклик в другое время',
                                reply_markup=keyboards.default.MainMenu.main_menu()
                                )
            return

        for index, event in enumerate(weekly_free_time):
            from datetime import timezone, timedelta
            new_dt = event.start.astimezone(timezone(timedelta(hours=5)))
            day = new_dt.strftime("%d/%m")
            start_time = new_dt.strftime("%H:%M")
            time_string = f'{day} в {start_time} (UTC+5, Екатеринбург)'
            date_list.append({'date_str': time_string, 'id_event': index})
            data[f'date_str_{index}'] = time_string
            data[f'outlook_{index}'] = event.object_id
        kb = keyboards.inline.Users.date_list(date_list)
        await message.reply("Выберите дату для собеседования", reply_markup=kb)


async def process_date(query: types.CallbackQuery, callback_data: dict, bot, state: FSMContext):
    """
    Callback for handling a date button
    """

    db = BaseMongo.get_data_base()

    async with state.proxy() as data:

        date_str = data[f'date_str_{callback_data["id"]}']
        email_outlook = data['email_outlook']
        id_event_outlook = data[f'outlook_{callback_data["id"]}']
        calendar_helper = CalendarHelper()
        await calendar_helper.update_event(email_outlook, id_event_outlook, "На рассмотрении")

        txt_to_user = [
            'Спасибо!',
            'Запрос отправлен HR. Скоро придет отклик.',
        ]

        vacancy = await db.Vacancies.find_one({"order": int(data['vacancy_order'])})
        username_telegram = 'не указан'
        if 'username' in query['from']:
            username_telegram = query['from']['username']
        result = await db.ApplicationForm.insert_one({
            "hr_telegram_id": vacancy['hr_telegram_id'],
            "name": data['name'],
            "phone": data['phone'],
            "email": data['email'],
            "resume": data['resume'],
            "motivation": data['motivation'],
            "date": date_str,
            "vacancy_order": data['vacancy_order'],
            "vacancy_name": vacancy['name'],
            "username_telegram": username_telegram,
            "user_telegram_id": query['from']['id'],
            "status": "waiting",
            'id_event_outlook': id_event_outlook
        })

        txt_to_hr = [
            'Новый отклик!',
            'Вакансия: ' + vacancy['name'],
            'Username пользователя: ' + username_telegram,
            'ФИО в анкете: ' + data['name'],
            'Телефон: ' + data['phone'],
            'Email: ' + data['email'],
            'Резюме: ' + data['resume'],
            'Почему выбрал эту вакансию: ' + data['motivation'],
            'Выбраная дата: ' + date_str,
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
