from Song import Song

class TikTokVideo:
    def __init__(self, song: Song, path: str):
        self.description = f"Aujourd'hui, {song.title} par {song.artist} sortie sur l'album {song.album.title} en {song.album.date.year} !"
        self.path = path
    
        
    def __str__(self) -> str:
        stre: str = f'Description: "{self.description}"'
        stre += f"\n--> fichier dans ./{self.path}"
        return stre