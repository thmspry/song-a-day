from Song import Song

class TikTokVideo:
    def __init__(self, song: Song, path: str = "tiktok_of_the_day.mp4"):
        self.description = f"Aujourd'hui, {song.title} par {song.artist} sortie sur l'album {song.album.title} en {song.album.date.year} !"
        self.path = path
        
    def __init__(self, description: str, path: str):
        self.description = description
        self.path = path
        
    def __str__(self) -> str:
        stre: str = f'Description: "{self.description}"'
        stre += f"\n--> fichier dans ./{self.path}"
        return stre