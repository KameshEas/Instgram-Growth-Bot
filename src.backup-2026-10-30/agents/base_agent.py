from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
from src.logger import setup_logger

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"agent.{name}")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic - must be implemented by subclasses"""
        pass
    
    async def log_execution(self, 
                           input_data: Dict, 
                           output_data: Dict, 
                           status: str):
        """Log execution for debugging"""
        self.logger.info(
            f"[{self.name}] {status} | "
            f"Input: {len(str(input_data))} chars | "
            f"Output: {len(str(output_data))} chars"
        )
