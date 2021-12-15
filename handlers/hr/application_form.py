from aiogram import types
from loguru import logger
from utils.db.mongo import BaseMongo
from bson.objectid import ObjectId
from utils.calendar_helper import CalendarHelper


async def change_status(query: types.CallbackQuery, callback_data: dict, bot):

    db = BaseMongo.get_data_base()

    application_form = await db.ApplicationForm.find_one({'_id': ObjectId(callback_data['application_form'])})

    if not application_form or not application_form["hr_telegram_id"] == query.from_user.id:
        logger.info(f"/change_status HR user_id={query.from_user.id} . failure ")
        await query.answer()
        return

    hr = await db.HR.find_one({'telegram_id': query.from_user.id})

    application_form['status'] = callback_data['status']
    await db.ApplicationForm.replace_one({'_id': ObjectId(callback_data['application_form'])},
                                         application_form)



    txt_to_user_deny= [
        f'Здравствуйте, {application_form["name"]}!',
        f'Большое спасибо за интерес, проявленный к вакансии {application_form["vacancy_name"]}.',
        'К сожалению, в настоящий момент мы не готовы пригласить Вас на дальнейшее интервью по этой вакансии.',
        'Мы внимательно ознакомились с Вашим резюме, и, возможно, вернемся к Вашей кандидатуре, когда у нас возникнет такая потребность.',
        'С уважением,',
        f'{hr["fio"]}'

    ]

    txt_to_user_accepted = [
        f'Здравствуйте, {application_form["name"]}, нас заинтересовала ваша анкета.',
        'Ожидайте звонка от hr-специалиста в ближайшее время для подтверждения даты и места собеседования.',
        f'С уважением, {hr["fio"]}',
        f'{hr["phone"]}'
    ]

    txt_status = ''
    outlook_status = ''
    if callback_data['status'] == 'accepted':
        txt_status = '<b>Принято</b>'
        outlook_status = 'Занято'
        await bot.send_message(application_form["user_telegram_id"], text='\n'.join(txt_to_user_accepted),)

    if callback_data['status'] == 'deny':
        txt_status = '<b>Отказано</b>'
        outlook_status = 'Свободное время'
        await bot.send_message(application_form["user_telegram_id"], text='\n'.join(txt_to_user_deny))

    txt_to_hr = [
        txt_status,
        'Вакансия: ' + application_form['vacancy_name'],
        'Username пользователя: ' + application_form['username_telegram'],
        'ФИО в анкете: ' + application_form['name'],
        'Телефон: ' + application_form['phone'],
        'Email: ' + application_form['email'],
        'Резюме: ' + application_form['resume'],
        'Почему выбрал эту вакансию: ' + application_form['motivation'],
        'Выбраная дата: ' + application_form['date'],
    ]

    await bot.edit_message_text(chat_id=application_form["hr_telegram_id"],
                               message_id=int(query['message']['message_id']),
                               text='\n'.join(txt_to_hr))

    calendar_helper = CalendarHelper()
    await calendar_helper.update_event(hr['email_outlook'], application_form['id_event_outlook'], outlook_status)

    logger.info(f"/change_status HR user_id={query.from_user.id} . successfully")
    await query.answer()




