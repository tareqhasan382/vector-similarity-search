from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Tuple, Optional
from app.modules.product.model import Product
from app.modules.embedding.model import ProductEmbedding

class SearchRepository:
    @staticmethod
    def search_by_vector(db: Session, embedding: List[float]) -> Optional[Tuple[Product, float]]:
        """
        Search for the single best product using cosine similarity.
        """
        query = (
            select(
                Product,
                (1 - ProductEmbedding.embedding.cosine_distance(embedding)).label("similarity")
            )
            .join(ProductEmbedding, Product.id == ProductEmbedding.product_id)
            .order_by(ProductEmbedding.embedding.cosine_distance(embedding))
            .limit(1)
        )
        
        result = db.execute(query).first()
        return result

class SearchService:
    @staticmethod
    def search(db: Session, embedding: List[float]) -> Optional[Tuple[Product, float]]:
        return SearchRepository.search_by_vector(db, embedding)