from google_sheet_api import GoogleSheetApi
import os
from dotenv import load_dotenv, find_dotenv
import random

from Song import Song
from TikTokVideo import TikTokVideo

import video_editor as ve
import tiktok_publisher as tp

import json
import locale
import time

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def get_songs_already_used() -> list:
    create_json_file_if_not_exit()
    with open("already_used.json", "r") as openfile:
        already_used = json.load(openfile)
    return list(already_used)

def save_new_song(song: Song, already_used: list):
    already_used.append(song.to_json())
    with open("already_used.json", "w") as outfile:
        json.dump(already_used, outfile)

def choose_song(songs: list[Song], already_used: list[str]) -> Song:
    possible_songs = songs
    song_already_used = True
    song_of_the_day = None
    while song_already_used:
        if len(possible_songs) == 0:
            raise Exception("Toutes les musiques ont été utilisées.\nIl faut ajouter de nouvelles musiques dans le Google Sheet.")
        song_of_the_day = random.choice(possible_songs)
        song_otd_id = song_of_the_day.spotify_id
        if song_otd_id not in already_used:
            return song_of_the_day
        else:
            possible_songs.remove(song_of_the_day)

def create_json_file_if_not_exit():
    file_path = "already_used.json"
    if not file_exists(file_path):
        with open(file_path, 'w') as file:
            data = []
            json.dump(data, file)
    
def print_and_exit(message: str):
    print(message)
    exit(0)
      
if __name__ == '__main__':
    # === 1. Initialisation ===
    locale.setlocale(locale.LC_TIME, "fr_FR")
    # Charge les variables d'environnement
    env = load_env()
    # Prend en compte les musiques déjà utilisées
    already_used_list = get_songs_already_used()
    
    # === 2. Choix de la musique ===
    # Récupération des musiques dans le Google Sheet
    gs_api = GoogleSheetApi(env["API_KEY"])
    songs: list[Song] = gs_api.request(env["SPREADSHEET_ID"], "Requested", "A1", "J215")
    if len(songs) == 0:
        print_and_exit("Aucune musique n'est disponible dans le Google Sheet permettant la création d'une vidéo.")
    try:
        song_of_the_day = choose_song(songs, already_used_list)
    except Exception as e:
        print_and_exit(e)
        
    print("La musique du jour est :", song_of_the_day)
    # Sauvegarde la musique du jour dans le json d'historique
    save_new_song(song_of_the_day, already_used_list)
    
    # === 3. Génération de la vidéo ===
    
    NEW_NAME = "sotd.mp3"
    # Supprime la musique de l'itération précédente
    os.remove(NEW_NAME)
    # Télécharge le mp3 de la nouvelle musique grâce à spotdl
    song_of_the_day.download_mp3(NEW_NAME)
    # Génération de la vidéo
    try:
        ve.generate_video(song_of_the_day)
    except Exception as e:
        print(e)
    
    # === 4. Publication sur TikTok ===
    tiktok_video = TikTokVideo(song_of_the_day)
    tp.publish_video(tiktok_video, env["SESSION_ID_TIKTOK"])
    