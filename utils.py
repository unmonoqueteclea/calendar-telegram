def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def reformat_persian_date(date: str) -> str:
    return date\
        .replace('یکشنبه', 'یک‌شنبه')\
        .replace('سه شنبه', 'سه‌شنبه')\
        .replace('پنجشنبه', 'پنج‌شنبه')