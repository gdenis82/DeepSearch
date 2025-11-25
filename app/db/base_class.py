from typing import Any, Dict
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import registry
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

# Create metadata for the Base class
mapper_registry = registry()

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Add the MetaData instance to Base
    metadata = mapper_registry.metadata

    # Common timestamp columns for all tables
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # Generate __tablename__ automatically based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Serialization method
    def as_dict(self) -> Dict[str, Any]:
        """Convert the model instance to a dictionary."""
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

