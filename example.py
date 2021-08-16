import pytba_calendar
import telebot
from datetime import datetime

bot = telebot.TeleBot('YOU_API_TOKEN')


"""
The following function will listen to the presses of most of the calendar buttons
The arguments of the function are the bot object, declared earlier, and the language
in which the names of the months and days of the week in the calendar will be indicated
Supported languages - 'ru' and 'en'
"""
pytba_calendar.callback_listener(bot, 'en')


"""Here's a simple example of adding a calendar using the /calendar command"""

@bot.message_handler(commands=['calendar'])
def calendar_command(message):
    chat_id = message.chat.id
    cal = pytba_calendar.Calendar('en') # Here, the language must also be passed to the Сalendar class attribute
    calendar_markup = cal.get_calendar()
    bot.send_message(chat_id, 'Choose a date', reply_markup=calendar_markup)


"""
If you want to change the timezone use the following example. 
The list of time zones you can find on wikipedia https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
"""

@bot.message_handler(commands=['calendar'])
def calendar_command(message):
    chat_id = message.chat.id
    cal = pytba_calendar.Calendar('en') # Here, the language must also be passed to the Сalendar class attribute
    cal.time_zone = 'Europe/Moscow' # Here we change the time zone
    calendar_markup = cal.get_calendar()
    bot.send_message(chat_id, 'Choose a date', reply_markup=calendar_markup)

"""
The only thing you need to take care of is tracking button clicks with the required date and the back button.

Clicking the date button returns a callback like this – 'selected_date:YYYY-MM-DD'
Clicking the 'Back' button only returns such a callback — 'get_back_from_dateselect'

How to use
"""

"""First option: all button presses are processed within one function"""

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    data = call.data
    message_text = call.message.text
    message_id = call.message.id
    chat_id = call.message.chat.id
    if data.split(':')[0] == 'selected_date': # Catching the click of the date button
        date = datetime.strptime(data.split(':')[1], "%Y-%m-%d")
        # Here you can do whatever you want with the received date
    elif data == 'get_back_from_dateselect':
        # Here you have to decide for yourself what to do when the
        # user clicks the "back" button. As an example, you can simply edit
        # the message and remove all buttons.
        bot.edit_message_text(message_text, chat_id, message_id)


"""The second option: pressing of each button is listening in each function separately"""

@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == 'selected_date')
def selected_date_call(call):
    data = call.data
    chat_id = call.message.chat.id
    date = datetime.strptime(data.split(':')[1], "%Y-%m-%d")
    # Here you can do whatever you want with the received date. For example, you can send the date back
    bot.send_message(chat_id, f'Selected date: {date}')


@bot.callback_query_handler(func=lambda call: call.data == 'get_back_from_dateselect')
def get_back_call(call):
    message_text = call.message.text
    message_id = call.message.id
    chat_id = call.message.chat.id
    # Here you have to decide for yourself what to do when the
    # user clicks the "back" button. As an example, you can simply edit
    # the message and remove all buttons.
    bot.edit_message_text(message_text, chat_id, message_id)
