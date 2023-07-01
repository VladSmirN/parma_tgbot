from .consts import DefaultConstructor


class MainMenu(DefaultConstructor):
    @staticmethod
    def main_menu():
        schema = [1,1,1,1]
        actions = [
            'Учить слова',
            'Пройти тест',
            'Прочитать текст',
            'Мой профиль',
        ]
        return MainMenu._create_kb(actions, schema)

    @staticmethod
    def cancel():
        schema = [1]
        actions = [
            'Закрыть'
        ]
        return MainMenu._create_kb(actions, schema)
