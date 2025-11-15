"""Anthropic Claude AI client wrapper"""

import os
from typing import List, Dict, Optional, Any
from anthropic import Anthropic, AnthropicError
import json


class AIClient:
    """Wrapper for Anthropic Claude API"""
    
    def __init__(self, api_key: str = None, model: str = None, 
                 max_tokens: int = 4096, temperature: float = 0.7):
        """
        Initialize AI client
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model name (defaults to claude-3-5-sonnet-20241022)
            max_tokens: Maximum tokens for response
            temperature: Temperature for response generation (0.0 to 1.0)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model or os.getenv("AI_MODEL", "claude-sonnet-4-5-20250929")
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    def create_message(self, system: str, messages: List[Dict[str, str]], 
                      max_tokens: int = None, temperature: float = None) -> Dict[str, Any]:
        """
        Create a message using Claude API
        
        Args:
            system: System prompt/instructions
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Override default max_tokens
            temperature: Override default temperature
        
        Returns:
            Response dict with 'content', 'usage', 'stop_reason'
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature if temperature is not None else self.temperature,
                system=system,
                messages=messages
            )
            
            # Extract content
            content = ""
            if response.content:
                content = response.content[0].text if response.content else ""
            
            return {
                "content": content,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "stop_reason": response.stop_reason,
                "model": response.model
            }
        
        except AnthropicError as e:
            raise Exception(f"Anthropic API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling AI: {str(e)}")
    
    def chat(self, system: str, messages: List[Dict[str, str]], 
            max_tokens: int = None, temperature: float = None) -> str:
        """
        Simplified chat method that returns just the content string
        
        Args:
            system: System prompt/instructions
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Override default max_tokens
            temperature: Override default temperature
        
        Returns:
            Response content as string
        """
        response = self.create_message(system, messages, max_tokens, temperature)
        return response["content"]
    
    def generate_with_context(self, system: str, user_message: str, 
                             conversation_history: List[Dict[str, str]] = None,
                             max_tokens: int = None) -> Dict[str, Any]:
        """
        Generate response with conversation history
        
        Args:
            system: System instructions
            user_message: Current user message
            conversation_history: Previous messages in conversation
            max_tokens: Override default max_tokens
        
        Returns:
            Full response dict with content and usage
        """
        messages = []
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        return self.create_message(system, messages, max_tokens)
    
    def count_tokens_estimate(self, text: str) -> int:
        """
        Estimate token count for text
        Claude uses ~4 characters per token as rough estimate
        
        Args:
            text: Text to estimate
        
        Returns:
            Estimated token count
        """
        return len(text) // 4
    
    def truncate_conversation_history(self, messages: List[Dict[str, str]], 
                                     max_tokens: int = 6000) -> List[Dict[str, str]]:
        """
        Truncate conversation history to fit within token limit
        Keeps most recent messages
        
        Args:
            messages: List of message dicts
            max_tokens: Maximum tokens to keep
        
        Returns:
            Truncated message list
        """
        if not messages:
            return []
        
        total_tokens = 0
        truncated = []
        
        # Iterate from most recent to oldest
        for message in reversed(messages):
            message_tokens = self.count_tokens_estimate(message.get("content", ""))
            
            if total_tokens + message_tokens > max_tokens:
                break
            
            truncated.insert(0, message)
            total_tokens += message_tokens
        
        return truncated


class PromptBuilder:
    """Helper class to build prompts for different tutoring scenarios"""
    
    @staticmethod
    def load_system_instructions(file_path: str = None) -> str:
        """
        Load system instructions from file
        
        Args:
            file_path: Path to system instructions file
        
        Returns:
            System instructions as string
        """
        if file_path is None:
            # Default path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            file_path = os.path.join(base_dir, "data", "system_instructions.txt")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"System instructions file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def build_system_prompt(student_name: str = None, grade_level: int = None,
                           student_context: str = None) -> str:
        """
        Build complete system prompt with student context
        
        Args:
            student_name: Student's name
            grade_level: Student's grade level
            student_context: Additional context about student (strengths, weaknesses, etc.)
        
        Returns:
            Complete system prompt
        """
        base_instructions = PromptBuilder.load_system_instructions()
        
        # Add student context
        context_parts = [base_instructions]
        
        if student_name or grade_level or student_context:
            context_parts.append("\n\n## Current Student Context\n")
            
            if student_name:
                context_parts.append(f"Student Name: {student_name}\n")
            
            if grade_level:
                context_parts.append(f"Grade Level: {grade_level} (High School)\n")
            
            if student_context:
                context_parts.append(f"\n{student_context}\n")
        
        return "".join(context_parts)
    
    @staticmethod
    def format_homework_help_prompt(problem: str) -> str:
        """
        Format a homework help prompt
        
        Args:
            problem: The homework problem
        
        Returns:
            Formatted prompt
        """
        return f"""I need help with this problem:

{problem}

Can you help me solve it?"""
    
    @staticmethod
    def format_study_session_prompt(topic: str, student_level: str = "developing") -> str:
        """
        Format a study session prompt
        
        Args:
            topic: Topic to study
            student_level: Student's current level (beginner, developing, proficient, advanced)
        
        Returns:
            Formatted prompt
        """
        return f"""I need help understanding {topic}. My current level is {student_level}. Can you explain the concept and provide some practice problems?"""
    
    @staticmethod
    def format_practice_request_prompt(topic: str, difficulty: str = "medium", 
                                      count: int = 5) -> str:
        """
        Format a request for practice problems
        
        Args:
            topic: Topic for practice
            difficulty: Difficulty level
            count: Number of problems
        
        Returns:
            Formatted prompt
        """
        return f"""Create {count} {difficulty} difficulty practice problems for {topic}.

Format each problem as:
Problem 1: [problem text]
Problem 2: [problem text]

Then provide solutions at the end under a Solutions section.

Use clear math notation and keep formatting simple. No HTML tags."""
    
    @staticmethod
    def format_test_prep_prompt(test_topics: List[str], days_until_test: int) -> str:
        """
        Format a test preparation prompt
        
        Args:
            test_topics: List of topics on the test
            days_until_test: Days until the test
        
        Returns:
            Formatted prompt
        """
        topics_str = "\n".join([f"- {topic}" for topic in test_topics])
        
        return f"""I have a test coming up in {days_until_test} days.

Topics that will be on the test:
{topics_str}

Can you help me create a study plan and practice materials to prepare?"""
    
    @staticmethod
    def build_context_summary(messages: List[Dict], max_messages: int = 5) -> str:
        """
        Build a summary of recent conversation for context
        
        Args:
            messages: List of message dicts from database
            max_messages: Maximum messages to include
        
        Returns:
            Context summary string
        """
        if not messages:
            return "This is the start of a new conversation."
        
        recent = messages[-max_messages:] if len(messages) > max_messages else messages
        
        summary_parts = ["Recent conversation context:\n"]
        
        for msg in recent:
            role = "Student" if msg.get("role") == "student" else "Tutor"
            content = msg.get("content", "")
            # Truncate long messages
            if len(content) > 200:
                content = content[:200] + "..."
            summary_parts.append(f"{role}: {content}\n")
        
        return "".join(summary_parts)

