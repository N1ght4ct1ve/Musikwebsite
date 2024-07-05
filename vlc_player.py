import vlc
import time


class MusicPlayer:
    def __init__(self, song_path):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.queue = []
        self.the_current_song = None
        self.current_media = None
        self.path = song_path

    def add_to_queue(self, file_path):
        self.queue.append(file_path)

    def play_next(self):
        if self.queue:
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
                self.play_next()
            time.sleep(1)

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


if __name__ == "__main__":
    import threading

    def test():
        print("Kam durch")
        time.sleep(3)
        print(player.current_song())
        time.sleep(5)  # 10 Sekunden warten
        player.pause()
        print("Lautstärke vor Änderung:", player.get_volume())
        player.set_volume(50)
        print("Lautstärke nach Änderung:", player.get_volume())
        player.skip()
        print(player.current_song())

    # Beispielverwendung
    player = MusicPlayer("./music")
    player.add_to_queue('Sad Trombone')
    player.add_to_queue('ICH ICH ICH')
    # player.add_to_queue('path/to/your/third/song.mp3')

    print("Test")
    # thread1 = threading.Thread(target=player.play, daemon=True, args=None)
    print("Helloo?")
    # thread2 = threading.Thread(test, daemon=True)
    # thread2.start()
    # thread1.start()

    test()
    print("Aktuelle Warteschlange:", player.get_queue())
