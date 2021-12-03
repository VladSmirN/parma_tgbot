from aiogram import types

from .consts import InlineConstructor
from .callbacks import vacancy_cb, to_interview_cb, date_cb


class Users(InlineConstructor):
    @staticmethod
    def vacancy_list(vacancy_list):
        schema = []
        actions = []
        for Vacancy in vacancy_list:
            actions.append({'text': Vacancy['name'], 'callback_data': vacancy_cb.new(order=Vacancy['order'])})
            schema.append(1)
        return Users._create_kb(actions, schema)

    @staticmethod
    def to_interview(vacancy_order):
        schema = [1]
        actions = [
            {'text': 'Пройти собеседование',
             'callback_data': to_interview_cb.new(order=vacancy_order)}]
        return Users._create_kb(actions, schema)

    @staticmethod
    def date_list(date_list):
        schema = []
        actions = []
        for date in date_list:
            actions.append({'text': date, 'callback_data': date_cb.new(date=date)})
            schema.append(1)
        return Users._create_kb(actions, schema)
