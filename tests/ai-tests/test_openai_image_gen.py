import allure
import pytest
import base64
import os
from openai import OpenAI


@pytest.mark.skip(reason="Test disabled")
@allure.epic("AI Services")
@allure.feature("OpenAI Image Generation")
@pytest.mark.api
class TestOpenAIImageGeneration:
    
    @allure.story("Pixel Art Generation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_generate_pixel_art_image(self):
        """Test that OpenAI can generate a pixel art image with transparent background"""
        with allure.step("Initialize OpenAI client"):
            client = OpenAI()
        
        with allure.step("Request image generation with specific parameters"):
            result = client.images.generate(
                model="gpt-image-1",
                prompt="a pixel art style of a miyamoto musashi in different fight poses",
                size="1024x1024",
                background="transparent",
                quality="high",
            )
        
        with allure.step("Extract image data from response"):
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            
            # Attach image to allure report
            allure.attach(
                image_bytes,
                name="Generated Pixel Art",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Save image to output directory"):
            os.makedirs("output", exist_ok=True)
            output_path = "output/miyamoto_musashi.png"
            with open(output_path, "wb") as f:
                f.write(image_bytes)
                
        with allure.step("Verify image file was created"):
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
