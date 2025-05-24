import os
import allure
import pytest
from dotenv import load_dotenv

@allure.feature("Dotenv Loading")
@allure.story("Verify .env loading and OPENAI_API_KEY presence")
def test_load_dotenv_and_print_openai_api_key():
    with allure.step("Load .env file"):
        load_dotenv()
    
    with allure.step("Get OPENAI_API_KEY from environment"):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        assert openai_api_key is not None, "OPENAI_API_KEY is not set in environment variables"
    