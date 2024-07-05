
import os

with open('text.txt', 'r') as f:
    text = f.readlines()
    for i in text:
        i = i.split(' ')[0]
        if i not in 'CONTAINER':
            print(f'docker rm {i}')
            os.system(f'docker rm {i}')
