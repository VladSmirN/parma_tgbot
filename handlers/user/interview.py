from aiogram import types
from states.user import FormInterview
from aiogram.dispatcher import FSMContext
import keyboards


async def bot_interview(query: types.CallbackQuery, callback_data: dict, bot):
    """
    Callback for for the beginning of the form
    """
    txt = [
        'Пожалуйста ответьте на вопросы.',
        'Ваше ФИО:',
    ]
    await FormInterview.name.set()
    await bot.send_message(query['from']['id'], text='\n'.join(txt),reply_markup=keyboards.default.MainMenu.cancel())
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

    await FormInterview.next()
    txt = [
        'Спасибо!',
        'Запрос отправлен HR. Скоро придет отклик.',
    ]
    print(data)
    await state.finish()
    await bot.send_message(query['from']['id'],
                           text='\n'.join(txt),
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
