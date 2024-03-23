from model.Album import Album


class Song:
    title: str
    artist: str
    length: str
    spotify_id: str
    comment: str
    album: Album
    featurings: list[str] | None = []
    
    def __init__(self, title: str, artist: str, length: str, spotify_id: str, comment: str, album: Album):
        self.title = title.split("(")[0]
        self.artist = artist
        self.length = length
        self.spotify_id = spotify_id
        self.comment = comment
        self.album = album
        self.featurings = []
        
    def __str__(self):
        str_final = f'{self.title} by {self.artist} on {self.album}'
        if self.is_feat():
            str_final += f'\n\tfeat. {", ".join(self.featurings)}'
        return str_final
    
    def to_json(self) -> dict:
        return {
            "spotify_id": self.spotify_id,
            "title": self.title,
            "artist": self.artist,
            "length": self.length,
            "comment": self.comment,
            "album": self.album.to_json(),
            "featurings": self.featurings,
        }
        
    def to_json_history(self) -> dict:
        return {
            "spotify_id": self.spotify_id,
            "title": self.title,
            "artist": self.artist,
            "featurings": self.featurings,
            "album_title": self.album.title,
            "album_cover": self.album.cover,
        }
    
    def __eq__(self, other_song) -> bool:
        return self.spotify_id == other_song.spotify_id
    
    def add_featuring(self, featuring: str):
        self.featurings.append(featuring)
        
    def is_feat(self) -> bool:
        return len(self.featurings) > 0
    
    def lenght_in_seconds(self) -> int:
        time = self.length.split(":")
        return int(time[0]) * 60 + int(time[1])
    
    
        