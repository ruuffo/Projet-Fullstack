CREATE TABLE IF NOT EXISTS Question (
    Id_Question INTEGER PRIMARY KEY,
    Title varchar(50) not null,
    Text varchar(50) not null,
    Image varchar(100) not null,
    Quiz_Position int not null
);

Create TABLE if not EXISTS Answer (
    Id_Question INTEGER,
    Reponse_Position INTEGER,
    Text varchar(50) not null,
    IsCorrect BOOLEAN not null check(IsCorrect in (0,1)),
    FOREIGN KEY(Id_Question) REFERENCES Question(Id_Question),
    PRIMARY KEY(Id_Question, Reponse_Position)
);

CREATE TABLE IF NOT EXISTS Player (
    Player_Name VARCHAR(32) PRIMARY KEY  
);

CREATE TABLE IF NOT EXISTS Participation (
    Id_Question INTEGER,
    Reponse_Position INTEGER,
    Player_Name VARCHAR(32),
    FOREIGN KEY(Id_Question, Reponse_Position) REFERENCES Answer(Id_Question, Reponse_Position),
    FOREIGN KEY(Player_Name) REFERENCES Player(Player_Name),
    PRIMARY KEY(Id_Question, Reponse_Position, Player_Name)
);

--pour trouver le score d'un joueur
SELECT COUNT(IsCorrect) FROM Participation AS P INNER JOIN ANSWER AS A ON P.Id_Question = A.Id_Question AND P.Reponse_Position = A.Reponse_Position WHERE IsCorrect = 1 AND Player_Name = ?

--pour enregister une participation
INSERT INTO Participation(Id_Question, Reponse_Position, Player_Name) VALUES (?,?,?)