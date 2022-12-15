
import sqlite3

# taulut

courses = """
    CREATE TABLE IF NOT EXISTS `Courses` (
    `CourseID`      INTEGER     NOT NULL,
    `Name`          TEXT        NOT NULL,
    `HoleCount`     INTEGER     NOT NULL,
    `CoursePar`     INTEGER     NOT NULL,
    `CourseRating`  INTEGER     NOT NULL,
    `BogeyRating`   INTEGER     NOT NULL,
    `SlopeRating`   INTEGER     NOT NULL,
    PRIMARY KEY (CourseID)
    );
"""

events = """
    CREATE TABLE IF NOT EXISTS `Events` (
    `EventID`       INTEGER     NOT NULL,
    `Name`          TEXT        NOT NULL,
    `ScheduleDate`  TEXT        NOT NULL,
    `ScoringTypeID` INTEGER     NOT NULL,
    `CourseID`      INTEGER     NOT NULL,
    FOREIGN KEY(CourseID) REFERENCES Courses(CourseID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    PRIMARY KEY (EventID)
    );
"""

#teams = """
#    CREATE TABLE IF NOT EXISTS `Teams` (
#    `TeamID`        INTEGER     NOT NULL,
#    `TeamName`      TEXT        NOT NULL,
#    PRIMARY KEY (TeamID)
#    );
#"""

players = """
    CREATE TABLE IF NOT EXISTS `Players` (
    `PlayerID`      INTEGER     NOT NULL,
    `FirstName`     TEXT        NOT NULL,
    `LastName`      TEXT        NOT NULL,
    `Handicap`      INTEGER     NOT NULL,
    PRIMARY KEY (PlayerID)
    );
"""


scores = """
    CREATE TABLE IF NOT EXISTS `Scores` (
    `Score`         INTEGER     NOT NULL,
    `PlayerID`      INTEGER     NOT NULL,
    `EventID`      INTEGER     NOT NULL,
    FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(EventID) REFERENCES Events(EventID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (Score)
    );
"""


participants = """
    CREATE TABLE IF NOT EXISTS `Participants` (
    `PlayerID`      INTEGER     NOT NULL,
    `EventID`       INTEGER     NOT NULL,
    FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(EventID) REFERENCES Events(EventID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY(PlayerID)
    );
"""


hole = """
    CREATE TABLE IF NOT EXISTS `Hole` (
    `CourseID`    INTEGER     NOT NULL,
    `HoleID`      INTEGER     NOT NULL,
    `HolePar`     INTEGER     NOT NULL,
    FOREIGN KEY(CourseID) REFERENCES Courses(CourseID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY(HoleID)
    );
"""

score = """
    CREATE TABLE IF NOT EXISTS `Score` (
    `Score`       INTEGER     ,
    `HoleID`      INTEGER     NOT NULL,
    `PlayerID`    INTEGER     NOT NULL,
    FOREIGN KEY(HoleID) REFERENCES Hole(HoleID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY(Score)
    );
"""


taulut = [courses, events, players, scores, participants, hole, score]
db_name = 'friba.db'
conn = sqlite3.connect(db_name)
print(f"\nConnected to database: {db_name}\n")
i = 1
for taulu in taulut:
    conn.execute(taulu)
    print(f"{i}/{len(taulut)} tables added succesfully")
    i += 1
conn.commit()

kursori = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("\nlisäyt taulut:\n")
for item in kursori.fetchall():
    print(', '.join(map(str, item)))
    

conn.close()

print("loppu")
