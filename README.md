# Date Selection tool for Telegram Bots
A simple inline calendar for Telegram bots written in Python using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot). Based on [calendar-telegram](https://github.com/unmonoqueteclea/calendar-telegram).
## Description
The file **telegramcalendar.py** proved the API to create an [inline keyboard](https://core.telegram.org/bots/2-0-intro) for a Telegram Bot. The user can either select a date or move to the next or previous month by clicking a singe button.

## Internals
The file **telegramcalendar.py** provides the user with two methods:
* **create_calendar**: This method returns a InlineKeyboardMarkup object with the calendar in the provided year and month.
* **process_calendar_selection:** This method can be used inside a CallbackQueryHandler method to check if the user has selected a date or wants to move to a different month. It also creates a new calendar with the same text if necessary.

## Usage
To use the telecram-calendar-keyboard you need to have [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) installed first. A full working example on how to use telegram-calendar-keyboard is provided in *bot_example.py*. As you can see below, you create a calendar and add it to a message with a *reply_markup* parameter and then you can process it in a callbackqueyhandler method using the *process_calendar_selection* method:
```python
def calendar_handler(bot,update):
    update.message.reply_text("Please select a date: ",
                        reply_markup=telegramcalendar.create_calendar())


def inline_handler(bot,update):
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="You selected %s" % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())
```

> For a more complex example please check out [renfe-notifier-bot](https://github.com/grcanosa/renfe-notifier-bot)

## Demo
![](https://github.com/grcanosa/telegram-calendar-keyboard/blob/master/example.gif)
