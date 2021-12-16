from aiogram import types


async def about_company(msg: types.Message):
    txt = ['Российский разработчик ПО на основе современных информационных технологий',
           '<a>https://parma.team</a>',
           ]
    await msg.answer('\n'.join(txt))
