"""Configuration management"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration manager"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config.yaml file
        """
        if config_path is None:
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config.yaml"
        
        self.config_path = config_path
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    @property
    def app_name(self) -> str:
        """Get application name"""
        return self.get('app.name', 'AI Math Tutor')
    
    @property
    def grade_levels(self) -> Dict[str, int]:
        """Get grade level configuration"""
        return self.get('app.grade_levels', {'min': 9, 'max': 12})
    
    @property
    def ai_model(self) -> str:
        """Get AI model name"""
        return os.getenv('AI_MODEL') or 'claude-3-5-sonnet-20241022'
    
    @property
    def ai_max_tokens(self) -> int:
        """Get max tokens for AI"""
        return int(os.getenv('AI_MAX_TOKENS', '4096'))
    
    @property
    def ai_temperature(self) -> float:
        """Get AI temperature"""
        return float(os.getenv('AI_TEMPERATURE', '0.7'))
    
    @property
    def database_url(self) -> str:
        """Get database URL"""
        return os.getenv('DATABASE_URL', 'sqlite:///data/tutoring.db')
    
    @property
    def session_timeout_minutes(self) -> int:
        """Get session timeout in minutes"""
        return int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    
    @property
    def max_conversation_history(self) -> int:
        """Get max conversation history messages"""
        return int(os.getenv('MAX_CONVERSATION_HISTORY', '50'))
    
    @property
    def topics(self) -> Dict[str, list]:
        """Get all topics configuration"""
        return self.get('topics', {})
    
    def get_topics_for_category(self, category: str) -> list:
        """Get topics for a specific category"""
        return self.get(f'topics.{category}', [])


# Global config instance
config = Config()

