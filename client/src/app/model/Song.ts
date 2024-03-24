export class Song {
  public spotify_id: string
  public title: string
  public artist: string
  public featurings: string[]
  public album_title: string
  public album_cover: string

  constructor(spotify_id: string, title: string, artist: string, featurings: string[], album_title: string, album_cover: string) {
    this.spotify_id = spotify_id
    this.title = title
    this.artist = artist
    this.featurings = featurings
    this.album_title = album_title
    this.album_cover = album_cover
  }
}
