from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.modules.product.model import Product
from app.modules.product.schema import ProductCreate, ProductUpdate

class ProductRepository:
    @staticmethod
    def create(db: Session, product_in: ProductCreate, image_url: str) -> Product:
        product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            image_url=image_url
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, product_id: UUID) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def update(db: Session, product_id: UUID, product_in: ProductUpdate) -> Optional[Product]:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product_id: UUID) -> bool:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        
        db.delete(product)
        db.commit()
        return True
