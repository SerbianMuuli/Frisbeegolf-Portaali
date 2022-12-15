-- SQLite
CREATE VIEW IF NOT EXISTS Event_1
AS 
SELECT 
   Players.FirstName AS Etunimi,
   Players.LastName AS Sukunimi
FROM
   Events
INNER JOIN Courses ON Courses.CourseID = Events.CourseID
INNER JOIN Participants ON Participants.EventID = Events.EventID
INNER JOIN Players ON Players.PlayerID = Participants.PlayerID
WHERE Events.EventID = 1;


CREATE VIEW IF NOT EXISTS Event_2
AS 
SELECT 
   Players.FirstName AS Etunimi,
   Players.LastName AS Sukunimi
FROM
   Events
INNER JOIN Courses ON Courses.CourseID = Events.CourseID
INNER JOIN Participants ON Participants.EventID = Events.EventID
INNER JOIN Players ON Players.PlayerID = Participants.PlayerID
WHERE Events.EventID = 2;

CREATE VIEW IF NOT EXISTS Event_courses
AS 
SELECT 
   Events.Name AS Event,
   Courses.Name AS Rata,
   Courses.HoleCount as Väyliä
FROM
   Events
INNER JOIN Courses ON Courses.CourseID = Events.CourseID;


CREATE VIEW IF NOT EXISTS Littoinen_Väylät
AS 
SELECT 
   * 
FROM
   Hole
Where CourseID = 3;


