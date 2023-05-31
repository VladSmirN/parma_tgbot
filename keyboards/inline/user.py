from aiogram import types

from .consts import InlineConstructor
from .callbacks import topic_cb, to_interview_cb, date_cb, word_cb


class Users():
    @staticmethod
    def topics_list(vacancy_list):
        buttons = []
        for Vacancy in vacancy_list:
            buttons.append(types.InlineKeyboardButton(text=Vacancy['Name'],
                                                      callback_data=topic_cb.new(order=Vacancy['order'])))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard
    def word_list(word_list_):
        buttons = []
        for word in word_list_:
            buttons.append(types.InlineKeyboardButton(text=word['Translate'],
                                                      callback_data=word_cb.new(order=word['order'])))
        keyboard = types.InlineKeyboardMarkup(row_width=2)
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
            buttons.append(types.InlineKeyboardButton(text=date['date_str'],
                                                      callback_data=date_cb.new(id=date['id_event'])))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

