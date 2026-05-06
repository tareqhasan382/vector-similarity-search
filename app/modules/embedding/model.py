import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class ProductEmbedding(Base):
    __tablename__ = "product_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    embedding = Column(Vector(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to product
    product = relationship("Product", back_populates="embedding")