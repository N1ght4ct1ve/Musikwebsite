import vlc
import time
import random


class MusicPlayer:
    def __init__(self, song_path):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.queue = []
        self.the_current_song = None
        self.current_media = None
        self.path = song_path
        self.loop = False
        self.shuffle = False
        self.killed = False


    def add_to_queue(self, file_path):
        self.queue.append(file_path)
    
    def remove_from_queue(self, file_path):
        if file_path in self.queue:
            self.queue.remove(file_path)

    def play_next(self):
        if self.queue:
            if self.shuffle and (not self.loop):
                random.shuffle(self.queue)
            next_media = self.queue.pop(0)
            self.the_current_song = next_media
            self.current_media = self.instance.media_new(
                f"{self.path}/{next_media}.mp3")
            self.player.set_media(self.current_media)
            self.player.play()
        else:
            print("Die Warteschlange ist leer.")
            time.sleep(2)

    def play(self):
        self.play_next()
        while True:
            state = self.player.get_state()
            if state == vlc.State.Ended:
                if self.loop:
                    self.queue.insert(0, self.the_current_song)
                self.play_next()
            time.sleep(1)
            if self.killed:
                print("Der Player wurde getötet!")
                break


    def pause(self):
        self.player.pause()

    def skip(self):
        self.play_next()

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    def get_volume(self):
        return self.player.audio_get_volume()

    def get_queue(self):
        return self.queue

    def current_song(self):
        if self.current_media:
            # print(self.current_media.get_mrl())
            # test = self.current_media.get_mrl().split('/')[-1][:-4]
            # test = test.encode()
            return self.the_current_song
        return None
    
    def get_current_time(self):
        return self.player.get_time()
    
    def get_total_time(self):
        return self.player.get_length()
    
    def get_percent(self):
        return (self.get_current_time() / self.get_total_time())
    
    def toggle_loop(self):
        self.loop = not self.loop
        return self.loop

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        return self.shuffle
    
    def is_shuffled(self):
        return self.shuffle
    
    def is_looped(self):
        return self.loop
    
    def kill(self):
        self.killed = True



# Funktion zum Starten des Players in einem separaten Thread
def start_player(player):
    player.play()

# Beispielaufruf
if __name__ == "__main__":
    import threading
    # Pfad zu den Musikdateien
    song_path = "./music"
    
    # Player initialisieren
    player = MusicPlayer(song_path)
    
    # Lieder zur Warteschlange hinzufügen
    player.add_to_queue('Treehouse')
    player.add_to_queue('ICH ICH ICH')
    
    # Thread zum Abspielen des Players starten
    player_thread = threading.Thread(target=start_player, args=(player,))
    player_thread.start()

    time.sleep(5)
    print(player.get_percent())
    # Beispielhafte Interaktion mit dem Player
    time.sleep(10)  # Warte 10 Sekunden, bevor der Player gestoppt wird
    print(player.get_percent())
    player.kill()  # Player stoppen
    player_thread.join()  # Auf das Ende des Player-Threads warten


