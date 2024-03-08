class Album:
    def __init__(self, title, cover, date, label):
        self.title = title
        self.cover = cover
        self.date = date
        self.label = label

    def __str__(self):
        return f'{self.title} ({self.date}) under {self.label} label'
    
    def __eq__(self, other_album) -> bool:
        return self.title == other_album.title and self.cover == other_album.cover and self.date == other_album.date