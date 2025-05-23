import allure
import pytest
import base64
import os
import uuid
from datetime import datetime
from openai import OpenAI


# @pytest.mark.skip(reason="Test disabled")
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
                prompt="a pixel art style of lu kang from mortal kombat in different fight poses",
                size="1024x1024",
                background="transparent",
                quality="high",
            )

        with allure.step("Extract image data from response"):
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

        with allure.step("Attach generated image to Allure report"):
            allure.attach(
                image_bytes,
                name="Generated Pixel Art",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Save image to output directory"):
            os.makedirs("output", exist_ok=True)
            # Generate a 5-char uuid and timestamp
            short_uuid = str(uuid.uuid4())[:5]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"image_gen_{short_uuid}_{timestamp}.png"
            output_path = os.path.join("output", output_filename)
            with open(output_path, "wb") as f:
                f.write(image_bytes)

        with allure.step("Attach saved image file to Allure report"):
            with open(output_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Saved Pixel Art ({output_filename})",
                    attachment_type=allure.attachment_type.PNG
                )

        with allure.step("Verify image file was created"):
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
