#!/usr/bin/env python3
"""
AstrOS - AI-Integrated Operating System v1.1.6
Real AI Integration - Universal AI Assistant that answers ANY question using API directly
"""

import asyncio
import sys
import os
import re
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Suppress logs for clean user experience
logging.basicConfig(level=logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import required packages with proper error handling
def ensure_packages():
    """Ensure required packages are installed"""
    try:
        import httpx
        from openai import AsyncOpenAI
        return httpx, AsyncOpenAI
    except ImportError:
        print("📦 Required packages not found. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "openai", "--quiet"])
            import httpx
            from openai import AsyncOpenAI
            print("✅ Packages installed successfully!")
            return httpx, AsyncOpenAI
        except Exception as install_error:
            print(f"❌ Failed to install packages: {install_error}")
            print("Please run: pip install httpx openai")
            sys.exit(1)

# Get the packages
httpx, AsyncOpenAI = ensure_packages()


class UniversalAIClient:
    """Universal AI client that answers ANY question using multiple free APIs"""
    
    def __init__(self):
        # Multiple free models to try
        self.models = [
            "openai/gpt-oss-20b:free",
            "x-ai/grok-4-fast:free",
            "qwen/qwen-2.5-72b-instruct:free",
            "meta-llama/llama-3.2-11b-vision-instruct:free", 
            "microsoft/phi-3-medium-128k-instruct:free",
            "google/gemma-2-27b-it:free",
            "mistralai/mistral-7b-instruct:free"
        ]
        
        # Multiple API keys to try
        self.api_keys = [
            "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",
            "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"
        ]
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.current_model = 0
        self.current_key = 0
        self.client = None
        self.successful_config = None
        
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize the OpenAI client"""
        try:
            self.client = AsyncOpenAI(
                api_key=self.api_keys[self.current_key],
                base_url=self.base_url,
                timeout=15.0,
                max_retries=1
            )
        except Exception:
            pass
    
    async def get_real_ai_answer(self, question: str) -> Optional[str]:
        """Get real AI answer from API - tries all combinations"""
        
        for key_idx in range(len(self.api_keys)):
            for model_idx in range(len(self.models)):
                try:
                    # Update client with current key
                    self.current_key = key_idx
                    self.current_model = model_idx
                    self.initialize_client()
                    
                    current_model = self.models[self.current_model]
                    
                    # Make API call
                    response = await self.client.chat.completions.create(
                        model=current_model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are AstrOS, an intelligent AI assistant. Provide clear, accurate, and helpful answers to any question. Be informative and conversational."
                            },
                            {
                                "role": "user", 
                                "content": question
                            }
                        ],
                        max_tokens=800,
                        temperature=0.7
                    )
                    
                    answer = response.choices[0].message.content.strip()
                    if answer and len(answer) > 10:  # Valid response
                        self.successful_config = (key_idx, model_idx)
                        return f"{answer}\n\n💡 *Powered by AstrOS*"
                
                except Exception as e:
                    error_str = str(e).lower()
                    # Continue trying other combinations
                    continue
        
        return None  # All combinations failed
    
    async def get_smart_local_answer(self, question: str) -> str:
        """Enhanced local responses when API fails"""
        q = question.lower().strip()
        
        # Extensive knowledge base
        knowledge = {
            "ayurveda": "Ayurveda is an ancient Indian system of medicine dating back over 5,000 years. It emphasizes balance between mind, body, and spirit through natural approaches including herbal medicines, dietary guidelines, yoga, meditation, and lifestyle practices. Ayurveda identifies three doshas (Vata, Pitta, Kapha) that govern physiological and psychological functions.",
            
            "paris": "Paris is the capital and largest city of France, located in north-central France on the Seine River. Known as 'The City of Light,' it's famous for the Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, Arc de Triomphe, and Champs-Élysées. Paris is a global center for art, fashion, gastronomy, and culture.",
            
            "ai": "Artificial Intelligence (AI) is the simulation of human intelligence in machines programmed to think, learn, and problem-solve. It includes machine learning, deep learning, natural language processing, and computer vision. AI is transforming industries from healthcare to transportation.",
            
            "machine learning": "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make predictions or decisions.",
            
            "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. Known for its simple syntax and readability, it's widely used in web development, data science, AI/ML, automation, and scientific computing.",
            
            "wifi": "WiFi (Wireless Fidelity) is a wireless networking technology that allows devices to connect to the internet and communicate with each other. Regarding security, I must emphasize that attempting to access networks without authorization is illegal and unethical.",
            
            "hack": "I cannot and will not provide guidance on hacking, unauthorized access to systems, or any illegal activities. Instead, I'd be happy to discuss ethical cybersecurity practices, legitimate penetration testing, or how to secure your own networks.",
            
            "computer": "A computer is an electronic device that processes data according to instructions (programs). It consists of hardware (CPU, memory, storage, input/output devices) and software (operating system, applications) working together to perform various tasks.",
            
            "science": "Science is the systematic study of the natural world through observation, experimentation, and analysis. It includes fields like physics, chemistry, biology, astronomy, and earth sciences, helping us understand how the universe works.",
            
            "technology": "Technology refers to the application of scientific knowledge and tools to solve problems and improve human life. It encompasses everything from simple tools to complex systems like computers, smartphones, and artificial intelligence."
        }
        
        # Check direct matches in knowledge base
        for key, value in knowledge.items():
            if key in q:
                return f"{value}\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Handle question patterns
        if any(pattern in q for pattern in ["what is", "tell me about", "explain", "define"]):
            # Extract topic from question
            topic = q
            for remove_word in ["what is", "tell me about", "explain", "define", "the", "a", "an", "?", "."]:
                topic = topic.replace(remove_word, "").strip()
            
            if topic:
                return f"Great question about '{topic}'! This is an interesting topic that spans multiple areas of knowledge. While I have extensive information on many subjects, for the most comprehensive and up-to-date details about {topic}, I'd recommend checking authoritative sources or educational resources. I'm happy to help with other questions or provide information on topics I'm more familiar with!\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Personal/Identity questions
        if any(phrase in q for phrase in ["who are you", "what are you", "about yourself"]):
            return "I'm AstrOS, your intelligent AI assistant! I'm designed to help answer questions, provide information, perform calculations, and assist with various tasks. I have knowledge across many topics and I'm always here to help make your day easier and more productive.\n\n🧠 *Enhanced Local Knowledge Base*"
        
        if any(phrase in q for phrase in ["how are you", "how do you do", "how's it going"]):
            return "I'm doing wonderfully, thank you for asking! I'm running smoothly and ready to help you with any questions or tasks you have. My systems are all functioning perfectly and I'm excited to assist you today. What would you like to explore or learn about?\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Capability questions
        if any(phrase in q for phrase in ["what can you do", "capabilities", "features", "help me"]):
            return "I'm capable of many things! I can:\n\n• Answer questions on a wide variety of topics\n• Perform mathematical calculations\n• Provide information about science, technology, history, and culture\n• Help with explanations and definitions\n• Engage in natural conversations\n• Assist with problem-solving\n\nJust ask me anything you're curious about - I'm here to help!\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Mathematical expressions
        if self.is_math_expression(question):
            try:
                result = self.calculate(question)
                return f"The calculation result is: {result}\n\n🧠 *Enhanced Local Knowledge Base*"
            except:
                return f"I can see this looks like a math problem: '{question}'. Let me help with the calculation, though I might need the expression in a clearer format.\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Gratitude responses
        if any(word in q for word in ["thank", "thanks", "appreciate"]):
            return "You're very welcome! I'm delighted to help and I really appreciate your kind words. Please don't hesitate to ask if you have any other questions - I'm always here and ready to assist!\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Farewell responses
        if any(word in q for word in ["bye", "goodbye", "see you", "farewell"]):
            return "Goodbye! It's been wonderful chatting with you. Feel free to come back anytime if you need assistance or just want to have a conversation. Take care!\n\n🧠 *Enhanced Local Knowledge Base*"
        
        # Default intelligent response
        return f"That's a fascinating question about '{question}'! I appreciate your curiosity. While I may not have specific details about this particular topic readily available, I'm designed to help with a wide range of subjects. Feel free to ask me about science, technology, mathematics, general knowledge, or anything else you're wondering about!\n\n🧠 *Enhanced Local Knowledge Base*"
    
    def is_math_expression(self, text: str) -> bool:
        """Check if text contains a mathematical expression"""
        # Pattern for basic math expressions
        math_pattern = r'^[\d\s\+\-\*\/\(\)\.]+$'
        has_operator = r'[\+\-\*\/]'
        
        text = text.strip()
        return bool(re.match(math_pattern, text) and re.search(has_operator, text) and len(text) > 2)
    
    def calculate(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Clean and validate the expression
            clean_expr = re.sub(r'[^\d\+\-\*\/\(\)\.\s]', '', expression.strip())
            
            # Simple evaluation for basic math
            result = eval(clean_expr)
            return str(float(result)) if isinstance(result, (int, float)) else str(result)
        except:
            raise ValueError("Invalid mathematical expression")


class EnhancedAstrOSAgent:
    """Enhanced AstrOS Agent with Universal AI Integration"""
    
    def __init__(self):
        self.ai_client = UniversalAIClient()
        self.conversation_count = 0
        
    async def get_response(self, question: str) -> str:
        """Get the best possible response to any question"""
        self.conversation_count += 1
        
        try:
            # PRIORITY 1: Always try real AI first
            ai_response = await self.ai_client.get_real_ai_answer(question)
            if ai_response:
                return ai_response
            
            # FALLBACK: Use enhanced local intelligence
            return await self.ai_client.get_smart_local_answer(question)
            
        except Exception as e:
            # Error fallback with more details
            # Always try local fallback
            try:
                return await self.ai_client.get_smart_local_answer(question)
            except Exception as fallback_error:
                return f"I encountered a technical issue, but I'm still here to help! Please try rephrasing your question or ask me something else. I'm designed to assist with a wide variety of topics and I'm ready to help you.\n\n🔧 *Error Recovery Mode*"


async def run_interactive():
    """Run interactive mode with universal AI"""
    print("🚀 AstrOS Universal AI Assistant")
    print("=" * 60)
    print("🤖 Real AI Integration - Answers ANY Question!")
    print("🧠 Multiple AI Models + Enhanced Local Intelligence")
    print("💡 Ask me absolutely anything!")
    print("=" * 60)
    print("\n✅ Ready! Ask me any question...")
    print("\n💡 Try asking about:")
    print("   • Any topic: 'What is quantum physics?'")
    print("   • Calculations: 'Calculate 456 * 789'")
    print("   • Explanations: 'Explain machine learning'")
    print("   • Current events: 'Tell me about recent discoveries'")
    print("   • Anything else you're curious about!")
    print("\n🔚 Type 'quit' or 'exit' to stop")
    print("-" * 60)
    
    agent = EnhancedAstrOSAgent()
    
    while True:
        try:
            # Get user input
            user_question = input("\n🌟 You: ").strip()
            
            # Handle exit commands
            if user_question.lower() in ['quit', 'exit', 'bye', 'goodbye', 'stop']:
                print("👋 Thank you for using AstrOS! Goodbye!")
                break
            
            # Skip empty input
            if not user_question:
                continue
            
            # Get and display response
            response = await agent.get_response(user_question)
            print(f"\n🤖 AstrOS: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using AstrOS!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error occurred: {str(e)}. Please try again!")


def main():
    """Main entry point for AstrOS Universal AI Assistant"""
    asyncio.run(run_interactive())


if __name__ == "__main__":
    main()