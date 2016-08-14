# Calendar for Telegram Bots
A simple inline calendar for Telegram bots written in Python using pyTelegramBotAPI
## Description
The file **telegramcalendar.py** creates a calendar view for Telegram Bots that uses [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). It creates an [inline keyboard](https://core.telegram.org/bots/2-0-intro) that lets the user execute one action when clicking one of its buttons.
Furthermore, the user can change the month displayed in the inline keyboard simply clicking in one button.
## Demo
![](https://github.com/unmonoqueteclea/calendar-telegram/blob/master/example.gif)
## Usage
In order to use **pyTelegramBotAPI** you will have to install it. The easiest way of doing it is with pip:
```bash
pip install pyTelegramBotAPI
```
To use this keyboard in your bot, only copy the file **telegramcalendar.py** to yout project.
Then you have to pass the object that returns the *create_calendar* function to the *send_message* function of pyTelegramBotAPI.
> **WARNING** The configuration of the bot doesn´t appear in these snippets. In order to see a complete bot working with this > > library you can see the **bot.py** file.

```python
from telegramcalendar import create_calendar
current_shown_dates={}
@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Please, choose a date", reply_markup=markup)
```
There are two more functions that you have to write in your code in order to let the user change the displayed month;
```python
@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

```
If we want to do something when the user clicks on one day, we should write the following code. The **date** variable will contain the date choosen by the user.
```python
@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        bot.send_message(chat_id, str(date))
        bot.answer_callback_query(call.id, text="")

    else:
        #Do something to inform of the error
        pass

```
