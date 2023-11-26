import micloud
from time import sleep
import os
counter = 0

username = os.getenv("XIA_USER", "")
login = os.getenv("XIA_PASS", "")


def create_app():
    global counter
    while True:
        if counter == 0:
            counter += 1

        sleep(1)


# cloud = micloud.MiCloud(username, login)


# def download_tokens():
#     cloud.login()
#     tokken = cloud.get_token()
#     print(tokken)
#     with open('tokken.txt', 'w') as f:
#         f.write(tokken)
