#!/usr/bin/env python3
"""
AstrOS - Clean Main Entry Point
Launch the AI-powered assistant with GPT-OSS-20B
"""
import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def run_interactive():
    """Run AstrOS in interactive mode"""
    try:
        from astros.core.agent import AstrOSAgent
        from astros.config.api_config import APIConfig
        
        print("🚀 AstrOS AI Assistant")
        print("=" * 40)
        print("🤖 Powered by GPT-OSS-20B")
        print("🧠 API-First Intelligence")
        print("=" * 40)
        
        # Show API status
        config = APIConfig.get_config_summary()
        if config['api_key_set']:
            print(f"✅ API Ready: {config['model']}")
        else:
            print("⚠️  API not configured - using local mode")
        
        # Initialize agent
        print("\n🔄 Starting agent...")
        agent = AstrOSAgent()
        await agent.initialize()
        
        print("✅ Ready! Ask me anything...")
        print("💡 Examples:")
        print("   • 'Explain quantum physics'")
        print("   • 'Write Python code'")
        print("   • 'Calculate 127 * 89'")
        print("   • 'What can you help with?'")
        print("\n🔚 Type 'quit' to exit")
        print("-" * 50)
        
        # Interactive loop
        while True:
            try:
                user_input = input("\n🌟 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 AstrOS: ", end="", flush=True)
                response = await agent.process_command(user_input)
                
                if response['success']:
                    print(response['message'])
                    
                    # Show tokens if available
                    if 'tokens_used' in response:
                        tokens = response['tokens_used']
                        source = response.get('source', 'local')
                        print(f"   📊 [{tokens} tokens, {source}]")
                else:
                    print(f"❌ {response['message']}")
                    
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        await agent.shutdown()
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Please install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Failed to start: {e}")

async def run_demo():
    """Run a quick demo"""
    try:
        from astros.core.agent import AstrOSAgent
        
        print("🎬 AstrOS Quick Demo")
        print("=" * 30)
        
        agent = AstrOSAgent()
        await agent.initialize()
        
        demo_queries = [
            "Hello! What can you do?",
            "Calculate 25 * 47",
            "Explain AI in simple terms"
        ]
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n🔸 Demo {i}: {query}")
            print("-" * 30)
            
            response = await agent.process_command(query)
            
            if response['success']:
                print(f"✅ {response['message']}")
                if 'tokens_used' in response:
                    print(f"📊 [{response['tokens_used']} tokens]")
            else:
                print(f"❌ {response['message']}")
            
            await asyncio.sleep(1)
        
        await agent.shutdown()
        print("\n🎉 Demo complete!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "interactive":
            asyncio.run(run_interactive())
        elif mode == "demo":
            asyncio.run(run_demo())
        else:
            print(f"❌ Unknown mode: {mode}")
            print("💡 Usage: python astros.py [interactive|demo]")
    else:
        print("🚀 AstrOS AI Assistant")
        print("Choose a mode:")
        print("  1. Interactive chat")
        print("  2. Quick demo")
        
        choice = input("\nChoice (1/2): ").strip()
        
        if choice == "1":
            asyncio.run(run_interactive())
        elif choice == "2":
            asyncio.run(run_demo())
        else:
            print("Starting interactive mode...")
            asyncio.run(run_interactive())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")