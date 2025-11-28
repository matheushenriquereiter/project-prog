class Screening:
    def __init__(self, date, start_time, end_time, id_movie):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.id_movie = id_movie

    def get_info(self):
        return f"Date: {self.date}, Start time: {self.start_time}, End time: {self.end_time}, ID movie: {self.id_movie}"
