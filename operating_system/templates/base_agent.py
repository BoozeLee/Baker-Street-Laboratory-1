"""
Base Agent Class for Terminal221B Autonomous Agents
Provides common functionality for Analyst, Artist, and Engineer agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import logging


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    enabled: bool = True
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: int = 30
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentAction:
    """Represents an action taken by an agent"""
    action_type: str
    timestamp: datetime
    success: bool
    details: Dict[str, Any]
    error: Optional[str] = None


class BaseAgent(ABC):
    """
    Abstract base class for Terminal221B agents

    All agents (Analyst, Artist, Engineer) inherit from this class
    and implement the required abstract methods.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = self._setup_logger()
        self.action_history: List[AgentAction] = []
        self.state: Dict[str, Any] = {}

    def _setup_logger(self) -> logging.Logger:
        """Configure agent-specific logger"""
        logger = logging.getLogger(f"terminal221b.agent.{self.config.name}")
        logger.setLevel(getattr(logging, self.config.log_level))

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s [{self.config.name}] %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the agent (connect to APIs, load models, etc.)

        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> AgentAction:
        """
        Execute a specific task

        Args:
            task: Dictionary containing task parameters

        Returns:
            AgentAction: Result of the task execution
        """
        pass

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status

        Returns:
            Dict containing agent status information
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """
        Gracefully shutdown the agent (cleanup resources)
        """
        pass

    def record_action(self, action: AgentAction) -> None:
        """
        Record an action in the agent's history

        Args:
            action: The action to record
        """
        self.action_history.append(action)
        self.logger.info(
            f"Action recorded: {action.action_type} "
            f"({'Success' if action.success else 'Failed'})"
        )

        # Keep history manageable (last 1000 actions)
        if len(self.action_history) > 1000:
            self.action_history = self.action_history[-1000:]

    def get_action_history(
        self,
        limit: Optional[int] = None,
        action_type: Optional[str] = None
    ) -> List[AgentAction]:
        """
        Get agent's action history

        Args:
            limit: Maximum number of actions to return
            action_type: Filter by specific action type

        Returns:
            List of AgentActions
        """
        history = self.action_history

        if action_type:
            history = [a for a in history if a.action_type == action_type]

        if limit:
            history = history[-limit:]

        return history

    def update_state(self, key: str, value: Any) -> None:
        """
        Update agent's internal state

        Args:
            key: State key
            value: State value
        """
        self.state[key] = value
        self.logger.debug(f"State updated: {key} = {value}")

    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get value from agent's state

        Args:
            key: State key
            default: Default value if key not found

        Returns:
            State value or default
        """
        return self.state.get(key, default)

    async def health_check(self) -> bool:
        """
        Perform health check

        Returns:
            bool: True if agent is healthy, False otherwise
        """
        try:
            status = await self.get_status()
            return status.get("healthy", False)
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False

    def is_enabled(self) -> bool:
        """Check if agent is enabled"""
        return self.config.enabled

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.config.name}', "
            f"enabled={self.config.enabled})"
        )
