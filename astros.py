#!/usr/bin/env python3
"""
AstrOS - Clean AI Assistant using MistralAI Ministral 8B
Environment-based configuration with no hardcoded values
"""

import asyncio
import sys
import os
import re
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

# Import required packages
def ensure_packages():
    """Ensure required packages are installed"""
    try:
        import httpx
        from openai import AsyncOpenAI
        return httpx, AsyncOpenAI
    except ImportError:
        print("📦 Installing required packages...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "openai", "python-dotenv", "--quiet"])
            import httpx
            from openai import AsyncOpenAI
            print("✅ Packages installed successfully!")
            return httpx, AsyncOpenAI
        except Exception as install_error:
            print(f"❌ Failed to install packages: {install_error}")
            print("Please run: pip install httpx openai python-dotenv")
            sys.exit(1)

httpx, AsyncOpenAI = ensure_packages()


class AstrOSAIClient:
    """Clean AI client using mistralai/ministral-8b via OpenRouter"""

    def __init__(self):
        # Load configuration from environment
        self.api_key = os.getenv('ASTROS_API_KEY')
        self.base_url = os.getenv('ASTROS_BASE_URL', 'https://openrouter.ai/api/v1')
        self.model = os.getenv('ASTROS_AI_MODEL__NAME', 'openai/gpt-oss-20b:free')
        self.max_tokens = int(os.getenv('ASTROS_AI_MODEL__MAX_TOKENS', '800'))
        self.temperature = float(os.getenv('ASTROS_AI_MODEL__TEMPERATURE', '0.7'))

        # Validate configuration
        if not self.api_key:
            print("❌ No API key found in .env file!")
            print("💡 Set ASTROS_API_KEY in your .env file")
            print("💡 Get a free API key at: https://openrouter.ai/keys")
            sys.exit(1)

        print(f"🔑 API key loaded from .env file")
        print(f"🎯 Model: {self.model}")

        # Initialize client
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=30.0,
            max_retries=2
        )

    async def get_ai_response(self, question: str, conversation_history: list = None) -> Optional[str]:
        """Get AI response using mistralai/ministral-8b"""
        try:
            # Build messages
            messages = [
                {
                    "role": "system",
                    "content": "You are AstrOS, an intelligent AI assistant. Provide clear, accurate, and helpful answers to any question. Be informative and conversational."
                }
            ]

            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 6 messages

            # Add current question
            messages.append({
                "role": "user",
                "content": question
            })

            # Make API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            answer = response.choices[0].message.content.strip()
            if answer and len(answer) > 10:
                return f"{answer}\n\n💡 *Powered by {self.model}*"

        except Exception as e:
            print(f"❌ API Error: {str(e)[:100]}...")
            return None

        return None

    async def get_local_fallback(self, question: str) -> str:
        """Enhanced local responses when API fails"""
        q = question.lower().strip()

        # Basic knowledge base
        knowledge = {
            "hello": "Hello! I'm AstrOS, your AI assistant powered by mistralai/ministral-8b.",
            "how are you": "I'm doing great! Ready to help with any questions.",
            "what can you do": "I can answer questions, perform calculations, and provide information on many topics.",
            "python": "Python is a high-level programming language known for its simplicity and versatility.",
            "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
        }

        # Check knowledge base
        for key, value in knowledge.items():
            if key in q:
                return f"{value}\n\n🧠 *Local Knowledge Base*"

        # Math calculations
        if self.is_math_expression(question):
            try:
                result = self.calculate(question)
                return f"The calculation result is: {result}\n\n🧠 *Local Calculator*"
            except:
                pass

        # Default response
        return f"That's an interesting question about '{question}'! I'm currently using local processing while the AI service reconnects.\n\n🧠 *Local Processing Mode*"

    def is_math_expression(self, text: str) -> bool:
        """Check if text contains a mathematical expression"""
        math_pattern = r'^[\d\s\+\-\*\/\(\)\.]+$'
        has_operator = r'[\+\-\*\/]'
        text = text.strip()
        return bool(re.match(math_pattern, text) and re.search(has_operator, text) and len(text) > 2)

    def calculate(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            clean_expr = re.sub(r'[^\d\+\-\*\/\(\)\.\s]', '', expression.strip())
            result = eval(clean_expr)
            return str(float(result)) if isinstance(result, (int, float)) else str(result)
        except:
            raise ValueError("Invalid mathematical expression")


class AstrOSAgent:
    """Clean AstrOS Agent with conversation context"""

    def __init__(self):
        self.ai_client = AstrOSAIClient()
        self.conversation_history = []
        self.max_history = 10

    async def get_response(self, question: str) -> str:
        """Get response with conversation context"""
        try:
            # Add user question to history
            self.conversation_history.append({
                "role": "user",
                "content": question
            })

            # Get AI response
            ai_response = await self.ai_client.get_ai_response(question, self.conversation_history)

            if ai_response:
                # Extract response text for history
                response_text = ai_response.split("\n\n💡 *")[0]

                # Add AI response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })

                # Keep history manageable
                if len(self.conversation_history) > self.max_history * 2:
                    self.conversation_history = self.conversation_history[-self.max_history * 2:]

                return ai_response

            # Fallback to local processing
            fallback_response = await self.ai_client.get_local_fallback(question)
            return f"{fallback_response}\n\n🔧 *API temporarily unavailable*"

        except Exception as e:
            return f"❌ Error: {str(e)[:100]}...\n\n💡 Please try again."


async def run_interactive():
    """Run interactive mode"""
    print("🚀 AstrOS Universal AI Assistant v1.3.0")
    print("=" * 60)
    print("🤖 mistralai/ministral-8b - Real AI Integration!")
    print("� API-Only Mode: Every question answered by real AI")
    print("💡 Ask me absolutely anything!")
    print("=" * 60)
    print("\n✅ Ready! Ask me any question...")
    print("\n💡 Try asking about:")
    print("   • Any topic: 'What is quantum physics?'")
    print("   • Calculations: 'Calculate 456 * 789'")
    print("   • Explanations: 'Explain machine learning'")
    print("   • Anything else you're curious about!")
    print("\n🔚 Type 'quit' or 'exit' to stop")
    print("-" * 60)

    agent = AstrOSAgent()

    while True:
        try:
            user_question = input("\n🌟 You: ").strip()

            if user_question.lower() in ['quit', 'exit', 'bye', 'goodbye', 'stop']:
                print("👋 Thank you for using AstrOS! Goodbye!")
                break

            if not user_question:
                continue

            response = await agent.get_response(user_question)
            print(f"\n🤖 AstrOS: {response}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using AstrOS!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}. Please try again!")


def main():
    """Main entry point"""
    asyncio.run(run_interactive())


if __name__ == "__main__":
    main()
