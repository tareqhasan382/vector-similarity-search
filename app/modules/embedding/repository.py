from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.modules.embedding.model import ProductEmbedding

class EmbeddingRepository:
    @staticmethod
    def create_or_update(db: Session, product_id: UUID, embedding: List[float]) -> ProductEmbedding:
        existing_embedding = db.query(ProductEmbedding).filter(ProductEmbedding.product_id == product_id).first()
        
        if existing_embedding:
            existing_embedding.embedding = embedding
        else:
            existing_embedding = ProductEmbedding(
                product_id=product_id,
                embedding=embedding
            )
            db.add(existing_embedding)
        
        db.commit()
        return existing_embedding
