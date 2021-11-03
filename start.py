import os
from os import path

def dir_check_make(directory):
    if not (path.isdir(directory)):
        os.mkdir(directory)
        print(f"created {directory}")
    else:
        print(f"{directory} already exists")


# def ensure_config():
#     os.environ["BOT_TOKEN"] = 