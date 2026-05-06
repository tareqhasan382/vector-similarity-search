# Vector Similarity Search API 🚀

A production-ready image-based product search system built with **FastAPI**, **PostgreSQL + pgvector**, and **CLIP**.

## 🎯 Project Overview

This project provides a modular and scalable backend for searching products using image similarity. It uses the OpenAI CLIP model to transform images into 512-dimensional vectors and leverages the `pgvector` extension in PostgreSQL for efficient similarity searches.

### Key Features
- **Product Management**: Full CRUD APIs for products (name, description, price, image).
- **AI-Powered Search**: Upload an image and find the single most accurate matching product.
- **Background Processing**: Heavy embedding generation is handled via FastAPI BackgroundTasks.
- **Singleton Pattern**: The CLIP model is loaded once at startup to optimize memory and performance.
- **Production-Ready Architecture**: Clean separation of concerns (Controllers, Services, Repositories).
- **HNSW Indexing**: High-performance vector search using HNSW (Hierarchical Navigable Small World) indexing.

---

## 🏗 Architecture

The project follows a clean, modular structure:

```text
app/
├── core/               # Configuration and database connection
├── modules/
│   ├── product/        # Product CRUD (Controller, Service, Repository, Model, Schema)
│   ├── embedding/      # CLIP Embedding logic and storage
│   └── search/         # Similarity search logic
├── services/           # External integrations (Cloudinary)
└── main.py             # Entry point and lifespan management
```

---

## ⚡ Tech Stack

- **FastAPI**: Modern, high-performance web framework.
- **PostgreSQL + pgvector**: Vector similarity storage and search.
- **SQLAlchemy**: ORM for database management.
- **Transformers (CLIP)**: `openai/clip-vit-base-patch32` for image embedding.
- **Cloudinary**: Cloud-based image storage and management.
- **Pydantic**: Data validation and serialization.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL with `pgvector` extension installed.
- Cloudinary account for image uploads.

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd vector-similarity-search
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🛠 API Endpoints

### Product APIs
- `POST /products/`: Create a new product with image upload (Triggers background embedding).
- `GET /products/`: List all products with pagination.
- `GET /products/{id}`: Get detailed information for a specific product.
- `PATCH /products/{id}`: Update product details.
- `DELETE /products/{id}`: Delete a product and its associated embedding.

### Search API
- `POST /search/image`: Upload an image to find the best matching product.
  - **Threshold**: Only returns results with a similarity score > 0.70.
  - **Response**: Returns the single best matching product and its score.

---

## 🧠 Performance Optimization

- **Model Lifecycle**: The CLIP model is loaded into memory once during application startup via the `lifespan` context manager.
- **Asynchronous Flow**: Product creation returns immediately while embedding generation runs in the background.
- **Indexing**: An HNSW index is automatically created on the embedding column for sub-second search speeds.

---

## 📝 License
This project is licensed under the MIT License.
