from aiogram import types
from utils.misc import rate_limit


@rate_limit(5, 'help')
async def bot_help(msg: types.Message):
    text = [
        'Взаимодействие с ботом полностью основано на кнопках. '
        'Вам не нужно использовать какие-либо команды',
        'Для связи с разработчиками:',
        'https://t.me/rgbvpn'
    ]
    await msg.answer('\n'.join(text))
