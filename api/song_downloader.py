import subprocess
import os



def download_mp3(spotify_id: str, path: str):
    spotify_url = f'https://open.spotify.com/track/{spotify_id}'
    subprocess.run(["spotdl", spotify_url])
    # Search for the downloaded file and move it to the production folder
    for fichier in os.listdir("./"):
        if fichier.endswith(".mp3"):
            os.rename(fichier, path)