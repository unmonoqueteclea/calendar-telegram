#!/usr/bin/python3

import logging

from telegram.ext import Updater
from telegram.ext import  CallbackQueryHandler
from telegram.ext import  CommandHandler
from telegram import  ReplyKeyboardRemove


import telegramcalendar


TOKEN = ""


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def calendar_handler(bot,update):
    update.message.reply_text("Please select a date: ",
                        reply_markup=telegramcalendar.create_calendar())


def inline_handler(bot,update):
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="You selected %s" % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())


if TOKEN == "":
    print("Please write TOKEN into file")
else:
    up = Updater("TOKEN")

    up.dispatcher.add_handler(CommandHandler("calendar",calendar_handler))
    up.dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    up.start_polling()
    up.idle()
