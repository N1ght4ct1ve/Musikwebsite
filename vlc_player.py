import vlc
import time

class MusicPlayer:
    def __init__(self, media_path):
        # Create a VLC media player object
        self.media_player = vlc.MediaPlayer()
        
        # Create a media object
        self.media = vlc.Media(media_path)
        
        # Set the media to the media player
        self.media_player.set_media(self.media)
        
        # Set initial volume
        self.media_player.audio_set_volume(100)
        
    def play(self):
        """Start playing the media."""
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
    
    def is_playing(self):
        """Check if the media is playing."""
        return self.media_player.is_playing()

# Example usage
if __name__ == "__main__":
    # Create an instance of the MusicPlayer with the path to the media file
    player = MusicPlayer("./KRAFTKLUB - Blaues Licht.mp3")
    
    # Start playing the media
    player.play()
    
    # Wait for 5 seconds
    time.sleep(5)
    
    # Pause the media
    player.pause()
    
    # Wait for 2 seconds
    time.sleep(2)
    
    # Resume playing the media
    player.pause()
    
    # Wait for another 5 seconds
    time.sleep(5)
    
    # Stop the media
    player.stop()
