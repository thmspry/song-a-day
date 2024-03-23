import datetime

class Album:
    title: str
    cover: str
    date: str
    
    def __init__(self, title, cover, date):
        self.title = title
        self.cover = cover
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d')
        
    def to_json(self) -> dict:
        return {
            "title": self.title,
            "cover": self.cover,
            "date": self.date.strftime('%Y-%m-%d'),
        }

    def __str__(self):
        return f'{self.title} ({self.date.strftime("%d %B %Y")})'
    
    def __eq__(self, other_album) -> bool:
        return self.title == other_album.title and self.cover == other_album.cover and self.date == other_album.date