
import time

from aiogram.types import User


spamers = {}


async def its_spam(user: User):

    spamers[user.id] = time.time()
    # try:
    #     spamers[user.id] = time.time()
    #     print('1', spamers)
    # except KeyError:
    #     pass
    print(time.time() - spamers[user.id])
    print('2', spamers)

    if time.time() - spamers[user.id] == 5:
        pass

