import customtkinter as ctk
import re
from connection import create_connection
from entities.Movie import Movie
from entities.Customer import Customer

import customtkinter as ctk

connection = create_connection()
cursor = connection.cursor()

BG_MAIN = "#1E1E1E"
BG_SURFACE = "#252526"
COLOR_BUTTON = "#7C3AED"
COLOR_HOVER = "#6D28D9"
TEXT_MAIN = "#eeeeee"

font_title = ("Roboto", 24)
font_body = ("Roboto", 14)
font_button = ("Roboto", 14)


def checkEmail(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    if re.fullmatch(regex, email):
        return True

    return False


class Authentication(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40

        ctk.CTkLabel(
            self.container,
            text="Cinema do Rogério",
            font=font_title,
            text_color=TEXT_MAIN,
        ).pack(pady=10)

        ctk.CTkButton(
            self.container,
            text="Criar Conta",
            height=height,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Register"),
        ).pack(pady=10, fill="x")

        ctk.CTkButton(
            self.container,
            text="Entrar",
            height=height,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Login"),
        ).pack(fill="x")


class Register(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        ctk.CTkLabel(
            self.container, text="Nome:", font=font_body, text_color=TEXT_MAIN
        ).pack(anchor="w")
        self.username_entry = ctk.CTkEntry(self.container)
        self.username_entry.pack(pady=(0, 10), fill="x")

        ctk.CTkLabel(
            self.container, text="Email:", font=font_body, text_color=TEXT_MAIN
        ).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(self.container)
        self.email_entry.pack(pady=(0, 10), fill="x")

        ctk.CTkLabel(
            self.container, text="Senha:", font=font_body, text_color=TEXT_MAIN
        ).pack(anchor="w")
        self.password_entry = ctk.CTkEntry(self.container)
        self.password_entry.pack(fill="x")

        submit_button = ctk.CTkButton(
            self.container,
            text="Criar Conta",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=self.handle_register,
        )
        submit_button.pack(pady=10)

        return_button = ctk.CTkButton(
            self.container,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Authentication"),
        )
        return_button.pack()

        self.status_label = ctk.CTkLabel(self.container, text="", text_color="#ff746c")
        self.status_label.pack()

    def handle_register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not username or len(username) < 8:
            self.status_label.configure(text="nome de usuário inválido")
            return

        if not email or not checkEmail(email):
            self.status_label.configure(text="email de usuário inválido")
            return

        if not password or len(password) < 8:
            self.status_label.configure(text="senha de usuário inválida")
            return

        cursor.execute(
            "INSERT INTO customers (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password),
        )

        connection.commit()

        self.clear_form()

        self.controller.show_frame("Login")

    def clear_form(self):
        self.username_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.status_label.configure(text="")


class Login(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        ctk.CTkLabel(
            self.container, text="Email:", font=font_body, text_color=TEXT_MAIN
        ).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(self.container)
        self.email_entry.pack(pady=(0, 10), fill="x")

        ctk.CTkLabel(
            self.container, text="Senha:", font=font_body, text_color=TEXT_MAIN
        ).pack(anchor="w")
        self.password_entry = ctk.CTkEntry(self.container)
        self.password_entry.pack(fill="x")

        login_button = ctk.CTkButton(
            self.container,
            text="Entrar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=self.handle_login,
        )
        login_button.pack(pady=10)

        return_button = ctk.CTkButton(
            self.container,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Authentication"),
        )
        return_button.pack()

        self.status_label = ctk.CTkLabel(self.container, text="", text_color="#ff746c")
        self.status_label.pack()

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not checkEmail(email):
            self.status_label.configure(text="email de usuário inválido")
            return

        if not password or len(password) < 8:
            self.status_label.configure(text="senha de usuário inválida")
            return

        cursor.execute(
            "SELECT * FROM customers WHERE (email = %s) AND (password = %s)",
            (
                email,
                password,
            ),
        )

        customer = cursor.fetchone()

        if not customer:
            self.status_label.configure(text="usuário não encontrado")
            return

        self.controller.set_user(
            Customer(customer[0], customer[1], customer[2], customer[3])
        )
        self.controller.show_frame("Home")

    def clear_form(self):
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.status_label.configure(text="")


class Home(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        show_movies_button = ctk.CTkButton(
            self.container,
            text="Mostrar Filmes",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("ShowMovies"),
        )
        show_movies_button.pack(pady=(0, 10))

        add_movie_button = ctk.CTkButton(
            self.container,
            text="Adicionar Filme",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("AddMovie"),
        )
        add_movie_button.pack(pady=(0, 10))

        remove_movie_button = ctk.CTkButton(
            self.container,
            text="Remover Filme",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("RemoveMovie"),
        )
        remove_movie_button.pack(pady=(0, 10))

        show_screenings_button = ctk.CTkButton(
            self.container,
            text="Sessões disponíveis",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("ShowScreenings"),
        )
        show_screenings_button.pack(pady=(0, 10))

        add_screening_button = ctk.CTkButton(
            self.container,
            text="Adicionar Sessão",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("AddScreening"),
        )
        add_screening_button.pack(pady=(0, 10))


class ShowMovies(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        ctk.CTkLabel(
            self.container,
            text="Filmes em Cartaz",
            font=font_title,
            text_color=TEXT_MAIN,
        ).pack()
        ctk.CTkButton(
            self.container,
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            text="Voltar",
            command=lambda: controller.show_frame("Home"),
        ).pack(pady=10)

        self.movies_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.movies_frame.pack(fill="both", expand=True)

    def refresh(self):
        for widget in self.movies_frame.winfo_children():
            widget.destroy()

        cursor.execute("SELECT * FROM movies")
        movies_data = cursor.fetchall()

        movies = list(map(lambda m: Movie(m[1], m[2], m[3], m[4]), movies_data))

        for movie in movies:
            ctk.CTkLabel(
                self.movies_frame, text=movie.get_info(), text_color=TEXT_MAIN
            ).pack()


class AddMovie(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        ctk.CTkLabel(
            self.container,
            text="Adicionar Filme",
            font=font_title,
            text_color=TEXT_MAIN,
        ).pack(pady=10)

        ctk.CTkLabel(
            self.container, text="Título:", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(self.container)
        self.title_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.container, text="Diretor:", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.director_entry = ctk.CTkEntry(self.container)
        self.director_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.container,
            text="Ano de lançamento:",
            text_color=TEXT_MAIN,
            font=font_body,
        ).pack(anchor="w")
        self.year_entry = ctk.CTkEntry(self.container)
        self.year_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.container, text="Gênero:", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.genre_entry = ctk.CTkEntry(self.container)
        self.genre_entry.pack(fill="x")

        add_movie_button = ctk.CTkButton(
            self.container,
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            text="Adicionar",
            command=self.handle_add_movie,
        )
        add_movie_button.pack(pady=10)

        return_button = ctk.CTkButton(
            self.container,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Home"),
        )
        return_button.pack()

        self.status_label = ctk.CTkLabel(self.container, text="", text_color="#ff746c")
        self.status_label.pack()

    def handle_add_movie(self):
        title = self.title_entry.get()
        director = self.director_entry.get()
        year = self.year_entry.get()
        genre = self.genre_entry.get()

        if not title:
            self.status_label.configure(text="título não pode ser vazio")
            return

        if not director:
            self.status_label.configure(text="diretor não pode ser vazio")
            return

        if not year:
            self.status_label.configure(text="ano não pode ser vazio")
            return

        if not genre:
            self.status_label.configure(text="gênero não pode ser vazio")
            return

        cursor.execute(
            "INSERT INTO movies (title, director, year, genre) VALUES (%s, %s, %s, %s)",
            (
                title,
                director,
                year,
                genre,
            ),
        )

        connection.commit()

        self.controller.show_frame("Home")
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, "end")
        self.director_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
        self.genre_entry.delete(0, "end")
        self.status_label.configure(text="")


class RemoveMovie(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        ctk.CTkLabel(
            self.container,
            text="Remover Filme",
            font=font_title,
            text_color=TEXT_MAIN,
        ).pack(pady=10)

        ctk.CTkLabel(
            self.container, text="Título:", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(self.container)
        self.title_entry.pack(fill="x", pady=(0, 10))

        remove_movie_button = ctk.CTkButton(
            self.container,
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            text="Remover",
            command=self.handle_remove_movie,
        )
        remove_movie_button.pack(pady=10)

        return_button = ctk.CTkButton(
            self.container,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Home"),
        )
        return_button.pack()

        self.status_label = ctk.CTkLabel(self.container, text="", text_color="#ff746c")
        self.status_label.pack()

    def handle_remove_movie(self):
        title = self.title_entry.get()

        if not title:
            self.status_label.configure(text="título não pode ser vazio")
            return

        cursor.execute(
            "DELETE FROM movies WHERE title = %s",
            (title,),
        )

        connection.commit()

        self.controller.show_frame("Home")
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, "end")
        self.status_label.configure(text="")


class ShowScreenings(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        height = 40
        width = 200

        ctk.CTkLabel(
            self, text="Sessões Disponíveis", font=font_title, text_color=TEXT_MAIN
        ).pack(pady=(20, 0))

        return_button = ctk.CTkButton(
            self,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Home"),
        )
        return_button.pack(pady=10)

        self.screenings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.screenings_frame.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        height = 40
        width = 200

        for widget in self.screenings_frame.winfo_children():
            widget.destroy()

        cursor.execute("SELECT * FROM screenings")
        screenings_data = cursor.fetchall()

        for row in screenings_data:
            screening_id = row[0]
            date = row[1]
            movie_id = row[4]

            cursor.execute("SELECT title FROM movies WHERE id_movie = %s", (movie_id,))
            movie_title = cursor.fetchone()[0]

            card = ctk.CTkFrame(self.screenings_frame, fg_color=BG_SURFACE)
            card.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(
                card, text=f"{movie_title} - {date}", text_color=TEXT_MAIN
            ).pack(side="left", padx=10)

            button = ctk.CTkButton(
                card,
                text="Ver Assentos",
                height=height,
                width=width,
                fg_color=COLOR_BUTTON,
                hover_color=COLOR_HOVER,
                command=lambda screening_id=screening_id: self.controller.show_frame(
                    "Seats", screening_id
                ),
            )
            button.pack(side="right")


class AddScreening(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        height = 40
        width = 200

        ctk.CTkLabel(
            self.container,
            text="Adicionar Sessão",
            font=font_title,
            text_color=TEXT_MAIN,
        ).pack(pady=10)

        ctk.CTkLabel(
            self.container, text="Data:", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(self.container)
        self.title_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.container, text="Hora de início:", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.director_entry = ctk.CTkEntry(self.container)
        self.director_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.container,
            text="Hora de fim:",
            text_color=TEXT_MAIN,
            font=font_body,
        ).pack(anchor="w")
        self.year_entry = ctk.CTkEntry(self.container)
        self.year_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.container, text="Nome do filme", text_color=TEXT_MAIN, font=font_body
        ).pack(anchor="w")
        self.genre_entry = ctk.CTkEntry(self.container)
        self.genre_entry.pack(fill="x")

        add_screening_button = ctk.CTkButton(
            self.container,
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            text="Adicionar",
            command=self.handle_add_screening,
        )
        add_screening_button.pack(pady=10)

        return_button = ctk.CTkButton(
            self.container,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("Home"),
        )
        return_button.pack()

        self.status_label = ctk.CTkLabel(self.container, text="", text_color="#ff746c")
        self.status_label.pack()

    def handle_add_screening(self):
        date = self.title_entry.get()
        start_time = self.director_entry.get()
        end_time = self.year_entry.get()
        movie_title = self.genre_entry.get()

        if not date:
            self.status_label.configure(text="título não pode ser vazio")
            return

        if not start_time:
            self.status_label.configure(text="diretor não pode ser vazio")
            return

        if not end_time:
            self.status_label.configure(text="ano não pode ser vazio")
            return

        if not movie_title:
            self.status_label.configure(text="gênero não pode ser vazio")
            return

        cursor.execute("SELECT id_movie FROM movies WHERE title = %s", (movie_title,))
        id_movie = cursor.fetchone()

        if not id_movie:
            self.status_label.configure(text="filme não encontrado")
            return

        cursor.execute(
            "INSERT INTO screenings (screening_date, start_time, end_time, movie_id) VALUES (%s, %s, %s, %s)",
            (date, start_time, end_time, id_movie[0]),
        )

        connection.commit()

        self.controller.show_frame("Home")
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, "end")
        self.director_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
        self.genre_entry.delete(0, "end")
        self.status_label.configure(text="")


class Seats(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.controller = controller

        height = 40
        width = 200

        self.screening_id = None

        self.selected_seats = []
        self.buttons = {}

        ctk.CTkLabel(
            self, text="Selecione Seus Assentos", font=font_title, text_color=TEXT_MAIN
        ).pack(pady=(20, 0))

        self.seats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.seats_frame.pack(pady=20)

        self.confirm_button = ctk.CTkButton(
            self,
            text="Confirmar",
            state="disabled",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=self.confirm_purchase,
        )
        self.confirm_button.pack(pady=10)

        return_button = ctk.CTkButton(
            self,
            text="Voltar",
            height=height,
            width=width,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            command=lambda: controller.show_frame("ShowScreenings"),
        )
        return_button.pack()

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def set_data(self, screening_id):
        self.screening_id = screening_id
        self.selected_seats = []
        self.status_label.configure(text="")
        self.confirm_button.configure(state="disabled")
        self.draw_grid()

    def draw_grid(self):
        for widget in self.seats_frame.winfo_children():
            widget.destroy()
        self.buttons = {}

        cursor.execute(
            "SELECT seat_row, seat_col FROM tickets WHERE screening_id = %s",
            (self.screening_id,),
        )

        occupied_seats = list(
            map(
                lambda occupied_seat: (
                    int(occupied_seat[0]),
                    int(occupied_seat[1]),
                ),
                cursor.fetchall(),
            )
        )

        customer = self.controller.get_user()

        cursor.execute(
            "SELECT seat_row, seat_col FROM tickets WHERE customer_id = %s",
            (customer.id,),
        )

        user_seats = list(
            map(
                lambda occupied_seat: (
                    int(occupied_seat[0]),
                    int(occupied_seat[1]),
                ),
                cursor.fetchall(),
            )
        )

        rows = ["A", "B", "C", "D"]
        cols = 6

        for row_index, row_letter in enumerate(rows):
            for col_index in range(cols):
                seat_coordinate = (row_index, col_index)

                is_occupied = seat_coordinate in occupied_seats
                is_user = seat_coordinate in user_seats

                if is_user:
                    color = "yellow"
                    state = "disabled"
                    command = None
                elif is_occupied:
                    color = "red"
                    state = "disabled"
                    command = None
                else:
                    color = "green"
                    state = "normal"
                    command = lambda row_index=row_index, col_index=col_index: self.toggle_seat(
                        row_index, col_index
                    )

                button = ctk.CTkButton(
                    self.seats_frame,
                    text=f"{row_letter}{col_index + 1}",
                    width=60,
                    height=60,
                    fg_color=color,
                    state=state,
                    command=command,
                )
                button.grid(row=row_index, column=col_index, padx=5, pady=5)

                self.buttons[seat_coordinate] = button

    def toggle_seat(self, row, col):
        coord = (row, col)
        button = self.buttons[coord]

        if coord in self.selected_seats:
            self.selected_seats.remove(coord)
            button.configure(fg_color="green")
        else:
            self.selected_seats.append(coord)
            button.configure(fg_color="#D4A017")

        if len(self.selected_seats) > 0:
            self.confirm_button.configure(state="normal")
        else:
            self.confirm_button.configure(state="disabled")

    def confirm_purchase(self):
        if not self.selected_seats:
            return

        customer = self.controller.get_user()

        for row, col in self.selected_seats:
            cursor.execute(
                "INSERT INTO tickets (seat_row, seat_col, customer_id, screening_id) VALUES (%s, %s, %s, %s)",
                (row, col, customer.id, self.screening_id),
            )

        connection.commit()

        self.selected_seats = []
        self.confirm_button.configure(state="disabled")

        self.after(1000, self.draw_grid)


class Application(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_MAIN)
        self.title("Sistema de Gestão de Cinema")
        self.minsize(800, 600)
        self.maxsize(1200, 800)
        self.geometry("800x600")

        self.container = ctk.CTkFrame(self, fg_color=BG_MAIN)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Frame in (
            Authentication,
            Register,
            Login,
            Home,
            ShowMovies,
            AddMovie,
            RemoveMovie,
            ShowScreenings,
            AddScreening,
            Seats,
        ):
            page_name = Frame.__name__
            frame = Frame(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Authentication")

    def show_frame(self, frame_name, data=None):
        frame = self.frames[frame_name]

        if frame_name in ("ShowMovies", "ShowScreenings"):
            frame.refresh()

        if data is not None and hasattr(frame, "set_data"):
            frame.set_data(data)

        frame.tkraise()

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user


if __name__ == "__main__":
    application = Application()
    application.mainloop()
