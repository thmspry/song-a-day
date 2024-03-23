from Song import Song
from Album import Album
from pydantic import BaseModel


class AlbumBody(BaseModel):
    title: str
    cover: str
    date: str

class SongBody(BaseModel):
    title: str
    artist: str
    length: str
    spotify_id: str
    comment: str
    album: AlbumBody
    featurings: list[str] | None = []

def songbody_to_song(song: SongBody) -> Song:
    album = albumbody_to_album(song.album)
    song = Song(song.title, song.artist, song.length, song.spotify_id, song.comment, album)
    for feat in song.featurings:
        song.add_featuring(feat)
    return song

def albumbody_to_album(album: AlbumBody) -> Album:
    return Album(album.title, album.cover, album.date)