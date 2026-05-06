import torch
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
from typing import List

class EmbeddingService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None

    def load_model(self):
        """Loads the CLIP model into memory once."""
        if self.model is None:
            print(f"Loading CLIP model on {self.device}...")
            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
            self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            print("Model loaded successfully.")

    def get_embedding(self, file_bytes: bytes) -> List[float]:
        """
        Generates a normalized CLIP embedding from image bytes.
        """
        if self.model is None:
            self.load_model()

        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            # Use get_image_features and ensure we handle the output correctly
            outputs = self.model.get_image_features(**inputs)
            
            # CLIPModel.get_image_features usually returns a tensor directly, 
            # but some versions or configurations might return an object.
            if hasattr(outputs, "image_embeds"):
                features = outputs.image_embeds
            elif hasattr(outputs, "pooler_output"):
                features = outputs.pooler_output
            else:
                features = outputs

        # Normalize vector for cosine similarity
        if hasattr(features, "norm"):
            features = features / (features.norm(dim=-1, keepdim=True) + 1e-8)
        else:
            # Fallback if features is somehow still not a tensor
            features = torch.tensor(features).to(self.device)
            features = features / (features.norm(dim=-1, keepdim=True) + 1e-8)
        
        return features.squeeze().cpu().tolist()

# Singleton instance
embedder = EmbeddingService()