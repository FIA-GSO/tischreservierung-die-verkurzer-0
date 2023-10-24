-----------------------------------------------------------------------------
-- Erzeugt eine SQLite Testdatenbank.
-- 
-- Flask üblich wäre, diese Datei schema.sql zu nennen.
-- Siehe auch: https://flask.palletsprojects.com/en/2.3.x/tutorial/database/
--
-----------------------------------------------------------------------------

DROP TABLE IF EXISTS reservierungen;
DROP TABLE IF EXISTS tische;

CREATE TABLE tische(
    tischnummer              INTEGER NOT NULL UNIQUE
,   anzahlPlaetze   INTEGER 
,   PRIMARY KEY (tischnummer)
);

CREATE TABLE reservierungen(
    reservierungsnummer          INTEGER NOT NULL UNIQUE
,   zeitpunkt   TEXT
,   dauerMin   INTEGER
,   tischnummer     INTEGER
,   pin         INTEGER
,   storniert   BOOLEAN NOT NULL CHECK (storniert IN ('True', 'False')) -- SQLite unterstützt keine Boolschen Werte, aber
,   PRIMARY KEY (reservierungsnummer)                                   -- dieser Workaround lässt nur zwei Einträge zu.
,   FOREIGN KEY (tischnummer) REFERENCES tische(tischnummer)
);

INSERT INTO tische (tischnummer, anzahlPlaetze) VALUES
    (1, 4)
,   (2, 6)
,   (3, 6)
,   (4, 5)
,   (5, 6)
,   (6, 5)
;

INSERT INTO reservierungen (reservierungsnummer, zeitpunkt, tischnummer, dauerMin, pin, storniert) VALUES
    (1, '2022-02-02 17:30:00', 1, 60, 1331, 'False') -- PIN wurde garantiert zufällig erzeugt...
,   (2, '2022-02-02 18:30:00', 1, 30, 1332, 'False')
,   (3, '2022-02-02 19:30:00', 1, 120, 1333, 'False')
,   (4, '2022-02-02 18:30:00', 3, 50, 1334, 'False')
,   (5, '2022-02-02 19:30:00', 3, 80, 1335, 'False')
,   (6, '2022-02-02 20:30:00', 3, 20, 1336, 'False')
;
