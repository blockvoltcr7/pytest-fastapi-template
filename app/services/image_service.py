import os
import base64
from typing import Optional
from openai import OpenAI
from app.core.config import settings

class ImageService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_image(
        self,
        prompt: str,
        output_filename: str,
        size: str = "1024x1024",
        n: int = 1
    ) -> Optional[str]:
        """
        Generate an image using OpenAI's image generation model.

        Args:
            prompt: The text prompt to generate the image from.
            output_filename: Name for the output image file (e.g., "output.png").
            size: The size of the image (default: "1024x1024").
            n: Number of images to generate (default: 1).

        Returns:
            Path to the generated image file, or None if generation failed.
        """
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")

        try:
            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                n=n,
                size=size
            )

            # Ensure output directory exists
            os.makedirs(settings.images_dir, exist_ok=True)
            output_path = os.path.join(settings.images_dir, output_filename)

            # Save the first generated image
            image_bytes = base64.b64decode(response.data[0].b64_json)
            with open(output_path, "wb") as f:
                f.write(image_bytes)

            print(f"✅ Generated image saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")
            return None

    def check_api_connection(self) -> bool:
        """Test OpenAI API connection."""
        if not settings.openai_api_key:
            return False

        try:
            models = self.client.models.list()
            return len(models.data) > 0
        except:
            return False