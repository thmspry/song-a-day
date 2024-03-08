import Album
import subprocess


class Song:
    
    featurings: list[str]
    def __init__(self, title: str, artist: str, length: str, spotify_id: str, album: Album):
        self.title = title
        self.artist = artist
        self.length = length
        self.spotify_id = spotify_id
        self.album = album
        self.featurings = []
        
    def __str__(self):
        str_final = f'{self.title} by {self.artist} on {self.album}'
        if self.is_feat():
            str_final += f'\n\tfeat. {", ".join(self.featurings)}'
        return str_final
    
    def __eq__(self, other_song) -> bool:
        return self.spotify_id == other_song.spotify_id
    
    def add_featuring(self, featuring: str):
        self.featurings.append(featuring)
        
    def is_feat(self) -> bool:
        return len(self.featurings) > 0
    
    def download_mp3(self):
        spotify_url = f'https://open.spotify.com/track/{self.spotify_id}'
        subprocess.run(["spotdl", spotify_url]) 
        
        