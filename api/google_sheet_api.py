from googleapiclient.discovery import build

import sys
sys.path.append('model')
from Song import Song
from Album import Album

class GoogleSheetApi:
    def __init__(self, api_key: str):
        self.sheet_connection = build('sheets', 'v4', developerKey=api_key).spreadsheets()
    
    def request(self, spreadsheet_id: str, sheet_name: str, range_start: str, range_end: str) -> list[Song]:
        range_name = f'{sheet_name}!{range_start}:{range_end}'
        try:
            result = self.sheet_connection.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        except Exception as e:
            raise Exception("Impossible de récupérer les données du Google Sheet. Vérifiez que l'ID du Google Sheet ou que la clé API soient corrects.\n: " + str(e))
        values = result.get('values', [])
        
        songs: list[Song] = []
        
        header: list = values[0]
        # header index for constructor
        header_idx_c: dict = {}
        for header_name in header:
            header_index: int = header.index(header_name)
            header_idx_c[header_name] = header_index

        for song_data in values[1:]:
            song = None
            
            
            comment_done = song_data[header_idx_c['Commentaire fini']] == "TRUE"
            
            # Select only the songs with all the data filled
            if len(song_data) == len(header) and comment_done:
                
                # Album
                album_title: str = song_data[header_idx_c['Album']]
                album_date: str = song_data[header_idx_c['Album Date']]
                cover: str = song_data[header_idx_c['Cover url high']]
                album = Album(album_title, cover, album_date)
                
                # Song
                    # Basic song data
                title: str = song_data[header_idx_c['Song']]
                length: str = song_data[header_idx_c['Time']]
                spotify_id: str = song_data[header_idx_c['Spotify Track Id']]
                
                comment: str = song_data[header_idx_c['Comment']]
                    # Artists
                artist: str = song_data[header_idx_c['Artist']]
                
                
                artists = artist.split(',')

                song = Song(title, artists[0], length, spotify_id, comment, album)

                if len(artists) > 1: # Song includes featuring artists
                    for artist_feat in artists[1:]:
                        song.add_featuring(artist_feat)
                
                songs.append(song)
        return songs
                