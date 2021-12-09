from aiogram import Dispatcher
from .start import *
import functools
from filters.is_hr import HRFilter


def callback(func, **kwargs):
    @functools.wraps(func)
    def wrapper(*a, **k):
        return functools.partial(func, **kwargs)(*a, **k)
    return wrapper


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, HRFilter())


