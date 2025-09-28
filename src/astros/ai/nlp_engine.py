"""
Natural Language Processing for AstrOS
Handles text preprocessing, intent classification, and entity recognition
"""
import re
import spacy
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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
    """Represents a classified user intent"""
    name: str
    confidence: float
    entities: List[Entity]
    parameters: Dict[str, Any]


@dataclass
class ProcessedInput:
    """Represents processed user input"""
    original_text: str
    cleaned_text: str
    tokens: List[str]
    entities: List[Entity]
    intent: Optional[Intent] = None


class NLPProcessor:
    """Natural Language Processing engine for AstrOS"""
    
    def __init__(self):
        self.logger = logging.getLogger("astros.ai.nlp")
        self.nlp = None
        self.intent_patterns = self._load_intent_patterns()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize NLP models"""
        try:
            self.logger.info("Loading spaCy model...")
            self.nlp = spacy.load("en_core_web_sm")
            self.logger.info("NLP models loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load NLP models: {e}")
            self.nlp = None
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent classification patterns"""
        return {
            "greeting": [
                "hello", "hi", "hey", "good morning", "good afternoon", 
                "good evening", "greetings", "howdy"
            ],
            "status": [
                "status", "how are you", "are you working", "are you running",
                "what's your status", "system status", "health check"
            ],
            "help": [
                "help", "what can you do", "commands", "instructions",
                "how to use", "guide", "manual", "documentation"
            ],
            "file_management": [
                "file", "folder", "directory", "organize files", "create folder",
                "delete file", "move file", "copy file", "list files", "find file",
                "search files", "manage files", "file system"
            ],
            "system_control": [
                "system info", "system information", "computer info", "hardware",
                "memory", "cpu", "disk space", "run command", "execute", 
                "system command", "check system"
            ],
            "calculation": [
                "calculate", "compute", "math", "add", "subtract", "multiply",
                "divide", "percentage", "what is", "how much", "sum", "total"
            ],
            "weather": [
                "weather", "temperature", "forecast", "climate", "rain",
                "sunny", "cloudy", "what's the weather", "weather today"
            ],
            "time_date": [
                "time", "date", "today", "now", "current time", "what time",
                "what date", "calendar", "when", "schedule"
            ],
            "shutdown": [
                "shutdown", "exit", "quit", "stop", "close", "goodbye",
                "bye", "terminate", "end"
            ]
        }
    
    async def process(self, text: str) -> ProcessedInput:
        """Process user input text"""
        try:
            # Clean and preprocess text
            cleaned_text = self._clean_text(text)
            
            # Tokenize
            tokens = self._tokenize(cleaned_text)
            
            # Extract entities
            entities = await self._extract_entities(text)
            
            # Classify intent
            intent = await self._classify_intent(cleaned_text, entities)
            
            return ProcessedInput(
                original_text=text,
                cleaned_text=cleaned_text,
                tokens=tokens,
                entities=entities,
                intent=intent
            )
        
        except Exception as e:
            self.logger.error(f"Error processing text: {e}")
            return ProcessedInput(
                original_text=text,
                cleaned_text=text,
                tokens=[text],
                entities=[],
                intent=None
            )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\-\.\,\?\!]', '', text)
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if self.nlp:
            doc = self.nlp(text)
            return [token.text for token in doc if not token.is_stop and not token.is_punct]
        else:
            # Fallback tokenization
            return text.split()
    
    async def _extract_entities(self, text: str) -> List[Entity]:
        """Extract named entities from text"""
        entities = []
        
        if not self.nlp:
            return entities
        
        try:
            doc = self.nlp(text)
            
            for ent in doc.ents:
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=1.0  # spaCy doesn't provide confidence scores by default
                ))
            
            # Add custom entity extraction for numbers and file paths
            entities.extend(self._extract_custom_entities(text))
        
        except Exception as e:
            self.logger.error(f"Error extracting entities: {e}")
        
        return entities
    
    def _extract_custom_entities(self, text: str) -> List[Entity]:
        """Extract custom entities like numbers, file paths, etc."""
        entities = []
        
        # Extract numbers
        number_pattern = r'\b\d+(?:\.\d+)?\b'
        for match in re.finditer(number_pattern, text):
            entities.append(Entity(
                text=match.group(),
                label="NUMBER",
                start=match.start(),
                end=match.end(),
                confidence=0.9
            ))
        
        # Extract file paths
        file_pattern = r'[a-zA-Z]?[:\\\/]?(?:[^\s<>:"|?*\\\/]+[\\\/])*[^\s<>:"|?*\\\/]*\.[a-zA-Z0-9]+'
        for match in re.finditer(file_pattern, text):
            entities.append(Entity(
                text=match.group(),
                label="FILE_PATH",
                start=match.start(),
                end=match.end(),
                confidence=0.8
            ))
        
        return entities
    
    async def _classify_intent(self, text: str, entities: List[Entity]) -> Intent:
        """Classify user intent from text and entities"""
        try:
            # Calculate similarity scores for each intent
            intent_scores = {}
            
            for intent_name, patterns in self.intent_patterns.items():
                score = self._calculate_intent_score(text, patterns)
                intent_scores[intent_name] = score
            
            # Find the best matching intent
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[best_intent]
            
            # Extract parameters based on intent and entities
            parameters = self._extract_parameters(best_intent, text, entities)
            
            return Intent(
                name=best_intent,
                confidence=confidence,
                entities=entities,
                parameters=parameters
            )
        
        except Exception as e:
            self.logger.error(f"Error classifying intent: {e}")
            return Intent(
                name="unknown",
                confidence=0.0,
                entities=entities,
                parameters={}
            )
    
    def _calculate_intent_score(self, text: str, patterns: List[str]) -> float:
        """Calculate similarity score between text and intent patterns"""
        try:
            # Simple keyword matching with weights
            score = 0.0
            text_words = set(text.lower().split())
            
            for pattern in patterns:
                pattern_words = set(pattern.lower().split())
                
                # Calculate Jaccard similarity
                intersection = len(text_words.intersection(pattern_words))
                union = len(text_words.union(pattern_words))
                
                if union > 0:
                    jaccard_score = intersection / union
                    score = max(score, jaccard_score)
            
            return score
        
        except Exception:
            return 0.0
    
    def _extract_parameters(self, intent: str, text: str, entities: List[Entity]) -> Dict[str, Any]:
        """Extract parameters based on intent and entities"""
        parameters = {}
        
        try:
            if intent == "calculation":
                # Extract numbers and operators
                numbers = [e.text for e in entities if e.label == "NUMBER"]
                parameters["numbers"] = numbers
                
                # Extract math operations
                operators = []
                if any(op in text for op in ["add", "plus", "+"]):
                    operators.append("add")
                if any(op in text for op in ["subtract", "minus", "-"]):
                    operators.append("subtract")
                if any(op in text for op in ["multiply", "times", "*", "x"]):
                    operators.append("multiply")
                if any(op in text for op in ["divide", "divided by", "/"]):
                    operators.append("divide")
                if any(op in text for op in ["percent", "%"]):
                    operators.append("percentage")
                
                parameters["operators"] = operators
                
                # Extract mathematical expression from the text
                import re
                # Look for mathematical expressions (numbers, operators, parentheses)
                math_pattern = r'[\d\+\-\*\/\(\)\.\s]+(?:[=\s]*[\d\.]+)?'
                math_matches = re.findall(math_pattern, text)
                
                # If we found mathematical expressions, use the longest one
                if math_matches:
                    # Find the longest mathematical expression
                    expression = max(math_matches, key=len).strip()
                    # Remove trailing equals and results if present
                    expression = re.sub(r'\s*=.*$', '', expression)
                    parameters["expression"] = expression
                else:
                    # Fallback: try to extract expression after command words
                    # Remove common calculation command words
                    cleaned = re.sub(r'\b(calculate|compute|what\s+is|how\s+much)\s*', '', text, flags=re.IGNORECASE)
                    parameters["expression"] = cleaned.strip()
            
            elif intent == "file_management":
                # Extract file paths and actions
                file_paths = [e.text for e in entities if e.label == "FILE_PATH"]
                parameters["file_paths"] = file_paths
                
                # Extract file actions
                actions = []
                if any(action in text for action in ["create", "make", "new"]):
                    actions.append("create")
                if any(action in text for action in ["delete", "remove", "rm"]):
                    actions.append("delete")
                if any(action in text for action in ["move", "mv"]):
                    actions.append("move")
                if any(action in text for action in ["copy", "cp"]):
                    actions.append("copy")
                if any(action in text for action in ["list", "ls", "show"]):
                    actions.append("list")
                if any(action in text for action in ["find", "search"]):
                    actions.append("search")
                
                parameters["actions"] = actions
            
            elif intent == "weather":
                # Extract location entities
                locations = [e.text for e in entities if e.label in ["GPE", "LOC"]]
                parameters["locations"] = locations
                
                # Extract time references
                times = [e.text for e in entities if e.label in ["DATE", "TIME"]]
                parameters["times"] = times
            
            # Always include the original text for context
            parameters["original_text"] = text
            
        except Exception as e:
            self.logger.error(f"Error extracting parameters: {e}")
        
        return parameters


class ResponseGenerator:
    """Generates natural language responses"""
    
    def __init__(self):
        self.logger = logging.getLogger("astros.ai.response")
        self.response_templates = self._load_response_templates()
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load response templates for different intents"""
        return {
            "greeting": [
                "Hello! I'm AstrOS, your AI assistant. How can I help you?",
                "Hi there! AstrOS is ready to assist you.",
                "Greetings! What would you like me to help you with today?",
            ],
            "status": [
                "I'm running smoothly and ready to help!",
                "All systems operational. AstrOS v0.1.0 is ready to assist.",
                "Status: Active and ready. How can I help you?",
            ],
            "help": [
                "I can help you with file management, calculations, system information, and more. Try asking me to 'organize my files' or 'calculate 25 * 4'.",
                "Here's what I can do: manage files, perform calculations, check system info, and answer questions. What would you like to try?",
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase that?",
                "I didn't quite get that. Can you try asking in a different way?",
                "That's not something I can help with yet. Try asking about files, calculations, or system information.",
            ],
            "error": [
                "Sorry, I encountered an error processing your request.",
                "Something went wrong. Please try again.",
                "I'm having trouble with that request. Could you try again?",
            ]
        }
    
    def generate_response(self, intent: Intent, result: Any = None, error: str = None) -> str:
        """Generate a natural language response"""
        try:
            if error:
                return self._get_random_template("error") + f" Error: {error}"
            
            templates = self.response_templates.get(intent.name, self.response_templates["unknown"])
            base_response = self._get_random_template_from_list(templates)
            
            # Customize response based on result
            if result and hasattr(result, 'get'):
                if intent.name == "calculation" and "result" in result:
                    base_response = f"The answer is {result['result']}."
                elif intent.name == "system_control" and "info" in result:
                    base_response = f"Here's your system information: {result['info']}"
                elif intent.name == "file_management":
                    if "files_found" in result:
                        count = result.get("count", 0)
                        base_response = f"I found {count} files matching your request."
                    elif "action_completed" in result:
                        base_response = f"File operation completed successfully."
            
            return base_response
        
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I'm having trouble generating a response right now."
    
    def _get_random_template(self, intent_name: str) -> str:
        """Get a random template for an intent"""
        templates = self.response_templates.get(intent_name, self.response_templates["unknown"])
        return self._get_random_template_from_list(templates)
    
    def _get_random_template_from_list(self, templates: List[str]) -> str:
        """Get a random template from a list"""
        import random
        return random.choice(templates)