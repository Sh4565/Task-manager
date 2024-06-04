import pytz
import datetime

# Текущая дата и время в UTC
current_time_UTC = datetime.datetime.now(pytz.utc)

# Дата и время в формате строки
date_str = current_time_UTC.strftime("%Y-%m-%d")
time_str = '14:34'
datetime_str = f'{date_str} {time_str}'

# Временная зона 'Europe/Kiev'
timezone = pytz.timezone('Europe/Kiev')

# Парсинг строки с датой и временем в объект datetime
string_time_Kiev = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

# Локализация времени в нужную временную зону
string_time_Kiev = timezone.localize(string_time_Kiev)

# Преобразование во временную зону UTC
string_time_utc = string_time_Kiev.astimezone(pytz.utc)

print(current_time_UTC.strftime("%H:%M"))
print(string_time_utc.strftime("%H:%M"))
