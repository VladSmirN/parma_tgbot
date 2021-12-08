from aiogram import types

from .consts import InlineConstructor
from .callbacks import vacancy_cb, to_interview_cb, date_cb


class Users():
    @staticmethod
    def vacancy_list(vacancy_list):
        buttons = []
        for Vacancy in vacancy_list:
            buttons.append(types.InlineKeyboardButton(text=Vacancy['name'],
                                                      callback_data=vacancy_cb.new(order=Vacancy['order'])))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    @staticmethod
    def to_interview(vacancy_order):
        buttons = [types.InlineKeyboardButton(text='Пройти собеседование',
                                              callback_data=to_interview_cb.new(order=vacancy_order))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    @staticmethod
    def date_list(date_list):
        buttons = []
        for date in date_list:
            buttons.append(types.InlineKeyboardButton(text=date,
                                                      callback_data=date_cb.new(date=date)))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard
