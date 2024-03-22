from fastapi import FastAPI, HTTPException
import random

import manager.history_manager as hist_m
import manager.env_manager as env_m
import manager.file_manager as file_m
from api.google_sheet_api import GoogleSheetApi
import api.song_downloader as song_dl
import utils

from Song import Song

app = FastAPI()

# CONSTANTS
BASE_MAPPING = "/api/"
SONG_MAPPING = BASE_MAPPING + "song/"

def __choose_song__(songs: list[Song], history: list[dict]) -> Song:
    history = map(lambda song: song["id"], history)
    unused_songs = list(filter(lambda song: song.spotify_id not in history, songs))

    if len(unused_songs) == 0:
        raise Exception("Toutes les musiques ont été utilisées. Il faut ajouter de nouvelles musiques dans le Google Sheet.")

    return random.choice(unused_songs)


# ENVIRONMENT
@app.get(BASE_MAPPING + "env")
def load_env() -> dict:
    try:
        return env_m.load_env()
    except Exception as e:
        return {"msg": e}

# SONG
@app.get(SONG_MAPPING + "random")
def random_song(api_key: str, spreadsheet_id: str) -> dict:
    gs_api = GoogleSheetApi(api_key)
    try:
        songs: list[Song] = gs_api.request(spreadsheet_id, "Requested", "A1", "J215")
        history = hist_m.get_history()
        song_of_the_day = __choose_song__(songs, history)
        hist_m.save_new_song(song_of_the_day)
        return song_of_the_day.to_json()
    except Exception as e:
        msg_err = e.args[0]
        raise HTTPException(status_code=400, detail=msg_err)

@app.get(SONG_MAPPING + "download")
def download_song(spotify_id: str) -> dict:
    song_download_path = song_dl.SONG_PATH
    try:
        file_m.remove_file(song_download_path)
        song_dl.download_mp3(spotify_id)
        return {"audio": utils.encode_audio_to_base64(song_download_path)}
    except Exception as e:
        msg_err = e.args[0]
        raise HTTPException(status_code=400, detail=msg_err)

    
    

# HISTORY
@app.get(BASE_MAPPING + "history")
def history() -> dict:
    history = hist_m.get_history()
    return history

@app.delete(BASE_MAPPING + "history", status_code=204)
def del_history() -> None:
    hist_m.reset_history()
