"""
Enhanced Natural Language Processing for AstrOS with OpenAI Integration
Combines local spaCy processing with OpenAI GPT capabilities
"""
import re
import spacy
import logging
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

if TYPE_CHECKING:
    from .openai_client import OpenAIClient

@dataclass
class Entity:
    """Represents a named entity found in text"""
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0


@dataclass
class Intent:
    """Represents a classified user intent with enhanced metadata"""
    name: str
    confidence: float
    entities: List[Entity]
    parameters: Dict[str, Any]
    reasoning: Optional[str] = None  # GPT reasoning for classification
    source: str = "local"  # "local" or "gpt"


@dataclass
class ProcessedInput:
    """Represents processed user input with enhanced context"""
    original_text: str
    cleaned_text: str
    tokens: List[str]
    entities: List[Entity]
    intent: Optional[Intent] = None
    processing_time: float = 0.0
    used_gpt: bool = False


class EnhancedNLPProcessor:
    """Enhanced NLP processor with OpenAI GPT integration"""
    
    def __init__(self):
        self.logger = logging.getLogger("astros.ai.nlp")
        self.nlp = None
        self.openai_client: Optional['OpenAIClient'] = None
        self.intent_patterns = self._load_enhanced_intent_patterns()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self._initialize_models()
    
    def set_openai_client(self, client: 'OpenAIClient') -> None:
        """Set OpenAI client for enhanced processing"""
        self.openai_client = client
        self.logger.info("OpenAI client connected to NLP processor")
    
    def _initialize_models(self) -> None:
        """Initialize spaCy and other models"""
        try:
            self.logger.info("Loading enhanced NLP models...")
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("spaCy model loaded successfully")
        except OSError:
            self.logger.error("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            raise
    
    def _load_enhanced_intent_patterns(self) -> Dict[str, List[str]]:
        """Load enhanced intent patterns with more sophisticated matching"""
        return {
            "greeting": [
                "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
                "howdy", "greetings", "what's up", "how are you", "nice to meet you",
                "hiya", "yo", "sup", "g'day"
            ],
            "help": [
                "help", "assistance", "support", "guide", "how to", "can you help",
                "i need help", "what can you do", "instructions", "tutorial",
                "explain", "show me", "assist me", "guidance"
            ],
            "conversation": [
                "tell me about", "what do you think", "do you know", "opinion",
                "chat", "talk", "discuss", "conversation", "let's talk",
                "i want to know", "explain to me", "what is", "how does"
            ],
            "file_management": [
                "file", "folder", "directory", "organize files", "create folder",
                "delete file", "move file", "copy file", "list files", "find file",
                "search files", "manage files", "file system", "browse files",
                "open file", "save file", "rename file", "file operations"
            ],
            "system_control": [
                "system info", "system information", "computer info", "hardware",
                "memory", "cpu", "disk space", "run command", "execute", 
                "system command", "check system", "performance", "processes",
                "restart", "reboot", "shutdown system", "system status"
            ],
            "calculation": [
                "calculate", "compute", "math", "add", "subtract", "multiply",
                "divide", "percentage", "what is", "how much", "sum", "total",
                "equation", "formula", "arithmetic", "numbers", "plus", "minus",
                "times", "divided by", "equals", "result"
            ],
            "weather": [
                "weather", "temperature", "forecast", "climate", "rain",
                "sunny", "cloudy", "what's the weather", "weather today",
                "weather report", "will it rain", "temperature today"
            ],
            "time_date": [
                "time", "date", "today", "now", "current time", "what time",
                "what date", "calendar", "when", "schedule", "clock",
                "today's date", "current date", "what day"
            ],
            "shutdown": [
                "shutdown", "exit", "quit", "stop", "close", "goodbye",
                "bye", "terminate", "end", "turn off", "power off"
            ],
            "productivity": [
                "remind me", "schedule", "appointment", "task", "todo",
                "note", "remember", "notification", "calendar event",
                "meeting", "deadline", "priority"
            ],
            "web_search": [
                "search", "look up", "find information", "google", "web search",
                "internet search", "research", "lookup", "browse", "investigate"
            ]
        }
    
    async def process(self, text: str, use_gpt: bool = True) -> ProcessedInput:
        """Enhanced processing with optional GPT integration"""
        import time
        start_time = time.time()
        
        try:
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Tokenize
            tokens = self._tokenize(cleaned_text)
            
            # Extract entities (local first, enhance with GPT if available)
            entities = await self._extract_entities_enhanced(text)
            
            # Classify intent (try GPT first if available, fallback to local)
            intent = await self._classify_intent_enhanced(cleaned_text, entities, use_gpt)
            
            processing_time = time.time() - start_time
            used_gpt = intent.source == "gpt" if intent else False
            
            return ProcessedInput(
                original_text=text,
                cleaned_text=cleaned_text,
                tokens=tokens,
                entities=entities,
                intent=intent,
                processing_time=processing_time,
                used_gpt=used_gpt
            )
        
        except Exception as e:
            self.logger.error(f"Enhanced NLP processing error: {e}")
            # Fallback to basic processing
            return await self._basic_process(text)
    
    async def _classify_intent_enhanced(
        self, 
        text: str, 
        entities: List[Entity], 
        use_gpt: bool = True
    ) -> Optional[Intent]:
        """Enhanced intent classification with GPT integration"""
        
        # Try GPT classification first if available
        if use_gpt and self.openai_client and self.openai_client.is_available():
            try:
                possible_intents = list(self.intent_patterns.keys())
                intent_name, confidence, parameters = await self.openai_client.classify_intent_advanced(
                    text, possible_intents
                )
                
                if confidence > 0.6:  # Trust GPT if confident
                    return Intent(
                        name=intent_name,
                        confidence=confidence,
                        entities=entities,
                        parameters=parameters,
                        reasoning=f"GPT classified with {confidence:.2f} confidence",
                        source="gpt"
                    )
            except Exception as e:
                self.logger.warning(f"GPT intent classification failed: {e}")
        
        # Fallback to local classification
        return await self._classify_intent_local(text, entities)
    
    async def _classify_intent_local(self, text: str, entities: List[Entity]) -> Optional[Intent]:
        """Local intent classification using pattern matching"""
        text_lower = text.lower()
        best_intent = None
        best_score = 0.0
        
        for intent_name, patterns in self.intent_patterns.items():
            score = 0.0
            matched_patterns = []
            
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    # Weight longer patterns more heavily
                    pattern_weight = len(pattern.split()) * 0.2 + 0.8
                    score += pattern_weight
                    matched_patterns.append(pattern)
            
            # Don't normalize by total patterns - just use raw match score
            # This gives better results for intent classification
            if matched_patterns and score > best_score:
                best_score = score
                best_intent = intent_name
        
        if best_intent and best_score > 0.5:
            parameters = self._extract_parameters_enhanced(best_intent, text, entities)
            return Intent(
                name=best_intent,
                confidence=best_score,
                entities=entities,
                parameters=parameters,
                source="local"
            )
        
        return None
    
    async def _extract_entities_enhanced(self, text: str) -> List[Entity]:
        """Enhanced entity extraction with GPT support"""
        entities = []
        
        # Local spaCy extraction
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.8
                ))
        
        # Enhance with GPT if available
        if self.openai_client and self.openai_client.is_available():
            try:
                entity_types = ["NUMBER", "DATE", "TIME", "PERSON", "ORG", "GPE", "MONEY", "PERCENT"]
                gpt_entities = await self.openai_client.extract_entities_advanced(text, entity_types)
                
                # Add GPT entities that don't overlap with spaCy entities
                for entity_type, entity_list in gpt_entities.items():
                    for entity_text in entity_list:
                        if not any(e.text.lower() == entity_text.lower() for e in entities):
                            entities.append(Entity(
                                text=entity_text,
                                label=entity_type.upper(),
                                start=text.lower().find(entity_text.lower()),
                                end=text.lower().find(entity_text.lower()) + len(entity_text),
                                confidence=0.9
                            ))
            except Exception as e:
                self.logger.warning(f"GPT entity extraction failed: {e}")
        
        return entities
    
    def _extract_parameters_enhanced(self, intent: str, text: str, entities: List[Entity]) -> Dict[str, Any]:
        """Enhanced parameter extraction with better context understanding"""
        parameters = {}
        
        try:
            if intent == "calculation":
                # Enhanced mathematical expression extraction
                numbers = [e.text for e in entities if e.label in ["NUMBER", "CARDINAL"]]
                parameters["numbers"] = numbers
                
                # Extract operators with better pattern recognition
                operators = []
                operator_patterns = {
                    "add": [r"\+", r"\badd\b", r"\bplus\b", r"\bsum\b"],
                    "subtract": [r"\-", r"\bsubtract\b", r"\bminus\b", r"\btake away\b"],
                    "multiply": [r"\*", r"×", r"\bmultiply\b", r"\btimes\b", r"\bof\b"],
                    "divide": [r"/", r"÷", r"\bdivide\b", r"\bdivided by\b", r"\binto\b"],
                    "percentage": [r"%", r"\bpercent\b", r"\bpercentage\b"]
                }
                
                for op_name, patterns in operator_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, text, re.IGNORECASE):
                            operators.append(op_name)
                            break
                
                parameters["operators"] = operators
                
                # Enhanced expression extraction
                math_patterns = [
                    r'[\d\+\*\/\(\)\.\s-]+(?:[=\s]*[\d\.]+)?',
                    r'\d+\.?\d*\s*[\+\*\/-]\s*\d+\.?\d*',
                    r'(?:what\s+is|calculate|compute)\s+([\d\+\*\/\(\)\.\s-]+)',
                ]
                
                for pattern in math_patterns:
                    try:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            expression = match.group(1) if match.lastindex else match.group(0)
                            # Clean up the expression
                            expression = re.sub(r'\b(?:what\s+is|calculate|compute|equals?)\b', '', expression, flags=re.IGNORECASE).strip()
                            if expression:
                                parameters["expression"] = expression
                                break
                    except re.error as e:
                        self.logger.warning(f"Regex pattern error: {e}")
                        continue
            
            elif intent == "file_management":
                # Enhanced file operation detection
                file_paths = [e.text for e in entities if e.label in ["FILE_PATH", "ORG"]]
                parameters["file_paths"] = file_paths
                
                # Detect file operations with better context
                action_patterns = {
                    "create": [r"\bcreate\b", r"\bmake\b", r"\bnew\b", r"\badd\b"],
                    "delete": [r"\bdelete\b", r"\bremove\b", r"\brm\b", r"\berase\b"],
                    "move": [r"\bmove\b", r"\bmv\b", r"\brelocate\b", r"\btransfer\b"],
                    "copy": [r"\bcopy\b", r"\bcp\b", r"\bduplicate\b", r"\bclone\b"],
                    "list": [r"\blist\b", r"\bls\b", r"\bshow\b", r"\bdisplay\b"],
                    "search": [r"\bfind\b", r"\bsearch\b", r"\blocate\b", r"\blook for\b"],
                    "organize": [r"\borganize\b", r"\bsort\b", r"\barrange\b", r"\btidy\b"]
                }
                
                actions = []
                for action_name, patterns in action_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, text, re.IGNORECASE):
                            actions.append(action_name)
                            break
                
                parameters["actions"] = actions
            
            elif intent == "system_control":
                # Enhanced system command detection
                command_patterns = {
                    "info": [r"\binfo\b", r"\binformation\b", r"\bstatus\b", r"\bdetails\b"],
                    "performance": [r"\bperformance\b", r"\bcpu\b", r"\bmemory\b", r"\bram\b"],
                    "processes": [r"\bprocess\b", r"\btask\b", r"\brunning\b", r"\bservice\b"],
                    "disk": [r"\bdisk\b", r"\bstorage\b", r"\bspace\b", r"\bdrive\b"]
                }
                
                commands = []
                for cmd_name, patterns in command_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, text, re.IGNORECASE):
                            commands.append(cmd_name)
                            break
                
                parameters["commands"] = commands
            
            elif intent == "time_date":
                # Extract time/date context
                time_entities = [e.text for e in entities if e.label in ["DATE", "TIME"]]
                parameters["time_references"] = time_entities
                
                # Detect specific time queries
                if re.search(r'\bwhat\s+time\b', text, re.IGNORECASE):
                    parameters["query_type"] = "current_time"
                elif re.search(r'\bwhat\s+date\b', text, re.IGNORECASE):
                    parameters["query_type"] = "current_date"
                else:
                    parameters["query_type"] = "general"
            
        except Exception as e:
            self.logger.warning(f"Parameter extraction error for intent {intent}: {e}")
        
        return parameters
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning with better preprocessing"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Normalize quotation marks
        text = re.sub(r'[""]', '"', text)
        text = re.sub(r"['']", "'", text)
        
        # Handle contractions better
        contractions = {
            "won't": "will not",
            "can't": "cannot",
            "n't": " not",
            "'re": " are",
            "'ve": " have",
            "'ll": " will",
            "'d": " would",
            "'m": " am"
        }
        
        for contraction, expansion in contractions.items():
            text = re.sub(contraction, expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Enhanced tokenization"""
        if self.nlp:
            doc = self.nlp(text)
            return [token.text for token in doc if not token.is_space]
        else:
            # Fallback tokenization
            return text.split()
    
    async def _basic_process(self, text: str) -> ProcessedInput:
        """Basic processing fallback"""
        return ProcessedInput(
            original_text=text,
            cleaned_text=text.strip(),
            tokens=text.split(),
            entities=[],
            intent=Intent(
                name="conversation",
                confidence=0.5,
                entities=[],
                parameters={},
                source="fallback"
            ),
            processing_time=0.0,
            used_gpt=False
        )


class EnhancedResponseGenerator:
    """Enhanced response generator with GPT integration"""
    
    def __init__(self):
        self.logger = logging.getLogger("astros.ai.response")
        self.openai_client: Optional['OpenAIClient'] = None
        self.response_templates = self._load_response_templates()
    
    def set_openai_client(self, client: 'OpenAIClient') -> None:
        """Set OpenAI client for enhanced response generation"""
        self.openai_client = client
        self.logger.info("OpenAI client connected to response generator")
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load enhanced response templates"""
        return {
            "greeting": [
                "Hello! I'm AstrOS, your AI assistant. How can I help you?",
                "Hi there! What would you like me to help you with today?",
                "Greetings! I'm here to assist you with various tasks.",
                "Hello! Ready to help with your computing needs.",
                "Hi! I'm AstrOS, your intelligent assistant. What can I do for you?"
            ],
            "help": [
                "I can help you with file management, calculations, system information, and more. Try asking me to 'organize my files' or 'calculate 25 * 4'.",
                "I'm here to assist! I can handle file operations, mathematical calculations, system queries, and general conversation. What would you like to try?",
                "Available features: file management, calculations, system information, web searches, and intelligent conversation. How can I help?",
                "I can assist with various tasks including file organization, mathematical computations, system monitoring, and more. What interests you?"
            ],
            "calculation": [
                "The result is {result}.",
                "That equals {result}.",
                "The answer is {result}.",
                "Computing... the result is {result}."
            ],
            "system_info": [
                "Here's your system information:",
                "System details retrieved:",
                "Current system status:",
                "System information summary:"
            ],
            "error": [
                "I encountered an error processing that request.",
                "Sorry, something went wrong with that operation.",
                "I'm having trouble with that request right now.",
                "There was an issue processing your command."
            ],
            "unknown": [
                "I'm not sure how to handle that request. Could you try rephrasing?",
                "That's not something I can help with yet. Try asking about files, calculations, or system information.",
                "I don't understand that command. Try 'help' to see what I can do.",
                "Could you clarify what you'd like me to do?"
            ]
        }
    
    async def generate_response(
        self, 
        intent: Intent, 
        result_data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        use_gpt: bool = True
    ) -> str:
        """Generate enhanced response with optional GPT enhancement"""
        
        # Try GPT enhancement first if available
        if use_gpt and self.openai_client and self.openai_client.is_available() and intent.source == "gpt":
            try:
                # GPT already generated a good response in the intent classification
                return intent.reasoning or "I've processed your request."
            except Exception as e:
                self.logger.warning(f"GPT response generation failed: {e}")
        
        # Fallback to template-based responses
        return self._generate_template_response(intent, result_data, error)
    
    def _generate_template_response(
        self, 
        intent: Intent, 
        result_data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> str:
        """Generate response using templates"""
        
        if error:
            templates = self.response_templates.get("error", ["An error occurred."])
            return np.random.choice(templates)
        
        intent_name = intent.name if intent else "unknown"
        templates = self.response_templates.get(intent_name, self.response_templates["unknown"])
        
        response = np.random.choice(templates)
        
        # Fill in template variables
        if result_data:
            try:
                response = response.format(**result_data)
            except (KeyError, ValueError):
                # If formatting fails, append the data
                if "result" in result_data:
                    response = f"{response} {result_data['result']}"
        
        return response


# Backwards compatibility aliases
NLPProcessor = EnhancedNLPProcessor
ResponseGenerator = EnhancedResponseGenerator