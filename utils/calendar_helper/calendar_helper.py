import datetime as dt
import asyncio
from functools import wraps, partial
from os import environ
from O365 import Account


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


class CalendarHelper:

    def __init__(self):
        self._account = Account(credentials=(environ['CLIENT_ID'], environ['SECRET_ID']),
                                auth_flow_type='credentials', tenant_id=environ['TENANT_ID'])

    @async_wrap
    def __get_schedule(self, hr_email):
        return self._account.schedule(resource=hr_email)

    @async_wrap
    def __get_calendar(self, schedule):
        return schedule.get_default_calendar()

    @async_wrap
    def __new_query(self, calendar):
        query = calendar.new_query('start').greater_equal(dt.datetime.today())
        query.chain('and').on_attribute('end').less_equal(dt.datetime.today() + dt.timedelta(days=8))
        return query

    @async_wrap
    def __auth(self):
        self._account.authenticate()

    @async_wrap
    def __get_events(self, calendar, query):
        return calendar.get_events(query=query)

    @async_wrap
    def __get_event(self, calendar, event_id):
        return calendar.get_event(event_id)

    @async_wrap
    def __event_save(self, event):
        event.save()

    async def weekly_free_time(self, hr_email):
        """
        Get weekly free time in Outlook calendar.
        :param hr_email: Provide the email of the person whose events you want to receive.
        :return: List of events with event.subject = 'Свободное время'.
        """
        if not self._account.is_authenticated:
            await self.__auth()
        schedule = await self.__get_schedule(hr_email)
        calendar = await self.__get_calendar(schedule)
        query = await self.__new_query(calendar)
        return [event for event in await self.__get_events(calendar, query) if event.subject == 'Свободное время']

    async def update_event(self, hr_email, event_id, new_subject):
        """
        Updates an existing event by its ID.
        :param hr_email: Provide an email of the person whose event you want to update.
        :param event_id: ID of event.
        :param new_subject: A new subject of event that will replace the old one.
        :return:
        """
        if not self._account.is_authenticated:
            await self.__auth()
        schedule = await self.__get_schedule(hr_email)
        calendar = await self.__get_calendar(schedule)
        event = await self.__get_event(calendar, event_id)
        event.subject = new_subject
        await self.__event_save(event)
