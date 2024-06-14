import pygame
from queue import Queue

class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._is_playing = False
        self.music_queue = Queue()

    def load_music(self, file):
        pygame.mixer.music.load(file)

    def play(self):
        if not pygame.mixer.music.get_busy() and not self.music_queue.empty():
            next_music = self.music_queue.get()
            self.load_music(next_music)
            pygame.mixer.music.play()
            self._is_playing = True

    def add_to_queue(self, file):
        self.music_queue.put(file)


    def view_queue(self):
        queue_list = list(self.music_queue.queue)
        return queue_list

    def skip(self):
        # Stop current music
        self.stop()
        # Remove current music from queue
        if not self.music_queue.empty():
            self.music_queue.get()
        # Play next music if queue is not empty
        if not self.music_queue.empty():
            self.play()
        else:
            self._is_playing = False

    def pause(self):
        if self._is_playing:
            pygame.mixer.music.pause()
            self._is_playing = False

    def unpause(self):
        if not self._is_playing:
            pygame.mixer.music.unpause()
            self._is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self._is_playing = False
        while not self.music_queue.empty():
            self.music_queue.get()

    def is_playing(self):
        return self._is_playing
    
    def volume(self):
        return self.get_volume

    def close(self):
        pygame.quit()



if __name__ == "__main__":
    import time
    player = MusicPlayer()

    # Füge mehrere Musikdateien zur Warteschlange hinzu
    player.add_to_queue("./music/KRAFTKLUB - Blaues Licht.mp3")


    # Starte die Wiedergabe
    player.play()

    # Simuliere die Wiedergabe und Steuerung
    time.sleep(10)  # Beispiel: Musik für 10 Sekunden spielen


    player.close()
