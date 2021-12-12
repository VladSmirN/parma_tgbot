from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db.mongo import BaseMongo


class HRFilter(BoundFilter):
    def __init__(self):
        self.db = BaseMongo.get_data_base()

    async def check(self, message: types.Message):
        hr = await self.db.HR.find_one({
            "telegram_id": message.from_user.id
        })

        if hr:
           return True
        else:
           return False

