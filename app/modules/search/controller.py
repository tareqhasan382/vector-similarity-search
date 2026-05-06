from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.modules.embedding.service import embedder
from app.modules.search.service import SearchService
from app.modules.product.schema import SearchResult, ProductResponse

router = APIRouter()

SIMILARITY_THRESHOLD = 0.70

@router.post("/image", response_model=SearchResult)
async def search_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Read file
    contents = await file.read()

    # 2. Generate embedding (Synchronous for search as user waits for result)
    embedding = embedder.get_embedding(contents)

    # 3. Search for the single best product
    result = SearchService.search(db, embedding)

    if not result:
        raise HTTPException(status_code=404, detail="No matching product found")

    product, score = result
    score = float(score)

    # 4. Apply similarity threshold
    if score < SIMILARITY_THRESHOLD:
        raise HTTPException(
            status_code=404, 
            detail=f"No matching product found (Best match score: {score:.2f} is below threshold {SIMILARITY_THRESHOLD})"
        )

    # 5. Format response
    return SearchResult(
        product=ProductResponse.model_validate(product),
        score=score
    )