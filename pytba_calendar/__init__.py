from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from pytz import timezone
from .config import *
import calendar

class Calendar:

    def __init__(self, language):
        self.language = language

    time_zone = 'UTC'
    current_datetime = datetime.now(timezone(time_zone))


    def _base_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 7
        markup.add(
            InlineKeyboardButton(
                MONTH_NAMES[self.language][self.current_datetime.month],
                callback_data=f'pytbacal_change_month:{self.current_datetime.year}'
            ),
            InlineKeyboardButton(
                str(self.current_datetime.year), callback_data=f'pytbacal_change_year:{self.current_datetime.month}:{self.current_datetime.year}')
        )
        weekday_buttons = []
        for weekday in WEEKDAYS[self.language]:
            weekday_buttons.append(InlineKeyboardButton(WEEKDAYS[self.language][weekday], callback_data=f'pytbacal_weekday:{weekday}'))
        markup.add(*weekday_buttons)
        return markup

    def _get_delta(self):
        return self.current_datetime.day - 1

    def _get_first_day_weekday(self):
        return self.current_datetime - timedelta(days=self._get_delta())

    def get_calendar(self):
        markup = self._base_markup()
        month_range = calendar.monthrange(self.current_datetime.year, self.current_datetime.month)[1]
        buttons = []
        counter = 0
        month_day = 1
        first_week_day = self._get_first_day_weekday().weekday()
        for weekday in range(0, first_week_day):
            if counter == 6:
                counter = 0
            else:
                counter += 1
            buttons.append(InlineKeyboardButton('⠀', callback_data='pytbacal_empty_space'))
        for weekday in range(month_day, month_range + 1):
            if counter == 6:
                counter = 0
            else:
                counter += 1
            buttons.append(InlineKeyboardButton(str(month_day), callback_data=f'selected_date:{self.current_datetime.year}-{self.current_datetime.month}-{month_day}'))
            month_day += 1
        if counter != 0:
            for i in range(counter, 7):
                buttons.append(InlineKeyboardButton('⠀', callback_data='pytbacal_empty_space:'))
        markup.add(*buttons)
        markup.add(
            InlineKeyboardButton('←', callback_data=f'pytbacal_previous_month:{self.current_datetime.month}:{self.current_datetime.year}'),
            InlineKeyboardButton(GET_BACK_BUTTON[self.language], callback_data='get_back_from_dateselect'),
            InlineKeyboardButton('→', callback_data=f'pytbacal_next_month:{self.current_datetime.month}:{self.current_datetime.year}')
        )
        return markup

    def get_months(self, year):
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        buttons = []
        for month in MONTH_NAMES[self.language]:
            buttons.append(
                InlineKeyboardButton(MONTH_NAMES[self.language][month], callback_data=f'pytbacal_selected_month:{month}:{year}')
            )
        markup.add(*buttons)
        return markup

    def get_years(self, year, month):
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        buttons = []
        for i in range(year - 4, year + 5):
            buttons.append(
                InlineKeyboardButton(str(i), callback_data=f'pytbacal_selected_year:{i}:{month}')
            )
        markup.add(*buttons)
        markup.add(
            InlineKeyboardButton('←', callback_data=f'pytbacal_previous_years:{year - 9}:{month}'),
            InlineKeyboardButton('→', callback_data=f'pytbacal_next_years:{year + 9 }:{month}')
        )
        return markup


def callback_listener(bot, language):
    @bot.callback_query_handler(func=lambda call: call.data.split(':')[0] in CALLBACKS)
    def call_listener(call):
        message_text = call.message.text
        message_id = call.message.id
        chat_id = call.message.chat.id
        data = call.data
        cal = Calendar(language)
        data_part = data.split(':')[0]
        if data_part == 'pytbacal_change_month':
            year = data.split(':')[1]
            markup = cal.get_months(year)
            bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)
        elif data_part == 'pytbacal_change_year':
            month = int(data.split(':')[1])
            year = int(data.split(':')[2])
            markup = cal.get_years(year, month)
            bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)
        elif data_part == 'pytbacal_weekday':
            weekday = int(data.split(':')[1])
            bot.answer_callback_query(call.id, WEEKDAY_NAMES[language][weekday])
        elif data_part == 'pytbacal_empty_space':
            bot.answer_callback_query(call.id, '⠀')
        elif data_part in ['pytbacal_previous_month', 'pytbacal_next_month']:
            current_month = int(data.split(':')[1])
            current_year = int(data.split(':')[2])
            if data_part == 'previous_month':
                if current_month == 1:
                    month = 12
                    year = current_year - 1
                else:
                    month = current_month - 1
                    year = current_year
            else:
                if current_month == 12:
                    month = 1
                    year = current_year + 1
                else:
                    month = current_month + 1
                    year = current_year
            new_datetime = datetime.strptime(f'{year}-{month}-01 00:00:00', "%Y-%m-%d %H:%M:%S")
            cal.current_datetime = new_datetime
            markup = cal.get_calendar()
            bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)
        elif data_part in ['pytbacal_previous_years', 'pytbacal_next_years']:
            year = int(data.split(':')[1])
            month = int(data.split(':')[2])
            markup = cal.get_years(year, month)
            bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)
        elif data_part == 'pytbacal_selected_year':
            year = int(data.split(':')[1])
            month = int(data.split(':')[2])
            new_datetime = datetime.strptime(f'{year}-{month}-01 00:00:00', "%Y-%m-%d %H:%M:%S")
            cal.current_datetime = new_datetime
            markup = cal.get_calendar()
            bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)
        elif data_part == 'pytbacal_selected_month':
            month = int(data.split(':')[1])
            year = int(data.split(':')[2])
            new_datetime = datetime.strptime(f'{year}-{month}-01 00:00:00', "%Y-%m-%d %H:%M:%S")
            cal.current_datetime = new_datetime
            markup = cal.get_calendar()
            bot.edit_message_text(message_text, chat_id, message_id, reply_markup=markup)
