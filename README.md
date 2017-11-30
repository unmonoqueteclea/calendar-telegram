# Calendar for Telegram Bots
A simple inline calendar for Telegram bots written in Python using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot). Based on [calendar-telegram](https://github.com/unmonoqueteclea/calendar-telegram).
## Description
The file **telegramcalendar.py** proved the API to create an [inline keyboard](https://core.telegram.org/bots/2-0-intro) for a Telegram Bot. The user can either select a date or move to the next or previous month by clicking a singe button.
## Demo
![](https://github.com/grcanosa/telegram-calendar-keyboard/blob/master/example.gif)
## Internals
The file **telegramcalendar.py** provides the user with two methods:
* *create_calendar*: This method returns a InlineKeyboardMarkup object with the calendar in the provided year and month.
* *process_calendar_selection:* This method can be used inside a CallbackQueryHandler method to check if the user has selected a date or wants to move to a different month. It also creates a new calendar with the same text if necessary.

An example of the usage of these two methods is shown in *bot_example.py*.
## Usage
To use the telecram-calendar-keyboard you need to have [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) installed first.
In order to use **pyTelegramBotAPI** you will have to install it. The easiest way of doing it is with pip:
```bash
pip install pyTelegramBotAPI
```
To use this keyboard in your bot, only copy the file **telegramcalendar.py** to yout project.
Then you have to pass the object that returns the *create_calendar* function to the *send_message* function of pyTelegramBotAPI.
> **WARNING** The configuration of the bot doesn´t appear in these snippets. In order to see a complete bot working with this > > library you can see the **bot.py** file.
