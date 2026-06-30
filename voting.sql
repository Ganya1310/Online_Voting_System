CREATE TABLE Users(
 id INT IDENTITY(1,1) PRIMARY KEY,
 name NVARCHAR(50),
 voter_id NVARCHAR(20) UNIQUE,
 password NVARCHAR(255),
 has_voted BIT DEFAULT 0
);

CREATE TABLE Votes(
 vote_id INT IDENTITY(1,1) PRIMARY KEY,
 encrypted_vote NVARCHAR(MAX),
 timestamp DATETIME DEFAULT GETDATE()
);

CREATE TABLE Admin(
 admin_id INT IDENTITY(1,1) PRIMARY KEY,
 username NVARCHAR(50) UNIQUE,
 password NVARCHAR(255)
);

INSERT INTO Admin(username, password)
VALUES('admin','admin123');

INSERT INTO Users(name, voter_id, password)
VALUES
('Dhriti Hegde','V001','$2b$12$nfx1DeGwsa71nY3xjg0WQOCUavFq0CdfAlQB8fRTfIFgcRj/qmYN6'),
('Disha Rani','V002','$2b$12$/xpmIg2NBXukuWXdfJNtjucWHTpyrfo3BF8jF/RJq9A8KgQIz42w.'),
('Diyadarshini M Amin','V003','$2b$12$p/2Ppt1kxK5m1od.hJrosuw6QfiGhHZwbmHm97/GSK6LCO3fdEwJ6'),
('Ganya','V004','$2b$12$NjBUr0TnU/mav5tGR.uO/OOS.imCK5QgALamr/MRgsOjj4uuMB3Gm');

-- Keep Votes table like this (NO voter_id)
CREATE TABLE Votes(
 vote_id INT IDENTITY(1,1) PRIMARY KEY,
 encrypted_vote NVARCHAR(MAX),
 timestamp DATETIME DEFAULT GETDATE()
);

DROP TABLE Votes;

select * from Votes;

UPDATE Admin 
SET password = '$2b$12$Cs8cHPsfg8VqfWsCc6H2xOnenytz6vy6HWDQj23/PFaVIfvhHINYO'
WHERE username='admin';

select * from Admin;

SELECT COUNT(*) AS TotalVotes FROM Votes;

SELECT name, voter_id, has_voted FROM Users;

DELETE FROM Votes;
UPDATE Users SET has_voted = 0;