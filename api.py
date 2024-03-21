from fastapi import FastAPI, HTTPException
import random

import history_manager as hist_m
import env_manager as env_m
from google_sheet_api import GoogleSheetApi

from Song import Song

app = FastAPI()
BASE_MAPPING = "/api/"

def choose_song(songs: list[Song], already_used: list) -> Song:
    already_used = map(lambda song: song["id"], already_used)
    unused_songs = list(filter(lambda song: song.spotify_id not in already_used, songs))

    if not unused_songs:
        raise Exception("Toutes les musiques ont été utilisées. Il faut ajouter de nouvelles musiques dans le Google Sheet.")

    return random.choice(unused_songs)

@app.get(BASE_MAPPING + "env")
def load_env():
    try:
        return env_m.load_env()
    except Exception as e:
        return {"msg": e}

@app.get(BASE_MAPPING + "random-song")
def random_song(api_key: str, spreadsheet_id: str):
    gs_api = GoogleSheetApi(api_key)
    try:
        songs: list[Song] = gs_api.request(spreadsheet_id, "Requested", "A1", "J215")
        al_us = hist_m.get_songs_already_used()
        song_of_the_day = choose_song(songs, al_us)
        hist_m.save_new_song(song_of_the_day, al_us)
        return song_of_the_day.to_json()
    except Exception as e:
        msg_err = e.args[0]
        raise HTTPException(status_code=400, detail=msg_err)

@app.get(BASE_MAPPING + "history")
def history():
    history = hist_m.get_songs_already_used()
    return history

@app.delete(BASE_MAPPING + "history", status_code=204)
def del_history():
    hist_m.reset_songs_already_used()
