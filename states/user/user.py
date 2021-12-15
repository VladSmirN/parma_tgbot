from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenu(StatesGroup):
    main_menu = State()
    vacancy_list = State()
    job_invitations = State()
    interview_results = State()
    setting = State()


class FormInterview(StatesGroup):
    name = State()
    phone = State()
    email = State()
    resume = State()
    motivation = State()
    date = State()
