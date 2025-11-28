class Movie:
    def __init__(self, title, director, year, genre):
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre

    def get_info(self):
        return f"{self.title} ({self.year}), dirigido por {self.director}, gênero: {self.genre}"
