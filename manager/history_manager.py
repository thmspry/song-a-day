import json

import manager.file_manager as file_man

from model.Song import Song

HISTORY_PATH = "./database/history.json"

def get_history() -> list[dict]:
    __create_json_file_if_not_exist__()
    with open(HISTORY_PATH, "r") as openfile:
        history = json.load(openfile)
    return list(history)

def save_new_song(song: Song) -> None:
    history = get_history()
    history.append(song.to_json_history())
    with open(HISTORY_PATH, "w") as outfile:
        json.dump(history, outfile)
        
def reset_history() -> None:
    if file_man.file_exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as outfile:
            json.dump([], outfile)
    else:
        __create_json_file_if_not_exist__()
        
def __create_json_file_if_not_exist__() -> None:
    file_path = HISTORY_PATH
    if not file_man.file_exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)
            