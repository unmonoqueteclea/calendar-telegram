#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#

from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove




def create_options_keyboard(options, cancel_msg):
    """
    Create an options keyboard with one line featuring each option
    """
    rows = []
    for i,op in enumerate(options):
        rows.append([InlineKeyboardButton(op,callback_data="CHOSEN;"+str(i))])
    if cancel_msg is not None:
        rows.append([InlineKeyboardButton(cancel_msg,callback_data="CANCEL;0")])
    return InlineKeyboardMarkup(rows)


def process_option_selection(bot, update):
    query = update.callback_query
    data = update.callback_query.data
    action, index = data.split(";")
    ret_data = (False,None)
    if action == "CHOSEN":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            )
        ret_data = True, int(index)
    elif action == "CANCEL":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = False, 0
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
    return ret_data