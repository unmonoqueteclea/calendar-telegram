#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""


from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove)
from telegram.error import BadRequest
import datetime
import calendar


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join(["CALENDAR", action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")[1:]


def create_calendar(year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the
                     current year is used.
    :param int month: Month to use in the calendar, if None the
                      current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    thismonth = False
    if year is None:
        year = now.year
    if month is None:
        month = now.month
        thismonth = True
    elif month == now.month:
        thismonth = True
    today = now.day
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    # First row - Month and Year (and prev, next button)
    row = []
    if not thismonth:
        row.append(InlineKeyboardButton("<",
                                        callback_data=create_callback_data(
                                            "PREV-MONTH", year, month, 0)))
    else:
        row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),
                                    callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",
                                    callback_data=create_callback_data(
                                        "NEXT-MONTH", year, month, 0)))
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    valid_week = False
    for week in my_calendar:
        row = []
        for day in week:
            if(day == 0):
                row.append(InlineKeyboardButton(" ",
                                                callback_data=data_ignore))
            elif(thismonth and (day < today)):
                row.append(InlineKeyboardButton(" ",
                                                callback_data=data_ignore))
            else:
                if not valid_week:
                    valid_week = True
                row.append(InlineKeyboardButton(str(day),
                           callback_data=create_callback_data(
                                                "DAY", year, month, day)))
        if valid_week:  # only append rows that have dates in them for readability
            keyboard.append(row)
    # Last row - user's input choice
    row = []
    row.append(InlineKeyboardButton("Freitextfeld, bitte!",
                                    callback_data=create_callback_data(
                                        "USER-INPUT", year, month, 0)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(update, context):
    """
    Process the callback_query. This method generates a new calendar if
    forward or backward is pressed. This method should be called inside
    a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the
                                   CallbackQueryHandler
    :return: Returns a triplet (Boolean,datetime.datetime,Boolean), indicating
             if a date is selected and returning the date if so or if the user
             wants to write it himself.
    """
    ret_data = (False, None, False)
    query = update.callback_query
    (action, year, month, day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        keyboard = []
        row = []
        row.append(InlineKeyboardButton("Nächster Spieleabend: " + str(day) +
                                        "/" + str(month) + "/" + str(year),
                                        callback_data=create_callback_data(
                                            "IGNORE", year, month, day)))
        keyboard.append(row)
        context.bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(keyboard))
        ret_data = True, datetime.datetime(
                            int(year), int(month), int(day)), False
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        context.bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(
                                  int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        context.bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(
                                  int(ne.year), int(ne.month)))
    elif action == "USER-INPUT":
        try:
            context.bot.delete_message(query.message.chat_id, query.message.message_id)
        except BadRequest:
            pass
        ret_data = (True, None, True)
    else:
        context.bot.answer_callback_query(callback_query_id=query.id,
                                  text="Something went wrong!")
        # UNKNOWN
    return ret_data
