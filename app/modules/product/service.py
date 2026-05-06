from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.modules.product.model import Product
from app.modules.product.schema import ProductCreate, ProductUpdate
from app.modules.embedding.service import embedder
from app.core.database import SessionLocal
from app.modules.product.repository import ProductRepository
from app.modules.embedding.repository import EmbeddingRepository

class ProductService:
    @staticmethod
    def create(db: Session, product_in: ProductCreate, image_url: str) -> Product:
        return ProductRepository.create(db, product_in, image_url)

    @staticmethod
    def update_product_embedding(product_id: UUID, image_bytes: bytes):
        """
        Background task to generate and store product embedding.
        """
        db = SessionLocal()
        try:
            embedding = embedder.get_embedding(image_bytes)
            EmbeddingRepository.create_or_update(db, product_id, embedding)
            print(f"Embedding generated and stored for product {product_id}")
        except Exception as e:
            db.rollback()
            print(f"Error generating embedding for product {product_id}: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return ProductRepository.get_all(db, skip, limit)

    @staticmethod
    def get_by_id(db: Session, product_id: UUID) -> Optional[Product]:
        return ProductRepository.get_by_id(db, product_id)

    @staticmethod
    def update(db: Session, product_id: UUID, product_in: ProductUpdate) -> Optional[Product]:
        return ProductRepository.update(db, product_id, product_in)

    @staticmethod
    def delete(db: Session, product_id: UUID) -> bool:
        return ProductRepository.delete(db, product_id)