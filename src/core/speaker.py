"""Text-to-speech module using ElevenLabs API and PyAudio for real-time streaming."""

import os
import threading
import requests
import pyaudio
import queue
import time
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Speaker:
    """Handles text-to-speech using ElevenLabs API with PyAudio streaming."""
    
    def __init__(self):
        """Initialize the speaker with API credentials and audio settings."""
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = "PyBPs4TifElCyta4uF2F"
        self.model = "eleven_turbo_v2_5"
        
        # Audio settings
        self.chunk_size = 4096  # Optimized chunk size
        self.sample_rate = 16000  # Using 16kHz PCM format
        self.channels = 1
        self.sample_width = 2  # 16-bit audio (S16LE)
        self.frames_per_buffer = 2048  # Separate buffer size for PyAudio
        
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
        # For some reason Claude code may insert \ characters in the text so clean the text before speaking.
        text = text.replace( '\\', '' )
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
            
            # Open audio stream with optimized parameters
            self.stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.frames_per_buffer,
                output_device_index=None,  # Use default device
                stream_callback=None  # Blocking mode
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
            
            # Make streaming request with PCM output format
            params = {"output_format": "pcm_16000"}  # Request 16kHz PCM format
            response = requests.post(url, headers=headers, json=data, params=params, stream=True)
            
            if response.ok:
                # Collect all audio data first
                audio_data = b''
                bytes_received = 0
                
                print("Downloading audio...")
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        audio_data += chunk
                        bytes_received += len(chunk)
                
                print(f"Downloaded {bytes_received} bytes, starting playback...")
                
                # Play audio data in properly sized chunks for PyAudio
                # Use frames_per_buffer size for playback
                playback_chunk_size = self.frames_per_buffer * self.sample_width
                
                for i in range(0, len(audio_data), playback_chunk_size):
                    chunk = audio_data[i:i + playback_chunk_size]
                    # Pad the last chunk if needed
                    if len(chunk) < playback_chunk_size:
                        chunk += b'\x00' * (playback_chunk_size - len(chunk))
                    self.stream.write(chunk)
                
                print(f"Speech playback complete")
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