#!/usr/bin/env python3
"""
AstrOS Advanced Context Management System
Scalable conversation memory with intelligent summarization and persistence
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"

class ContextScope(Enum):
    SESSION = "session"      # Current conversation session
    SHORT_TERM = "short_term"  # Last few conversations
    LONG_TERM = "long_term"    # Summarized historical context
    PERSISTENT = "persistent"  # User preferences and facts

@dataclass
class Message:
    role: MessageType
    content: str
    timestamp: float
    metadata: Dict[str, Any] = None
    importance: float = 1.0  # 0.0 - 1.0, for memory retention

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class ConversationSummary:
    session_id: str
    start_time: float
    end_time: float
    message_count: int
    key_topics: List[str]
    summary: str
    importance: float

@dataclass
class UserFact:
    fact: str
    confidence: float
    last_updated: float
    category: str
    source_sessions: List[str]

class AdvancedContextManager:
    """
    Advanced conversation context management with:
    - Multi-level memory (session, short-term, long-term, persistent)
    - Intelligent summarization
    - Scalable storage
    - Context-aware retrieval
    """
    
    def __init__(self, db_path: str = "astros_context.db", max_session_messages: int = 50):
        self.db_path = db_path
        self.max_session_messages = max_session_messages
        self.current_session: Dict[str, List[Message]] = {}
        self.user_facts: Dict[str, List[UserFact]] = {}
        
        # Initialize database
        self._init_database()
        
        # Memory management settings
        self.session_timeout = 3600  # 1 hour
        self.short_term_days = 7
        self.long_term_days = 30
        
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    metadata TEXT,
                    importance REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversation summaries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL NOT NULL,
                    message_count INTEGER NOT NULL,
                    key_topics TEXT,
                    summary TEXT NOT NULL,
                    importance REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User facts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    fact TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    last_updated REAL NOT NULL,
                    category TEXT NOT NULL,
                    source_sessions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_facts_user ON user_facts(user_id)')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def _generate_session_id(self, user_id: str = "anonymous") -> str:
        """Generate unique session ID"""
        timestamp = str(time.time())
        return hashlib.md5(f"{user_id}_{timestamp}".encode()).hexdigest()[:16]

    async def add_message(self, session_id: str, role: MessageType, content: str, 
                         metadata: Dict[str, Any] = None, importance: float = 1.0) -> Message:
        """Add a message to the conversation context"""
        try:
            message = Message(
                role=role,
                content=content,
                timestamp=time.time(),
                metadata=metadata or {},
                importance=importance
            )
            
            # Add to current session
            if session_id not in self.current_session:
                self.current_session[session_id] = []
            
            self.current_session[session_id].append(message)
            
            # Persist to database
            await self._persist_message(session_id, message)
            
            # Manage session size
            if len(self.current_session[session_id]) > self.max_session_messages:
                await self._trim_session(session_id)
            
            # Extract user facts if it's a user message
            if role == MessageType.USER:
                await self._extract_user_facts(session_id, content)
            
            logger.info(f"Added message to session {session_id}: {role.value}")
            return message
            
        except Exception as e:
            logger.error(f"Failed to add message: {e}")
            raise

    async def _persist_message(self, session_id: str, message: Message):
        """Persist message to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO messages (session_id, role, content, timestamp, metadata, importance)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                message.role.value,
                message.content,
                message.timestamp,
                json.dumps(message.metadata),
                message.importance
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to persist message: {e}")

    async def get_context(self, session_id: str, max_messages: int = 20, 
                         include_summaries: bool = True, user_id: str = "anonymous") -> List[Dict[str, Any]]:
        """Get conversation context with intelligent retrieval"""
        try:
            context = []
            
            # 1. Get current session messages
            if session_id in self.current_session:
                session_messages = self.current_session[session_id][-max_messages:]
                for msg in session_messages:
                    context.append({
                        "role": msg.role.value,
                        "content": msg.content,
                        "timestamp": msg.timestamp,
                        "importance": msg.importance
                    })
            
            # 2. Get relevant user facts
            user_facts = await self._get_relevant_facts(user_id, session_id)
            if user_facts:
                facts_content = "User information: " + "; ".join([f.fact for f in user_facts[:5]])
                context.insert(0, {
                    "role": "system",
                    "content": facts_content,
                    "timestamp": time.time(),
                    "importance": 1.0
                })
            
            # 3. Get conversation summaries if requested
            if include_summaries:
                summaries = await self._get_relevant_summaries(session_id, user_id)
                if summaries:
                    summary_content = "Previous conversation context: " + "; ".join([s.summary for s in summaries[:2]])
                    context.insert(0, {
                        "role": "system",
                        "content": summary_content,
                        "timestamp": time.time(),
                        "importance": 0.8
                    })
            
            logger.info(f"Retrieved context for session {session_id}: {len(context)} messages")
            return context
            
        except Exception as e:
            logger.error(f"Failed to get context: {e}")
            return []

    async def _extract_user_facts(self, session_id: str, content: str):
        """Extract and store user facts from conversation"""
        try:
            # Simple fact extraction (can be enhanced with NLP)
            facts_to_extract = []
            
            # Name extraction
            if "my name is" in content.lower():
                name = content.lower().split("my name is")[-1].strip().split()[0]
                if name.isalpha():
                    facts_to_extract.append(("name", f"User's name is {name.title()}", 0.9))
            
            # Preference extraction
            if "i like" in content.lower() or "i love" in content.lower():
                preference = content.strip()
                facts_to_extract.append(("preference", preference, 0.7))
            
            # Store extracted facts
            for category, fact, confidence in facts_to_extract:
                await self._store_user_fact("anonymous", fact, confidence, category, session_id)
                
        except Exception as e:
            logger.error(f"Failed to extract user facts: {e}")

    async def _store_user_fact(self, user_id: str, fact: str, confidence: float, 
                              category: str, session_id: str):
        """Store a user fact with deduplication"""
        try:
            # Check if similar fact exists
            existing_facts = self.user_facts.get(user_id, [])
            for existing_fact in existing_facts:
                if existing_fact.category == category and existing_fact.fact == fact:
                    # Update existing fact
                    existing_fact.confidence = max(existing_fact.confidence, confidence)
                    existing_fact.last_updated = time.time()
                    if session_id not in existing_fact.source_sessions:
                        existing_fact.source_sessions.append(session_id)
                    return
            
            # Create new fact
            user_fact = UserFact(
                fact=fact,
                confidence=confidence,
                last_updated=time.time(),
                category=category,
                source_sessions=[session_id]
            )
            
            if user_id not in self.user_facts:
                self.user_facts[user_id] = []
            
            self.user_facts[user_id].append(user_fact)
            
            # Persist to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_facts (user_id, fact, confidence, last_updated, category, source_sessions)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, fact, confidence, time.time(), category, json.dumps([session_id])
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored user fact: {fact}")
            
        except Exception as e:
            logger.error(f"Failed to store user fact: {e}")

    async def _get_relevant_facts(self, user_id: str, session_id: str, limit: int = 10) -> List[UserFact]:
        """Get relevant user facts for context"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT fact, confidence, last_updated, category, source_sessions
                FROM user_facts
                WHERE user_id = ?
                ORDER BY confidence DESC, last_updated DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            facts = []
            for row in rows:
                facts.append(UserFact(
                    fact=row[0],
                    confidence=row[1],
                    last_updated=row[2],
                    category=row[3],
                    source_sessions=json.loads(row[4])
                ))
            
            return facts
            
        except Exception as e:
            logger.error(f"Failed to get relevant facts: {e}")
            return []

    async def _get_relevant_summaries(self, session_id: str, user_id: str, limit: int = 3) -> List[ConversationSummary]:
        """Get relevant conversation summaries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent summaries (excluding current session)
            cursor.execute('''
                SELECT session_id, start_time, end_time, message_count, key_topics, summary, importance
                FROM conversation_summaries
                WHERE session_id != ?
                ORDER BY importance DESC, end_time DESC
                LIMIT ?
            ''', (session_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            summaries = []
            for row in rows:
                summaries.append(ConversationSummary(
                    session_id=row[0],
                    start_time=row[1],
                    end_time=row[2],
                    message_count=row[3],
                    key_topics=json.loads(row[4] or "[]"),
                    summary=row[5],
                    importance=row[6]
                ))
            
            return summaries
            
        except Exception as e:
            logger.error(f"Failed to get relevant summaries: {e}")
            return []

    async def _trim_session(self, session_id: str):
        """Trim session when it gets too long"""
        try:
            if session_id not in self.current_session:
                return
            
            messages = self.current_session[session_id]
            if len(messages) <= self.max_session_messages:
                return
            
            # Keep the most recent messages and important ones
            important_messages = [msg for msg in messages if msg.importance > 0.8]
            recent_messages = messages[-self.max_session_messages // 2:]
            
            # Combine and deduplicate
            kept_messages = []
            seen_contents = set()
            
            for msg in important_messages + recent_messages:
                if msg.content not in seen_contents:
                    kept_messages.append(msg)
                    seen_contents.add(msg.content)
            
            # Sort by timestamp
            kept_messages.sort(key=lambda x: x.timestamp)
            
            self.current_session[session_id] = kept_messages[-self.max_session_messages:]
            
            logger.info(f"Trimmed session {session_id} to {len(kept_messages)} messages")
            
        except Exception as e:
            logger.error(f"Failed to trim session: {e}")

    async def summarize_session(self, session_id: str) -> Optional[ConversationSummary]:
        """Create a summary of a conversation session"""
        try:
            if session_id not in self.current_session:
                return None
            
            messages = self.current_session[session_id]
            if len(messages) < 5:  # Don't summarize very short conversations
                return None
            
            # Extract key information
            start_time = messages[0].timestamp
            end_time = messages[-1].timestamp
            message_count = len(messages)
            
            # Simple key topic extraction (can be enhanced with NLP)
            content_text = " ".join([msg.content for msg in messages if msg.role == MessageType.USER])
            key_topics = await self._extract_key_topics(content_text)
            
            # Create summary (simplified - could use AI for better summaries)
            user_messages = [msg.content for msg in messages if msg.role == MessageType.USER]
            assistant_messages = [msg.content for msg in messages if msg.role == MessageType.ASSISTANT]
            
            summary = f"Conversation with {len(user_messages)} user messages and {len(assistant_messages)} responses. "
            if key_topics:
                summary += f"Main topics: {', '.join(key_topics[:3])}."
            
            # Calculate importance based on message count and user engagement
            importance = min(1.0, (message_count / 20) * 0.5 + 0.5)
            
            conversation_summary = ConversationSummary(
                session_id=session_id,
                start_time=start_time,
                end_time=end_time,
                message_count=message_count,
                key_topics=key_topics,
                summary=summary,
                importance=importance
            )
            
            # Persist summary
            await self._persist_summary(conversation_summary)
            
            logger.info(f"Created summary for session {session_id}")
            return conversation_summary
            
        except Exception as e:
            logger.error(f"Failed to summarize session: {e}")
            return None

    async def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from text (simplified implementation)"""
        try:
            # Simple keyword extraction (can be enhanced with NLP libraries)
            common_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this'}
            words = text.lower().split()
            
            # Count word frequency
            word_count = {}
            for word in words:
                word = word.strip('.,!?";()[]{}')
                if len(word) > 3 and word not in common_words:
                    word_count[word] = word_count.get(word, 0) + 1
            
            # Get top topics
            topics = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            return [topic[0] for topic in topics[:5]]
            
        except Exception as e:
            logger.error(f"Failed to extract key topics: {e}")
            return []

    async def _persist_summary(self, summary: ConversationSummary):
        """Persist conversation summary to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO conversation_summaries 
                (session_id, start_time, end_time, message_count, key_topics, summary, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                summary.session_id,
                summary.start_time,
                summary.end_time,
                summary.message_count,
                json.dumps(summary.key_topics),
                summary.summary,
                summary.importance
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to persist summary: {e}")

    async def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old conversation data"""
        try:
            cutoff_time = time.time() - (days_to_keep * 24 * 3600)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete old messages
            cursor.execute('DELETE FROM messages WHERE timestamp < ?', (cutoff_time,))
            
            # Delete old summaries (keep important ones longer)
            cursor.execute('DELETE FROM conversation_summaries WHERE end_time < ? AND importance < 0.7', (cutoff_time,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cleaned up data older than {days_to_keep} days")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")

    async def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a conversation session"""
        try:
            if session_id not in self.current_session:
                return {}
            
            messages = self.current_session[session_id]
            user_messages = [msg for msg in messages if msg.role == MessageType.USER]
            assistant_messages = [msg for msg in messages if msg.role == MessageType.ASSISTANT]
            
            stats = {
                "session_id": session_id,
                "total_messages": len(messages),
                "user_messages": len(user_messages),
                "assistant_messages": len(assistant_messages),
                "session_duration": messages[-1].timestamp - messages[0].timestamp if messages else 0,
                "average_response_time": 0,  # Could be calculated from metadata
                "topics_discussed": await self._extract_key_topics(" ".join([msg.content for msg in user_messages])),
                "session_start": messages[0].timestamp if messages else None,
                "last_activity": messages[-1].timestamp if messages else None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get session stats: {e}")
            return {}

# Test the system
async def test_context_manager():
    """Test the advanced context management system"""
    print("🧪 Testing Advanced Context Management System")
    print("=" * 50)
    
    # Initialize context manager
    context_mgr = AdvancedContextManager()
    
    # Create a test session
    session_id = context_mgr._generate_session_id("test_user")
    print(f"Created session: {session_id}")
    
    # Add some test messages
    await context_mgr.add_message(session_id, MessageType.USER, "Hi, my name is John")
    await context_mgr.add_message(session_id, MessageType.ASSISTANT, "Hello John! Nice to meet you. How can I help you today?")
    await context_mgr.add_message(session_id, MessageType.USER, "I like programming and AI")
    await context_mgr.add_message(session_id, MessageType.ASSISTANT, "That's great! Programming and AI are fascinating fields. What specific areas interest you most?")
    await context_mgr.add_message(session_id, MessageType.USER, "What's my name?")
    
    # Get context
    context = await context_mgr.get_context(session_id)
    print(f"\n📝 Context retrieved ({len(context)} messages):")
    for msg in context:
        print(f"  {msg['role']}: {msg['content'][:50]}...")
    
    # Get session stats
    stats = await context_mgr.get_session_stats(session_id)
    print(f"\n📊 Session Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Create summary
    summary = await context_mgr.summarize_session(session_id)
    if summary:
        print(f"\n📋 Session Summary:")
        print(f"  Topics: {summary.key_topics}")
        print(f"  Summary: {summary.summary}")
        print(f"  Importance: {summary.importance}")
    
    print("\n✅ Context management system test completed!")

if __name__ == "__main__":
    asyncio.run(test_context_manager())