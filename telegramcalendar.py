from telebot import types
import calendar

def create_calendar(year,month):
    markup = types.InlineKeyboardMarkup()
    #First row - Month and Year
    row=[]
    row.append(types.InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data="ignore"))
    markup.row(*row)
    #Second row - Week Days
    week_days=["M","T","W","R","F","S","U"]
    row=[]
    for day in week_days:
        row.append(types.InlineKeyboardButton(day,callback_data="ignore"))
    markup.row(*row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(types.InlineKeyboardButton(" ",callback_data="ignore"))
            else:
                row.append(types.InlineKeyboardButton(str(day),callback_data="calendar-day-"+str(day)))
        markup.row(*row)
    #Last row - Buttons
    row=[]
    row.append(types.InlineKeyboardButton("<",callback_data="previous-month"))
    row.append(types.InlineKeyboardButton(" ",callback_data="ignore"))
    row.append(types.InlineKeyboardButton(">",callback_data="next-month"))
    markup.row(*row)
    return markup
