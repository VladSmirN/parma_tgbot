from aiogram import types

from utils.misc import rate_limit


@rate_limit(5, 'help')
async def bot_help(msg: types.Message):
    text = [
        'Взаимодействие с ботом основано на кнопках.'
        'Для связи с разработчиками:',
        'https://t.me/rgbvpn',
        'https://t.me/VladSmirN'
    ]
    await msg.answer('\n'.join(text))
