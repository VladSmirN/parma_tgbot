from aiogram import Dispatcher
from .start import *
from .application_form import *
import functools
from filters.is_hr import HRFilter
from keyboards.inline import *


def callback(func, **kwargs):
    @functools.wraps(func)
    def wrapper(*a, **k):
        return functools.partial(func, **kwargs)(*a, **k)
    return wrapper


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, HRFilter())
    dp.register_callback_query_handler(callback(change_status, bot=dp.bot), select_status_cb.filter())


