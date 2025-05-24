import allure
import pytest
import os
from openai import OpenAI

@allure.epic("AI Integration")
@allure.feature("OpenAI API")
class TestOpenAIIntegration:

    @allure.story("Basic API Response")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_openai_response(self, openai_client):
        """Test that OpenAI API returns a valid response."""

        prompt = "Say hello world in exactly 3 words"

        with allure.step(f"Send request to OpenAI with prompt: '{prompt}'"):
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50
                )

                allure.attach(
                    str(response),
                    name="Raw Response Object",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                allure.attach(
                    str(e),
                    name="API Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.fail(f"OpenAI API request failed: {str(e)}")

        with allure.step("Verify response contains message content"):
            assert len(response.choices) > 0, "Response missing choices"
            
            message = response.choices[0].message
            assert message.content, "Response message missing content"

            output_text = message.content.strip()
            allure.attach(
                output_text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT
            )

            assert isinstance(output_text, str), "Output text is not a string"
            assert len(output_text) > 0, "Output text is empty"

            print(f"OpenAI Response: {output_text}")