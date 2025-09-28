"""
Voice processing module for AstrOS
Provides speech-to-text and text-to-speech capabilities using OpenAI APIs
"""
import asyncio
import logging
import io
import wave
import tempfile
import os
import platform
import subprocess
from typing import Optional, Dict, Any
from pathlib import Path

import openai
from openai import AsyncOpenAI
import pyaudio
import pyttsx3
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
    import platform
    import subprocess

from ..config.api_config import APIConfig

logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Voice processing with OpenAI Whisper (STT) and TTS"""

    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None
        self.tts_engine = None
        self.audio = None
        self._setup_clients()

    def _setup_clients(self):
        """Initialize OpenAI client and TTS engine"""
        try:
            # OpenAI client for Whisper and TTS
            api_key = APIConfig.get_api_key()
            if api_key:
                base_url = APIConfig.get_base_url()
                client_kwargs = {"api_key": api_key}

                if base_url:
                    client_kwargs["base_url"] = base_url

                self.client = AsyncOpenAI(**client_kwargs)
                logger.info("OpenAI voice client initialized")
            else:
                logger.warning("OpenAI API key not configured - voice features disabled")

            # Local TTS engine as fallback
            try:
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Set to a more natural voice if available
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                self.tts_engine.setProperty('rate', 180)  # Slightly slower for clarity
                logger.info("Local TTS engine initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize local TTS: {e}")

            # Audio recording setup
            try:
                self.audio = pyaudio.PyAudio()
                logger.info("Audio recording initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize audio recording: {e}")

        except Exception as e:
            logger.error(f"Failed to setup voice clients: {e}")

    def is_available(self) -> bool:
        """Check if voice processing is available"""
        return self.client is not None

    def can_record_audio(self) -> bool:
        """Check if audio recording is available"""
        return self.audio is not None

    def can_speak(self) -> bool:
        """Check if text-to-speech is available"""
        return self.tts_engine is not None or self.client is not None

    async def speech_to_text(self, audio_data: bytes, language: str = "en") -> Optional[str]:
        """Convert speech to text using OpenAI Whisper"""
        if not self.is_available():
            logger.warning("OpenAI client not available for STT")
            return None

        try:
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name

                # Convert raw audio data to WAV format
                with wave.open(temp_file, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(16000)  # 16kHz
                    wav_file.writeframes(audio_data)

            # Transcribe with Whisper
            with open(temp_path, 'rb') as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="text"
                )

            # Clean up temp file
            os.unlink(temp_path)

            return transcript.strip() if transcript else None

        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            return None

    async def text_to_speech_openai(self, text: str, voice: str = "alloy") -> Optional[bytes]:
        """Convert text to speech using OpenAI TTS"""
        if not self.is_available():
            return None

        try:
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                response_format="mp3"
            )

            # Get audio data
            audio_data = b""
            async for chunk in response.aiter_bytes():
                audio_data += chunk

            return audio_data

        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return None

    def text_to_speech_local(self, text: str) -> bool:
        """Convert text to speech using local TTS engine"""
        if not self.tts_engine:
            return False

        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"Local TTS error: {e}")
            return False

    async def speak(self, text: str, use_openai: bool = True) -> bool:
        """Speak text using available TTS method"""
        if use_openai and self.is_available():
            try:
                audio_data = await self.text_to_speech_openai(text)
                if audio_data:
                    # Save audio to temporary file and play it
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                        temp_path = temp_file.name
                        temp_file.write(audio_data)
                    
                    try:
                        # Play the audio file
                        success = self.play_audio_file(temp_path)
                        if success:
                            logger.info(f"Played OpenAI TTS audio for: {text[:50]}...")
                            return True
                        else:
                            logger.warning("Failed to play OpenAI TTS audio")
                    finally:
                        # Clean up temp file
                        try:
                            os.unlink(temp_path)
                        except:
                            pass
                    
            except Exception as e:
                logger.warning(f"OpenAI TTS failed, falling back to local: {e}")

        # Fallback to local TTS
        return self.text_to_speech_local(text)

    def record_audio(self, duration: int = 5, sample_rate: int = 16000) -> Optional[bytes]:
        """Record audio from microphone"""
        if not self.can_record_audio():
            logger.warning("Audio recording not available")
            return None

        try:
            # Audio recording parameters
            chunk = 1024
            format = pyaudio.paInt16
            channels = 1
            rate = sample_rate

            # Open stream
            stream = self.audio.open(
                format=format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=chunk
            )

            logger.info(f"Recording audio for {duration} seconds...")
            frames = []

            # Record audio
            for i in range(0, int(rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(data)

            # Stop and close stream
            stream.stop_stream()
            stream.close()

            # Convert to bytes
            audio_data = b''.join(frames)
            logger.info(f"Recorded {len(audio_data)} bytes of audio")
            return audio_data

        except Exception as e:
            logger.error(f"Audio recording error: {e}")
            return None

    def play_audio_file(self, file_path: str) -> bool:
        """Play an audio file using playsound or system commands"""
        try:
            if PLAYSOUND_AVAILABLE:
                # Use playsound for cross-platform audio playback
                playsound(file_path, block=True)
                return True
            else:
                # Fallback to system commands
                system = platform.system().lower()
                
                if system == "windows":
                    # Use Windows Media Player or PowerShell
                    subprocess.run([
                        "powershell", 
                        "-c", 
                        f'(New-Object Media.SoundPlayer "{file_path}").PlaySync();'
                    ], check=True, capture_output=True)
                elif system == "darwin":  # macOS
                    subprocess.run(["afplay", file_path], check=True, capture_output=True)
                elif system == "linux":
                    # Try common Linux audio players
                    for player in ["mpg123", "aplay", "play"]:
                        try:
                            if player == "aplay":
                                subprocess.run([player, file_path], check=True, capture_output=True)
                            else:
                                subprocess.run([player, file_path], check=True, capture_output=True)
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                    else:
                        logger.warning("No suitable audio player found on Linux")
                        return False
                else:
                    logger.warning(f"Unsupported platform for audio playback: {system}")
                    return False
                    
                return True
            
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
            return False

    def __del__(self):
        """Cleanup resources"""
        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass


# Global voice processor instance
_voice_processor: Optional[VoiceProcessor] = None


def get_voice_processor() -> VoiceProcessor:
    """Get global voice processor instance"""
    global _voice_processor
    if _voice_processor is None:
        _voice_processor = VoiceProcessor()
    return _voice_processor


async def test_voice_features() -> Dict[str, bool]:
    """Test voice processing capabilities"""
    processor = get_voice_processor()

    results = {
        "openai_available": processor.is_available(),
        "recording_available": processor.can_record_audio(),
        "tts_available": processor.can_speak(),
    }

    # Test TTS if available
    if results["tts_available"]:
        try:
            success = await processor.speak("Voice system test successful", use_openai=False)
            results["local_tts_working"] = success
        except:
            results["local_tts_working"] = False
    else:
        results["local_tts_working"] = False

    return results