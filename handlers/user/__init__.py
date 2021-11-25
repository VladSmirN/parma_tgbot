from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from .help import bot_help
from .start import bot_start
from .vacancy import bot_vacancy_list, bot_vacancy
from .interview import bot_interview
import functools
from keyboards.inline import vacancy_cb, to_interview_cb


def callback(func, **kwargs):
    @functools.wraps(func)
    def wrapper(*a, **k):
        return functools.partial(func, **kwargs)(*a, **k)
    return wrapper


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(bot_vacancy_list, text=['Список вакансий'], state="*")
    dp.register_callback_query_handler(callback(bot_vacancy, bot=dp.bot), vacancy_cb.filter())
    dp.register_callback_query_handler(callback(bot_interview, bot=dp.bot), to_interview_cb.filter())

