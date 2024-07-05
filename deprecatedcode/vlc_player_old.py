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

        # Event manager for the media player
        self.event_manager = self.media_player.event_manager()
        # Register event for end of media
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end_reached)

    def add_to_queue(self, song):
        """Add a song to the queue."""
        self.queue.append(song)

    def play_next(self):
        """Play the next media in the queue."""
        
        if self.queue:
            song = self.queue.pop(0)
            print(song)
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
        """Get the current playback time in milliseconds."""
        return self.media_player.get_time()

    def get_length(self):
        """Get the total length of the media in milliseconds."""
        return self.media_player.get_length()

    def is_playing(self):
        """Check if the media is playing."""
       
        return self.media_player.is_playing()
        

    def print_queue(self):
        """Print the current queue of media files."""
        if self.queue:
            print("Current queue:")
            for idx, media_path in enumerate(self.queue):
                print(f"{idx + 1}. {media_path}")
        else:
            print("Queue is empty!")

    def get_queue(self):
        """Return the current queue of media files."""
        return self.queue

    def skip(self):
        """Skip the current media and play the next in the queue."""
        if self.media_player.is_playing():
            self.stop()  # Stop current media
            self.play_next()  # Play next in queue
        elif self.queue:
            self.play_next()  # Play next in queue directly if paused or stopped

    def on_end_reached(self, event):
        """Callback function for when end of media is reached."""
        print("End of media reached!")
        #self.stop()
        
        self.play_next()

    def monitor_progress(self):
        """Monitor progress of the current media."""
        while True:
            if self.is_playing():
                position = self.media_player.get_position()
                print(f"Current position: {position}")
                time.sleep(1)
            else:
                time.sleep(0.1)

# Example usage
if __name__ == "__main__":
    # Create an instance of the MusicPlayer
    player = MusicPlayer("./music")

    # Add media files to the queue
    player.add_to_queue("Sad Trombone")
    player.add_to_queue("ICH ICH ICH")

    # Print the current queue
    player.print_queue()

    # Start playing the media from the queue
    player.play()
    #time.sleep(3)
    #player.skip()
    # Monitor progress of the current media
    player.monitor_progress()
