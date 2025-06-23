"""Text-to-speech module using ElevenLabs API and PyAudio for real-time streaming."""

import os
import threading
import requests
import pyaudio
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Speaker:
    """Handles text-to-speech using ElevenLabs API with PyAudio streaming."""
    
    def __init__(self):
        """Initialize the speaker with API credentials and audio settings."""
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = "MphrLyAczpXnJIuHd3sx"  # WIL voice from speak.py
        self.model = "eleven_flash_v2_5"
        
        # Audio settings
        self.chunk_size = 1024
        self.sample_rate = 44100
        self.channels = 1
        self.sample_width = 2  # 16-bit audio
        
        # PyAudio instance
        self.pyaudio = None
        self.stream = None
        
        # Thread for async playback
        self.playback_thread = None
        
        # Check if API key is available
        if not self.api_key:
            print("Warning: ELEVENLABS_API_KEY not found in .env file. Speech disabled.")
    
    def speak(self, text: str, async_mode: bool = True) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: The text to speak
            async_mode: If True, play audio in background thread
            
        Returns:
            True if speech started successfully, False otherwise
        """
        if not self.api_key:
            return False
            
        if async_mode:
            # Start playback in background thread
            self.playback_thread = threading.Thread(
                target=self._stream_and_play,
                args=(text,),
                daemon=True
            )
            self.playback_thread.start()
            return True
        else:
            # Blocking playback
            return self._stream_and_play(text)
    
    def _stream_and_play(self, text: str) -> bool:
        """Stream audio from ElevenLabs API and play it."""
        try:
            # Initialize PyAudio
            self.pyaudio = pyaudio.PyAudio()
            
            # Open audio stream
            self.stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.chunk_size
            )
            
            # Prepare API request
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
            headers = {
                "Accept": "audio/mpeg",
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": text,
                "model_id": self.model,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            # Make streaming request
            response = requests.post(url, headers=headers, json=data, stream=True)
            
            if response.ok:
                # Play audio chunks as they arrive
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        self.stream.write(chunk)
                return True
            else:
                print(f"Speech error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Speech playback error: {e}")
            return False
        finally:
            # Clean up
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.pyaudio:
                self.pyaudio.terminate()
    
    def wait_for_completion(self):
        """Wait for async playback to complete."""
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join()