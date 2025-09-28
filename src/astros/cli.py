"""
AstrOS Command Line Interface
"""
import asyncio
import click
from astros.core.agent import AstrOSAgent
from astros.config.api_config import APIConfig


@click.group()
def cli():
    """AstrOS AI Assistant - GPT-OSS-20B Powered"""
    pass


@cli.command()
@click.option('--config', default=None, help='Configuration file path')
def interactive(config):
    """Start interactive chat mode"""
    async def run_interactive():
        agent = AstrOSAgent(config) 
        await agent.initialize()
        
        print("🚀 AstrOS Interactive Mode")
        print("🤖 Ask me anything! Type 'quit' to exit.")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n🌟 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                print("🤖 AstrOS: ", end="", flush=True)
                response = await agent.process_command(user_input)
                
                if response['success']:
                    print(response['message'])
                else:
                    print(f"❌ {response['message']}")
                    
            except KeyboardInterrupt:
                break
        
        await agent.shutdown()
    
    asyncio.run(run_interactive())


@cli.command()
def demo():
    """Run a quick demonstration"""
    async def run_demo():
        agent = AstrOSAgent()
        await agent.initialize()
        
        demos = [
            "Hello! What can you do?",
            "Calculate 25 * 47 + 123", 
            "Explain machine learning briefly"
        ]
        
        print("🎬 AstrOS Demo")
        print("=" * 30)
        
        for i, query in enumerate(demos, 1):
            print(f"\n🔸 Demo {i}: {query}")
            response = await agent.process_command(query)
            print(f"🤖 {response['message']}")
            await asyncio.sleep(1)
        
        await agent.shutdown()
    
    asyncio.run(run_demo())


@cli.command()
def status():
    """Show AstrOS configuration and status"""
    config = APIConfig.get_config_summary()
    
    print("🔧 AstrOS Status")
    print("=" * 25)
    print(f"API Configured: {'✅' if config['api_key_set'] else '❌'}")
    print(f"Model: {config['model']}")
    print(f"Endpoint: {config['base_url']}")
    print(f"Max Tokens: {config['max_tokens']}")
    
    if config['api_key_set']:
        print("🚀 Ready for intelligent responses!")
    else:
        print("⚠️  Set ASTROS_OPENAI_API_KEY for full features")


@cli.command()
def interactive():
    """Start interactive mode"""
    async def interactive_loop():
        agent = AstrOSAgent()
        await agent.initialize()
        
        print("🚀 AstrOS Interactive Mode - Stage 2 (Voice Enabled)")
        print("Available commands: hello, status, help, system info, quit")
        print("Voice commands: voice, speak, voice-status")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                command = input("astros> ")
                if command.lower().strip() in ['quit', 'exit']:
                    break
                
                if not command.strip():
                    continue
                
                response = await agent.process_command(command)
                print(f"Response: {response['message']}")
                print()
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        await agent.shutdown()
        print("AstrOS Agent stopped.")
    
    asyncio.run(interactive_loop())


@cli.command()
def status():
    """Show AstrOS status"""
    async def show_status():
        agent = AstrOSAgent()
        await agent.initialize()
        
        voice_status = await agent.get_voice_status()
        
        print("🚀 AstrOS Status")
        print("================")
        print("Version: 0.1.0 (Stage 2 - Voice Enabled)")
        print("Status: Development")
        print("Components: Core Agent, AI Integration, Voice Processing")
        print(f"OpenAI Integration: {'✅ Enabled' if agent.openai_client and agent.openai_client.is_available() else '❌ Disabled'}")
        print(f"Voice Processing: {'✅ Available' if voice_status['voice_available'] else '❌ Not Available'}")
        print()
        print("Available Commands:")
        print("• astros interactive - Text-based interaction")
        print("• astros voice - Voice-based interaction")
        print("• astros speak - Test text-to-speech")
        print("• astros voice-status - Check voice system status")
        print("• astros agent - Start background agent")
        
        await agent.shutdown()
    
    asyncio.run(show_status())


@cli.command()
def voice():
    """Start voice interactive mode"""
    async def voice_loop():
        agent = AstrOSAgent()
        await agent.initialize()
        
        print("🎤 AstrOS Voice Mode")
        print("===================")
        print("Say commands naturally - the agent will listen and respond")
        print("Available commands: hello, status, help, system info, quit")
        print("Type 'quit' to exit voice mode")
        print("-" * 50)
        
        while True:
            try:
                # Wait for user input to start listening
                command = input("Press Enter to start listening (or 'quit' to exit): ")
                if command.lower().strip() in ['quit', 'exit']:
                    break
                
                print("🎤 Listening... (5 seconds)")
                response = await agent.process_voice_command(duration=5)
                
                if response.get('voice_input'):
                    print(f"You said: {response['voice_input']}")
                
                print(f"Agent: {response['message']}")
                
                if not response.get('spoken', False):
                    print("(Voice output not available)")
                
                print()
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        await agent.shutdown()
        print("Voice mode stopped.")


@cli.command()
def speak():
    """Test text-to-speech"""
    async def speak_test():
        agent = AstrOSAgent()
        await agent.initialize()
        
        test_text = "Hello! This is a test of the text-to-speech system."
        print(f"Speaking: {test_text}")
        
        success = await agent.speak_response(test_text)
        if success:
            print("Speech completed successfully")
        else:
            print("Speech failed or not available")
        
        await agent.shutdown()
    
    asyncio.run(speak_test())


@cli.command()
def voice_status():
    """Show voice processing status"""
    async def status_check():
        agent = AstrOSAgent()
        await agent.initialize()
        
        status = await agent.get_voice_status()
        
        print("🎤 AstrOS Voice Status")
        print("=====================")
        print(f"Voice Processing: {'✅ Available' if status['voice_available'] else '❌ Not Available'}")
        print(f"Speech-to-Text: {'✅ Available' if status['stt_available'] else '❌ Not Available'}")
        print(f"Text-to-Speech: {'✅ Available' if status['tts_available'] else '❌ Not Available'}")
        print(f"Audio Recording: {'✅ Available' if status['recording_available'] else '❌ Not Available'}")
        print(f"OpenAI Voice APIs: {'✅ Available' if status['openai_voice'] else '❌ Not Available'}")
        
        if not status['voice_available']:
            print("\nTo enable voice features:")
            print("1. Install voice dependencies: pip install openai-whisper pyaudio pyttsx3")
            print("2. Configure OpenAI API key for Whisper/TTS")
            print("3. Ensure microphone permissions are granted")
        
        await agent.shutdown()
    
    asyncio.run(status_check())


def main():
    cli()


if __name__ == "__main__":
    main()