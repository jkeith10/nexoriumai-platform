"""Memory implementation for agents."""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Database configuration
DATABASE_URL = "sqlite:///agent_memory.db"
engine = create_engine(DATABASE_URL)

class Memory(SQLModel, table=True):
    """Memory entry for storing agent interactions."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: str = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    content: str
    role: str  # system, user, or assistant

class MemoryManager:
    """Manages persistent memory for agents."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        
    def add_entry(self, content: str, role: str) -> None:
        """Add a new memory entry."""
        with Session(engine) as session:
            memory = Memory(
                agent_id=self.agent_id,
                content=content,
                role=role
            )
            session.add(memory)
            session.commit()
    
    def get_recent_memories(self, limit: int = 10) -> List[Memory]:
        """Get recent memories for the agent."""
        with Session(engine) as session:
            statement = select(Memory)\
                .where(Memory.agent_id == self.agent_id)\
                .order_by(Memory.timestamp.desc())\
                .limit(limit)
            return list(session.exec(statement))

# Create tables
SQLModel.metadata.create_all(engine)