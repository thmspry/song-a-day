import json
import os
import sys

import utils

sys.path.append(os.path.join(os.path.dirname(__file__), "model"))

from Song import Song

def get_songs_already_used() -> list:
    __create_json_file_if_not_exist__()
    with open("already_used.json", "r") as openfile:
        already_used = json.load(openfile)
    return list(already_used)

def save_new_song(song: Song, already_used: list):
    already_used.append(song.to_json())
    with open("already_used.json", "w") as outfile:
        json.dump(already_used, outfile)
        
def reset_songs_already_used():
    if utils.__file_exists__("already_used.json"):
       with open("already_used.json", "w") as outfile:
            json.dump([], outfile)
    else:
        __create_json_file_if_not_exist__()
def __create_json_file_if_not_exist__():
    file_path = "already_used.json"
    if not utils.__file_exists__(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)
            