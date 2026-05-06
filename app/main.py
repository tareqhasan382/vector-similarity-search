from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.modules.product.controller import router as product_router
from app.modules.search.controller import router as search_router
from app.core.database import Base, engine
from app.modules.embedding.service import embedder

# Create extension and tables on startup
def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    
    # Create HNSW index if it doesn't exist
    with engine.connect() as conn:
        # Check if index exists
        check_index = conn.execute(text(
            "SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
            "WHERE c.relname = 'hnsw_idx_product_embeddings' AND n.nspname = 'public'"
        )).fetchone()
        
        if not check_index:
            print("Creating HNSW index for product embeddings...")
            conn.execute(text(
                "CREATE INDEX hnsw_idx_product_embeddings ON product_embeddings "
                "USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64)"
            ))
            conn.commit()
            print("HNSW index created.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    embedder.load_model()
    yield
    # Shutdown logic (optional)

app = FastAPI(
    title="Vector Similarity Search API",
    description="A production-ready image-based product search system using CLIP and pgvector.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Vector Similarity Search API"}

app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(search_router, prefix="/search", tags=["Search"])