from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.modules.product.service import ProductService
from app.modules.product.schema import ProductCreate, ProductUpdate, ProductResponse
from app.services.cloudinary_service import upload_to_cloudinary

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_product(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Read file once
    contents = await file.read()

    # 2. Upload to cloudinary (can also be background task if needed, but usually we want URL back)
    image_url = await upload_to_cloudinary(contents)

    # 3. Save product
    product_in = ProductCreate(name=name, description=description, price=price)
    product = ProductService.create(db, product_in, image_url)

    # 4. Background task for embedding generation
    background_tasks.add_task(ProductService.update_product_embedding, product.id, contents)

    return product

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return ProductService.get_all(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    product = ProductService.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = ProductService.update(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    success = ProductService.delete(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}