from aiogram import types

from .consts import InlineConstructor
from .callbacks import *


class Users():
    @staticmethod
    def topics_test_list(vacancy_list):
        buttons = []
        for Vacancy in vacancy_list:
            buttons.append(types.InlineKeyboardButton(text=Vacancy['Name'],
                                                      callback_data=topic_test_cb.new(order=Vacancy['order'])))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard
    @staticmethod
    def topics_learning_list(vacancy_list):
        buttons = []
        for Vacancy in vacancy_list:
            buttons.append(types.InlineKeyboardButton(text=Vacancy['Name'],
                                                      callback_data=topic_learning_cb.new(order=Vacancy['order'])))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    @staticmethod
    def topics_test_text_list(vacancy_list):
        buttons = []
        for Vacancy in vacancy_list:
            buttons.append(types.InlineKeyboardButton(text=Vacancy['Name'],
                                                      callback_data=topic_text_test_cb.new(order=Vacancy['order'])))
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

    def text_answer_list(word_list_):
        buttons = []
        for id,word in enumerate(word_list_):
            buttons.append(types.InlineKeyboardButton(text=f'{id+1}',
                                                      callback_data=text_answer_cb.new(order=id+1)))
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

