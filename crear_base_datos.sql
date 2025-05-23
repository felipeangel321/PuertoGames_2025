
CREATE DATABASE PuertoGames2025;
GO
USE PuertoGames2025;
GO

CREATE TABLE Plataformas (
id_plataforma INT PRIMARY KEY IDENTITY(1,1),
Nombre NVARCHAR (50) NOT NULL
);

CREATE TABLE VideoJuegos(
id_videojuego INT PRIMARY KEY IDENTITY(1,1),
titulo NVARCHAR(50) NOT NULL,
precio DECIMAL(10,2) NOT NULL,
stock INT NOT NULL DEFAULT (0),
id_plataforma INT NOT NULL,
FOREIGN KEY (id_plataforma) REFERENCES Plataformas(id_plataforma),
CHECK (stock >= 0)
);

INSERT INTO Plataformas (nombre) VALUES 

('PlayStation 5'),
('Xbox Series X'),
('Nintendo Switch'),
('PC'),
('Steam Deck');
INSERT INTO Videojuegos (titulo, precio, stock, id_plataforma) VALUES 

('The Legend of Zelda: Tears of the Kingdom', 69.99, 15, 3),
('Halo Infinite', 59.99, 10, 2),
('Spider-Man: Miles Morales', 49.99, 8, 1),
('Cyberpunk 2077', 39.99, 20, 4),
('Stardew Valley', 14.99, 25, 5),
('God of War Ragnarok', 69.99, 5, 1),
('Forza Horizon 5', 59.99, 7, 2),
('Mario Kart 8 Deluxe', 59.99, 12, 3),
('Elden Ring', 59.99, 10, 4),
('Hollow Knight: Silksong', 29.99, 18, 5);
--
