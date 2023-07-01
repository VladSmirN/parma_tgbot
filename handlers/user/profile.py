from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards
from utils.db.mongo import BaseMongo
db = BaseMongo.get_data_base()
import datetime as dt
async def bot_profile(msg: types.Message):



    user = await db.Users.find_one({"telegram_id": msg.from_user.id})

    count_learning_word = 0
    async for _ in  db.Learning_statistics.find({"id_user": user["_id"]}) :
        count_learning_word += 1
    # print(count_learning_word)

    count_text_test = 0
    count_true_text_test = 0
    async for text_test in  db.Text_tests_statistics.find({"id_user": user["_id"]}) :
        count_text_test +=1
        if text_test["status"]==1:
            count_true_text_test +=1
    # print(count_text_test ,count_true_text_test )

    count_word_test = 0
    count_true_word_test = 0
    async for word_test in  db.Dictionary.find({"id_user": user["_id"]}) :
        count_word_test +=1
        if word_test["status"] == 1:
            count_true_word_test += 1
    # print(count_word_test ,count_true_word_test)

    txt = ['Информация о тебе:',
           f'ты изучил со мной {count_learning_word} слов,',
           f'ответил на {count_true_word_test} из {count_word_test} тестов правильно, ',
           f'прочитал  {count_text_test} текст и дал {count_true_text_test} из {count_text_test} правильный ответ ',
            "Супер! Продолжай учиться дальше."
           ]

    await msg.answer('\n'.join(txt))

