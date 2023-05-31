from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from .help import bot_help
from .start import bot_start
from .about_company import about_company
from .vacancy import bot_vacancy_list, bot_vacancy
from .interview import *
import functools
from keyboards.inline import *
from states.user import FormInterview
import re

regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_url = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
regex_fio = r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?'


def callback(func, **kwargs):
    @functools.wraps(func)
    def wrapper(*a, **k):
        return functools.partial(func, **kwargs)(*a, **k)
    return wrapper


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(bot_vacancy_list, text=['Запомнить слово'], state="*")
    dp.register_message_handler(about_company, text=['О компании'], state="*")
    dp.register_callback_query_handler(callback(bot_vacancy, bot=dp.bot), vacancy_cb.filter())
    dp.register_callback_query_handler(callback(bot_interview, bot=dp.bot), to_interview_cb.filter())
    dp.register_message_handler(cancel_handler, text=['Закрыть'], state="*")
    dp.register_message_handler(process_name_invalid,
                                lambda message: not re.fullmatch(regex_fio, message.text) or not len(message.text) <= 128,
                                state=FormInterview.name)
    dp.register_message_handler(process_name,
                                lambda message: re.fullmatch(regex_fio, message.text) and len(message.text) <= 128,
                                state=FormInterview.name)
    dp.register_message_handler(process_phone_invalid,
                                lambda message: not message.text.isdigit() or not len(message.text) == 10,
                                state=FormInterview.phone)
    dp.register_message_handler(process_phone,
                                lambda message:  message.text.isdigit() and len(message.text) == 10,
                                state=FormInterview.phone)
    dp.register_message_handler(process_email_invalid,
                                lambda message: not re.fullmatch(regex_email, message.text),
                                state=FormInterview.email)
    dp.register_message_handler(process_email,
                                lambda message: re.fullmatch(regex_email, message.text),
                                state=FormInterview.email)
    dp.register_message_handler(process_resume_invalid,
                                lambda message: not re.fullmatch(regex_url, message.text),
                                state=FormInterview.resume)
    dp.register_message_handler(process_resume,
                                lambda message: re.fullmatch(regex_url, message.text),
                                state=FormInterview.resume)
    dp.register_message_handler(process_motivation_invalid,
                                lambda message: not len(message.text) <= 256,
                                state=FormInterview.motivation)
    dp.register_message_handler(process_motivation,
                                lambda message: len(message.text) <= 256,
                                state=FormInterview.motivation)
    dp.register_callback_query_handler(callback(process_date, bot=dp.bot), date_cb.filter(), state=FormInterview.date)
