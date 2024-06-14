import vlc
import time

class MusicPlayer:
    def __init__(self, song_path):
        # Create a VLC media player object
        self.media_player = vlc.MediaPlayer()
        # Create a list to hold the queue of media paths
        self.queue = []
        # Set initial volume
        self.media_player.audio_set_volume(100)
        self.path = song_path

    def add_to_queue(self, song):
        """Add a song to the queue."""
        self.queue.append(song)
    
    def play_next(self):
        """Play the next media in the queue."""
        if self.queue:
            song = self.queue.pop(0)
            self.play_media(song)
        else:
            print("Queue is empty!")

    def play_media(self, song):
        """Play a specific media file."""
        media = vlc.Media(f"{self.path}/{song}.mp3")
        self.media_player.set_media(media)
        self.media_player.play()

    def play(self):
        """Start playing the media."""
        if not self.media_player.is_playing() and self.queue:
            self.play_next()
        else:
            self.media_player.play()
    
    def pause(self):
        """Pause the media."""
        self.media_player.pause()
    
    def stop(self):
        """Stop the media."""
        self.media_player.stop()
    
    def set_volume(self, volume):
        """Set the volume of the media player."""
        self.media_player.audio_set_volume(volume)
    
    def get_volume(self):
        """Get the current volume of the media player."""
        return self.media_player.audio_get_volume()
    
    def set_track(self, track_id):
        """Set the audio track."""
        self.media_player.audio_set_track(track_id)
    
    def get_track(self):
        """Get the current audio track."""
        return self.media_player.audio_get_track()
    
    def get_time(self):
        """Get the current audio track."""
        return self.media_player.get_time()
    
    def is_playing(self):
        """Check if the media is playing."""
        return self.media_player.is_playing()
    
    def get_length(self):
        """Check if the media is playing."""
        return self.media_player.get_length()
    

    def get_queue(self):
        """Print the current queue of media files."""
        if self.queue:
            return self.queue
        else:
            return []

    def skip(self):
        """Skip the current media and play the next in the queue."""
        if self.media_player.is_playing():
            self.stop()  # Stop current media
            self.play_next()  # Play next in queue
        elif self.queue:
            self.play_next()  # Play next in queue directly if paused or stopped



# Example usage
if __name__ == "__main__":
    # Create an instance of the MusicPlayer
    player = MusicPlayer("./music")
    
    # Add media files to the queue
    player.add_to_queue("In Your Hands")
    player.add_to_queue("Cowboys On Acid")
    
    # Print the current queue
    player.print_queue()
    
    # Start playing the media from the queue
    player.play()
    


    # Play the next media in the queue
    # player.play_next()
    
    # Print the current queue again
    player.print_queue()
    print("-----")
    print(player.get_track())
    print("-----")

    while True:
        print(f"Is playing... {player.get_time()/1000} von {player.get_length()/1000} Sekunden er spielt gerade: {player.is_playing()}")
        time.sleep(2)
