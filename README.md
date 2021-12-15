![CodeQL](https://github.com/VladSmirN/parma_tgbot/actions/workflows/codeql-analysis.yml/badge.svg)

___

Данный бот был разработан в ходе учебной практики в вузе, которую курировала [Parma](https://www.parma.ru/). Целью проекта является оптимизация работы HR. 

#### Основные разработчики
- [Смирнов Владислав](https://github.com/VladSmirN)
- [Калайда Даниил](https://github.com/challenger128)


### Почему вы должны выбрать нас?
- Заточен для удобства использования обычными пользователями.
- Полностью асинхронный, под копотом [aiogram](https://github.com/aiogram/aiogram), что значит он справится с высокой нагрузкой.
- Использован грамотный с точки зрения проектирования [шаблон](https://github.com/Forden/aiogram-bot-template) для создания масштабируемых ботов.
- Сохраняет в [MongoDB](https://www.mongodb.com/) и берет из неё JSON-подобные данные.
- Простота установки, мы позаботились о вас и подготовили необходимые докерфайлы.
- Имеет утилиту собственной разработки, которая работает с календарем Outlook. 
- Вашему HR не нужно будет договариваться о времени встречи, мы сделаем это за вас.

___

## Содержание
- [До установки](#до установки)
- [Установка](#установка)

## До установки

## Установка
```
git clone https://github.com/VladSmirN/aiogram-bot-template
cd /aiogram-bot-template
```

# Run Docker
Перед этим нужно создать файл ```.env```, внутри него указать токен. 
``` 
bot_token=your_token_here 
```

```
docker-compose up --build 
```
