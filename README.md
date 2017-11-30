# Calendar for Telegram Bots
A simple inline calendar for Telegram bots written in Python using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot). Based on [calendar-telegram](https://github.com/unmonoqueteclea/calendar-telegram).
## Description
The file **telegramcalendar.py** proved the API to create an [inline keyboard](https://core.telegram.org/bots/2-0-intro) for a Telegram Bot. The user can either select a date or move to the next or previous month by clicking a singe button.

## Internals
The file **telegramcalendar.py** provides the user with two methods:
* **create_calendar**: This method returns a InlineKeyboardMarkup object with the calendar in the provided year and month.
* **process_calendar_selection:** This method can be used inside a CallbackQueryHandler method to check if the user has selected a date or wants to move to a different month. It also creates a new calendar with the same text if necessary.

An example of the usage of these two methods is shown in *bot_example.py*.
## Usage
To use the telecram-calendar-keyboard you need to have [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) installed first.


## Demo
![](https://github.com/grcanosa/telegram-calendar-keyboard/blob/master/example.gif)
