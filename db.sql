DROP DATABASE cinema;
SHOW DATABASES;
CREATE DATABASE cinema;
USE cinema;

CREATE TABLE movies (
	id_movie INT PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	director VARCHAR(255) NOT NULL,
	year YEAR NOT NULL,
	genre VARCHAR(255) NOT NULL
);

INSERT INTO movies (title, director, year, genre) VALUES
('A Origem', 'Christopher Nolan', 2010, 'Ficção Científica'),
('O Poderoso Chefão', 'Francis Ford Coppola', 1972, 'Crime'),
('Cidade de Deus', 'Fernando Meirelles', 2002, 'Drama'),
('Vingadores: Ultimato', 'Anthony Russo', 2019, 'Ação'),
('Interestelar', 'Christopher Nolan', 2014, 'Ficção Científica'),
('Barbie', 'Greta Gerwig', 2023, 'Comédia'),
('Pulp Fiction', 'Quentin Tarantino', 1994, 'Crime'),
('O Auto da Compadecida', 'Guel Arraes', 2000, 'Comédia'),
('Homem-Aranha: Através do Aranhaverso', 'Joaquim Dos Santos', 2023, 'Animação'),
('Titanic', 'James Cameron', 1997, 'Romance');

CREATE TABLE customers (
	id_customer INT PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL
);

INSERT INTO customers (username, email, password) VALUES ("a", "a", "a");
SELECT * FROM customers;

CREATE TABLE screenings (
	id_screening INT PRIMARY KEY AUTO_INCREMENT,
	screening_date DATE NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	movie_id INT,
	FOREIGN KEY (movie_id) REFERENCES movies(id_movie) ON DELETE CASCADE
)

INSERT INTO screenings (screening_date, start_time, end_time, movie_id) VALUES
('2025-11-22', '14:00:00', '16:30:00', 1),
('2025-11-22', '18:00:00', '21:00:00', 2),
('2025-11-22', '21:30:00', '23:40:00', 3);
SELECT * FROM screenings;

CREATE TABLE tickets (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    seat_row VARCHAR(255) NOT NULL,
    seat_col VARCHAR(255) NOT NULL,
    customer_id INT NOT NULL,
    screening_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id_customer) ON DELETE CASCADE,
    FOREIGN KEY (screening_id) REFERENCES screenings(id_screening) ON DELETE CASCADE
);

INSERT INTO tickets (seat_row, seat_col, customer_id, screening_id) VALUES
(1, 2, 1, 1);
SELECT * FROM tickets;
DELETE FROM tickets;
