#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""


from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import datetime
import calendar

def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None, month=None, from_date=None, to_date=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """

    if from_date > to_date:
        raise ValueError('`from_date` must not be greater than `to_date`')

    now = datetime.datetime.now()

    if from_date is not None:
        from_day = from_date.day
    else:
        from_day = None

    if to_date is not None:
        to_day = to_date.day
    else:
        to_day = None

    if year is None:
        if from_date is not None:
            year = from_date.year
        else:
            year = now.year

    if month is None:
        if from_date is not None:
            month = from_date.month
        else:
            month = now.month

    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(' ',callback_data=data_ignore))
            elif year == from_date.year and month == from_date.month and day < from_day:
                row.append(InlineKeyboardButton(' ', callback_data=data_ignore))
            elif year == to_date.year and month == to_date.month and day > to_day:
                row.append(InlineKeyboardButton(' ', callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)
    #Last row - Buttons
    row=[]

    prev_month_last_date = datetime.datetime(year=year, month=month, day=1) - datetime.timedelta(days=1)
    if prev_month_last_date < from_date:
        prev_month_button_content, prev_month_callback_data = ' ', data_ignore
    else:
        prev_month_button_content, prev_month_callback_data = '<', create_callback_data('PREV-MONTH', year, month, day)

    if month < 12:
        next_month_first_date = datetime.datetime(year=year, month=month + 1, day=1)
    else:
        next_month_first_date = datetime.datetime(year=year + 1, month=1, day=1)
    if next_month_first_date < from_date:
        next_month_button_content, next_month_callback_data = ' ', data_ignore
    else:
        next_month_button_content, next_month_callback_data = '>', create_callback_data('NEXT-MONTH', year, month, day)

    row.append(InlineKeyboardButton(prev_month_button_content,callback_data=prev_month_callback_data))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(next_month_button_content,callback_data=next_month_callback_data))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(bot, update, from_date=None, to_date=None):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = update.callback_query
    (action,year,month,day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)
    elif action == "DAY":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(pre.year), int(pre.month), from_date=from_date, to_date=to_date))
    elif action == "NEXT-MONTH":
        if curr.month < 12:
            ne = datetime.datetime(year=year, month=curr.month + 1, day=1)
        else:
            ne = datetime.datetime(year=year + 1, month=1, day=1)

        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year), int(ne.month), from_date=from_date, to_date=to_date))
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
