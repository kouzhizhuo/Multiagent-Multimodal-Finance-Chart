from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class AgentResponse(BaseModel):
    """Base response model for all agents"""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.context: Dict[str, Any] = {}
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process the input data and return results"""
        pass
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update the agent's context with new information"""
        self.context.update(new_context)
    
    def get_context(self) -> Dict[str, Any]:
        """Get the current context of the agent"""
        return self.context
    
    def clear_context(self) -> None:
        """Clear the agent's context"""
        self.context = {} 