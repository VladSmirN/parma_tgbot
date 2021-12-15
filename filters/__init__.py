from aiogram import Dispatcher

from .is_hr import HRFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(HRFilter)
