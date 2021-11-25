from .consts import DefaultConstructor


class MainMenu(DefaultConstructor):
    @staticmethod
    def main_menu():
        schema = [2]
        actions = [
            'Список вакансий',
            'О компании',
        ]
        return MainMenu._create_kb(actions, schema)

