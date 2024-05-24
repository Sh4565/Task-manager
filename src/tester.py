import calendar
from pprint import pprint
from datetime import datetime

fg = calendar.Calendar()

calendar_list = []
week_list = []

for date in fg.itermonthdates(datetime.now().year, datetime.now().month):
    week_list.append(date.day)
    # Добавляем неделю в список, когда она полная (7 дней)
    if len(week_list) == 7:
        calendar_list.append(week_list)
        week_list = []

# Добавляем оставшиеся дни последней недели, если есть
if week_list:
    calendar_list.append(week_list)

pprint(calendar_list)
