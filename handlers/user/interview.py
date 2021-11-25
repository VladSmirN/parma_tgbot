from aiogram import types


async def bot_interview(query: types.CallbackQuery, callback_data: dict, bot):
    txt = ['Овтетьте на вопросы.']
    await bot.send_message(query['from']['id'], text='\n'.join(txt))
