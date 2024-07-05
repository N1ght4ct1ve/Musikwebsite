import sqlite3

class Database:
    def __init__(self, db_name='db_songs.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        # Erstelle die Tabelle, falls sie nicht existiert
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            priority INTEGER NOT NULL DEFAULT 0
        )
        ''')
        self.conn.commit()

    def add_song(self, name, url, priority=0):
        # Füge einen neuen Song hinzu
        self.cursor.execute('''
        INSERT INTO songs (name, url, priority)
        VALUES (?, ?, ?)
        ''', (name, url, priority))
        self.conn.commit()

    def delete_song(self, song_id):
        # Lösche einen Song basierend auf seiner ID
        self.cursor.execute('''
        DELETE FROM songs WHERE id=?
        ''', (song_id,))
        self.conn.commit()

    def update_priority(self, song_id, priority):
        # Aktualisiere die Priorität eines Songs basierend auf seiner ID
        self.cursor.execute('''
        UPDATE songs
        SET priority=?
        WHERE id=?
        ''', (priority, song_id))
        self.conn.commit()

    def get_songs(self):
        # Hole alle Songs aus der Datenbank
        self.cursor.execute('SELECT * FROM songs')
        return self.cursor.fetchall()

    def __del__(self):
        # Schließe die Datenbankverbindung beim Zerstören des Objekts
        self.conn.close()

# Beispielverwendung
if __name__ == '__main__':
    db = Database()

    # Füge ein paar Songs hinzu
    db.add_song('Song 1', 'https://youtube.com/song1')
    db.add_song('Song 2', 'https://youtube.com/song2', 5)

    # Zeige alle Songs an
    songs = db.get_songs()
    for song in songs:
        print(song)

    # Aktualisiere die Priorität eines Songs
    db.update_priority(1, 10)

    # Lösche einen Song
    db.delete_song(2)

    # Zeige alle Songs an
    songs = db.get_songs()
    for song in songs:
        print(song)
