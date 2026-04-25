from typing import Dict, Any
from src.agents.base_agent import BaseAgent

class TelegramHandlerAgent(BaseAgent):
    """Parse and handle Telegram commands"""
    
    def __init__(self):
        super().__init__("TelegramHandler")
    
    async def execute(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Telegram update and extract command"""
        try:
            # Extract basic info
            message = update.get("message", {})
            user_id = message.get("from", {}).get("id")
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            
            # Parse command
            command = self._parse_command(text)
            params = self._extract_parameters(command, text)
            
            result = {
                "status": "success",
                "user_id": user_id,
                "chat_id": chat_id,
                "command": command,
                "parameters": params,
                "raw_message": text
            }
            
            await self.log_execution(update, result, "success")
            return result
            
        except Exception as e:
            self.logger.error(f"Error parsing Telegram update: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _parse_command(self, text: str) -> str:
        """Extract command from text"""
        if not text:
            return "message"
        
        if text.startswith("/"):
            return text.split()[0]
        return "message"
    
    def _extract_parameters(self, command: str, text: str) -> Dict:
        """Extract parameters from command"""
        # Example: /generate_woman professional -> {"style": "professional"}
        if " " in text:
            params = text.split(" ", 1)[1]
            return {"input": params}
        return {}
