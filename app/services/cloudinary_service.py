import cloudinary.uploader
from app.core.config import settings
from io import BytesIO

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_to_cloudinary(file_bytes: bytes):
    """
    Uploads image bytes to Cloudinary and returns the secure URL.
    """
    result = cloudinary.uploader.upload(file_bytes)
    return result["secure_url"]