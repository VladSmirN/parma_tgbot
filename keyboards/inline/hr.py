from aiogram import types

from .consts import InlineConstructor
from .callbacks import select_status_cb


class HR():
    @staticmethod
    def select_status(application_form):
        buttons = [types.InlineKeyboardButton(text='Принять',
                                              callback_data=select_status_cb.new(status="accepted",
                                                                                 application_form=application_form)),
                   types.InlineKeyboardButton(text='Отказать',
                                              callback_data=select_status_cb.new(status="deny",
                                                                                 application_form=application_form))
                   ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        return keyboard
