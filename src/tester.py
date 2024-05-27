
import time

text = '15:00-11:30'

start_time = text.split('-')[0]
end_time = text.split('-')[1]

# if len(start_time) != 4 or len(end_time) != 4:
#     print('good len')


try:
  valid_start_time = time.strptime(start_time, '%H:%M')
  valid_end_time = time.strptime(end_time, '%H:%M')
  print(valid_start_time < valid_end_time)
except ValueError:
  print('Invalid date!')