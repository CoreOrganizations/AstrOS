"""
Response Customization System for AstrOS
Allows fine-tuning and customization of LLM responses
"""
import re
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ResponseRule:
    """A rule for customizing responses"""
    name: str
    pattern: str  # Regex pattern to match user input
    system_prompt_addition: str  # Additional system prompt
    response_filter: Optional[str] = None  # Post-process the response
    priority: int = 0  # Higher priority rules are applied first

@dataclass
class ResponseTemplate:
    """A template for specific types of responses"""
    name: str
    intent_patterns: List[str]
    template: str
    variables: Dict[str, Any] = None

class ResponseCustomizer:
    """Customizes and fine-tunes LLM responses"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path("config")
        self.rules: List[ResponseRule] = []
        self.templates: Dict[str, ResponseTemplate] = {}
        self.custom_filters: Dict[str, Callable] = {}
        self.load_customizations()
        
    def load_customizations(self):
        """Load customization rules and templates"""
        try:
            # Load rules from config
            rules_file = self.config_dir / "response_rules.json"
            if rules_file.exists():
                with open(rules_file, 'r', encoding='utf-8') as f:
                    rules_data = json.load(f)
                    for rule_data in rules_data.get('rules', []):
                        rule = ResponseRule(**rule_data)
                        self.rules.append(rule)
                logger.info(f"Loaded {len(self.rules)} response customization rules")
            
            # Load templates
            templates_file = self.config_dir / "response_templates.json"
            if templates_file.exists():
                with open(templates_file, 'r', encoding='utf-8') as f:
                    templates_data = json.load(f)
                    for template_data in templates_data.get('templates', []):
                        template = ResponseTemplate(**template_data)
                        self.templates[template.name] = template
                logger.info(f"Loaded {len(self.templates)} response templates")
            
            # Initialize default rules if none exist
            if not self.rules and not self.templates:
                self._create_default_customizations()
                
        except Exception as e:
            logger.warning(f"Failed to load response customizations: {e}")
            self._create_default_customizations()
    
    def _create_default_customizations(self):
        """Create default customization rules"""
        # Default rules for better responses
        default_rules = [
            ResponseRule(
                name="friendly_greetings",
                pattern=r"\b(hello|hi|hey|greetings)\b",
                system_prompt_addition="Be extra friendly and welcoming. Use a warm, conversational tone.",
                priority=10
            ),
            ResponseRule(
                name="math_problems",
                pattern=r"\b(calculate|compute|math|solve|\+|\-|\*|\/)\b",
                system_prompt_addition="Provide step-by-step mathematical solutions. Show your work clearly.",
                priority=8
            ),
            ResponseRule(
                name="programming_help",
                pattern=r"\b(code|programming|python|javascript|function|class|debug)\b",
                system_prompt_addition="Provide detailed programming help with code examples. Format code blocks properly.",
                priority=7
            ),
            ResponseRule(
                name="explanations",
                pattern=r"\b(explain|what is|how does|why)\b",
                system_prompt_addition="Provide clear, educational explanations. Use examples and analogies when helpful.",
                priority=6
            )
        ]
        
        self.rules = default_rules
        
        # Default templates
        self.templates = {
            "greeting": ResponseTemplate(
                name="greeting",
                intent_patterns=["hello", "hi", "hey", "greetings"],
                template="Hello! I'm AstrOS, your AI assistant. {custom_message} How can I help you today?"
            ),
            "help": ResponseTemplate(
                name="help",
                intent_patterns=["help", "what can you do"],
                template="I can assist you with:\n• {capabilities}\n\nWhat would you like to try?"
            )
        }
    
    def customize_system_prompt(self, user_input: str, base_prompt: str) -> str:
        """Customize system prompt based on user input and rules"""
        # Sort rules by priority (highest first)
        sorted_rules = sorted(self.rules, key=lambda r: r.priority, reverse=True)
        
        customized_prompt = base_prompt
        applied_rules = []
        
        for rule in sorted_rules:
            if re.search(rule.pattern, user_input, re.IGNORECASE):
                customized_prompt += f"\n\nAdditional guidance: {rule.system_prompt_addition}"
                applied_rules.append(rule.name)
        
        if applied_rules:
            logger.debug(f"Applied customization rules: {applied_rules}")
        
        return customized_prompt
    
    def apply_response_filters(self, response: str, user_input: str) -> str:
        """Apply post-processing filters to the response"""
        filtered_response = response
        
        # Apply rule-based filters
        for rule in self.rules:
            if rule.response_filter and re.search(rule.pattern, user_input, re.IGNORECASE):
                filtered_response = self._apply_filter(filtered_response, rule.response_filter)
        
        # Apply custom filters
        for filter_name, filter_func in self.custom_filters.items():
            try:
                filtered_response = filter_func(filtered_response, user_input)
            except Exception as e:
                logger.warning(f"Custom filter {filter_name} failed: {e}")
        
        return filtered_response
    
    def _apply_filter(self, response: str, filter_rule: str) -> str:
        """Apply a specific filter rule to the response"""
        try:
            # Simple filter rules
            if filter_rule == "remove_disclaimers":
                # Remove common AI disclaimers
                disclaimers = [
                    r"I'm an AI.*?[\.!]",
                    r"As an AI.*?[\.!]",
                    r"I should mention.*?[\.!]",
                    r"Please note that.*?[\.!]"
                ]
                for disclaimer in disclaimers:
                    response = re.sub(disclaimer, "", response, flags=re.IGNORECASE)
            
            elif filter_rule == "add_confidence":
                # Add confidence indicators
                if not re.search(r"\b(definitely|certainly|sure|confident)\b", response, re.IGNORECASE):
                    response = "I'm confident that " + response.lower()
            
            elif filter_rule == "personalize":
                # Make response more personal
                response = response.replace("you should", "you might want to")
                response = response.replace("it is recommended", "I'd recommend")
            
        except Exception as e:
            logger.warning(f"Filter application failed: {e}")
        
        return response
    
    def get_template_response(self, intent: str, variables: Dict[str, Any] = None) -> Optional[str]:
        """Get a templated response for a specific intent"""
        for template in self.templates.values():
            if intent in template.intent_patterns:
                try:
                    # Merge template variables with provided variables
                    template_vars = template.variables or {}
                    if variables:
                        template_vars.update(variables)
                    
                    return template.template.format(**template_vars)
                except Exception as e:
                    logger.warning(f"Template formatting failed: {e}")
        
        return None
    
    def add_custom_filter(self, name: str, filter_func: Callable[[str, str], str]):
        """Add a custom response filter function"""
        self.custom_filters[name] = filter_func
        logger.info(f"Added custom filter: {name}")
    
    def save_customizations(self):
        """Save current customizations to config files"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            
            # Save rules
            rules_data = {
                "rules": [
                    {
                        "name": rule.name,
                        "pattern": rule.pattern,
                        "system_prompt_addition": rule.system_prompt_addition,
                        "response_filter": rule.response_filter,
                        "priority": rule.priority
                    }
                    for rule in self.rules
                ]
            }
            with open(self.config_dir / "response_rules.json", 'w', encoding='utf-8') as f:
                json.dump(rules_data, f, indent=2)
            
            # Save templates
            templates_data = {
                "templates": [
                    {
                        "name": template.name,
                        "intent_patterns": template.intent_patterns,
                        "template": template.template,
                        "variables": template.variables
                    }
                    for template in self.templates.values()
                ]
            }
            with open(self.config_dir / "response_templates.json", 'w', encoding='utf-8') as f:
                json.dump(templates_data, f, indent=2)
            
            logger.info("Saved response customizations")
            
        except Exception as e:
            logger.error(f"Failed to save customizations: {e}")

# Example usage and configuration
def create_sample_config():
    """Create sample configuration files"""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Sample rules
    sample_rules = {
        "rules": [
            {
                "name": "technical_questions",
                "pattern": "\\b(how to|tutorial|guide|explain)\\b",
                "system_prompt_addition": "Provide detailed, step-by-step explanations with examples.",
                "response_filter": "personalize",
                "priority": 5
            },
            {
                "name": "casual_conversation", 
                "pattern": "\\b(chat|talk|conversation)\\b",
                "system_prompt_addition": "Be conversational and friendly. Use a casual tone.",
                "response_filter": "remove_disclaimers",
                "priority": 3
            }
        ]
    }
    
    with open(config_dir / "response_rules.json", 'w') as f:
        json.dump(sample_rules, f, indent=2)
    
    # Sample templates
    sample_templates = {
        "templates": [
            {
                "name": "greeting",
                "intent_patterns": ["greeting", "hello", "hi"],
                "template": "Hello! I'm AstrOS, ready to help with anything you need. What's on your mind?",
                "variables": {}
            }
        ]
    }
    
    with open(config_dir / "response_templates.json", 'w') as f:
        json.dump(sample_templates, f, indent=2)

if __name__ == "__main__":
    # Create sample configuration
    create_sample_config()
    print("Sample response customization config created!")