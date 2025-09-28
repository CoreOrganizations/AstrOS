"""
Voice Plugin for AstrOS
Handles voice-related intents and operations
"""
import logging
from typing import Dict, Any
from astros.plugins.base import BasePlugin, ExecutionResult


class VoicePlugin(BasePlugin):
    """Plugin for voice operations"""

    name = "voice"
    version = "1.0.0"
    description = "Handles voice input/output operations"
    author = "AstrOS Team"
    handled_intents = ["voice_command", "listen", "speak", "voice_status"]

    def __init__(self):
        super().__init__()
        self.voice_processor = None

    async def initialize(self) -> bool:
        """Initialize voice plugin"""
        try:
            from astros.ai.voice_processor import get_voice_processor
            self.voice_processor = get_voice_processor()
            self.logger.info("Voice plugin initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize voice plugin: {e}")
            return False

    async def execute(self, intent_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute voice-related operations"""
        try:
            if intent_name == "voice_command":
                return await self._handle_voice_command(parameters)
            elif intent_name == "listen":
                return await self._handle_listen(parameters)
            elif intent_name == "speak":
                return await self._handle_speak(parameters)
            elif intent_name == "voice_status":
                return await self._handle_voice_status(parameters)
            else:
                return ExecutionResult.error_result(f"Unknown voice intent: {intent_name}")

        except Exception as e:
            self.logger.error(f"Voice plugin execution error: {e}")
            return ExecutionResult.error_result(f"Voice operation failed: {e}")

    async def _handle_voice_command(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Handle voice command processing"""
        duration = parameters.get("duration", 5)

        if not self.voice_processor or not self.voice_processor.can_record_audio():
            return ExecutionResult.error_result("Voice input not available")

        try:
            # This would typically be called from the agent, but we can provide status
            return ExecutionResult.success_result(
                data={"duration": duration, "ready": True},
                message=f"Voice command processing ready for {duration} seconds of audio"
            )
        except Exception as e:
            return ExecutionResult.error_result(f"Voice command setup failed: {e}")

    async def _handle_listen(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Handle listening for voice input"""
        duration = parameters.get("duration", 5)
        language = parameters.get("language", "en")

        if not self.voice_processor or not self.voice_processor.can_record_audio():
            return ExecutionResult.error_result("Audio recording not available")

        try:
            # Record and transcribe
            transcribed_text = await self.voice_processor.listen_and_transcribe(duration, language)

            if transcribed_text:
                return ExecutionResult.success_result(
                    data={
                        "transcribed_text": transcribed_text,
                        "duration": duration,
                        "language": language
                    },
                    message=f"I heard: {transcribed_text}"
                )
            else:
                return ExecutionResult.error_result("Could not transcribe audio")

        except Exception as e:
            return ExecutionResult.error_result(f"Listening failed: {e}")

    async def _handle_speak(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Handle text-to-speech"""
        text = parameters.get("text", "")
        use_openai = parameters.get("use_openai", True)

        if not text:
            return ExecutionResult.error_result("No text provided to speak")

        if not self.voice_processor or not self.voice_processor.can_speak():
            return ExecutionResult.error_result("Text-to-speech not available")

        try:
            success = await self.voice_processor.speak(text, use_openai)

            if success:
                return ExecutionResult.success_result(
                    data={"text": text, "spoken": True},
                    message=f"Spoke: {text}"
                )
            else:
                return ExecutionResult.error_result("Speech failed")

        except Exception as e:
            return ExecutionResult.error_result(f"Speech error: {e}")

    async def _handle_voice_status(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Handle voice status query"""
        if not self.voice_processor:
            return ExecutionResult.success_result(
                data={"voice_available": False},
                message="Voice processing not initialized"
            )

        status = {
            "voice_available": self.voice_processor.is_available(),
            "stt_available": self.voice_processor.is_available(),
            "tts_available": self.voice_processor.can_speak(),
            "recording_available": self.voice_processor.can_record_audio(),
            "openai_voice": self.voice_processor.is_available()
        }

        status_message = "Voice Status:\n"
        status_message += f"• Speech-to-Text: {'Available' if status['stt_available'] else 'Not Available'}\n"
        status_message += f"• Text-to-Speech: {'Available' if status['tts_available'] else 'Not Available'}\n"
        status_message += f"• Audio Recording: {'Available' if status['recording_available'] else 'Not Available'}\n"
        status_message += f"• OpenAI Voice APIs: {'Available' if status['openai_voice'] else 'Not Available'}"

        return ExecutionResult.success_result(
            data=status,
            message=status_message
        )

    async def shutdown(self) -> None:
        """Shutdown voice plugin"""
        self.logger.info("Voice plugin shutdown")