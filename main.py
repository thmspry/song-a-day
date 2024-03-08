from google_sheet_api import GoogleSheetApi
import os
from dotenv import load_dotenv, find_dotenv
import random

import sys
sys.path.append('model')
from Song import Song

import json

def get_songs_already_used() -> list:
    with open("already_used.json", "r") as openfile:
        already_used = json.load(openfile)
    return list(already_used)

def save_new_song(song: Song, already_used: list[str]):
    already_used.append(song.spotify_id)
    with open("already_used.json", "w") as outfile:
        json.dump(already_used, outfile)

def choose_song(songs: list[Song], already_used: list[str]) -> Song:
    song_already_used = True
    song_of_the_day = None
    while song_already_used:
        song_of_the_day = random.choice(songs)
        song_otd_id = song_of_the_day.spotify_id
        if song_otd_id not in already_used:
            return song_of_the_day
    return song_of_the_day

def create_json_file_if_not_exit():
    file_path = "already_used.json"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            data = []
            json.dump(data, file)
            
if __name__ == '__main__':
    create_json_file_if_not_exit()
    
    already_used_list = get_songs_already_used()
        
    load_dotenv(find_dotenv())
    API_KEY = os.environ.get("API_KEY")
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
    
    gs_api = GoogleSheetApi(API_KEY)
    songs: list[Song] = gs_api.request(SPREADSHEET_ID, "Requested", "A1", "H215")
    
    song_of_the_day = choose_song(songs, already_used_list)
    
    if song_of_the_day is None:
        print("Toutes les musiques ont été utilisées.")
        print("Il faut ajouter de nouvelles musiques dans le Google Sheet.")
        exit(0)
        
    print("La musique du jour est :", song_of_the_day)
    save_new_song(song_of_the_day, already_used_list)
    song_of_the_day.download_mp3()
    
    # génération de la vidéo
    
    # publication sur les réseaux sociaux