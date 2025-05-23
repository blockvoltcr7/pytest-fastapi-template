"""Test utilities and helper functions."""

import json
import allure
from typing import Any, Dict, Optional


def attach_response_to_allure(
    response_data: Any,
    name: str = "Response Data",
    attachment_type: str = allure.attachment_type.JSON,
) -> None:
    """
    Attach API response data to Allure report.

    Args:
        response_data: The response data to attach
        name: Name of the attachment
        attachment_type: Type of attachment (JSON, TEXT, etc.)
    """
    if isinstance(response_data, (dict, list)):
        allure.attach(
            json.dumps(response_data, indent=2),
            name=name,
            attachment_type=attachment_type,
        )
    else:
        allure.attach(
            str(response_data),
            name=name,
            attachment_type=allure.attachment_type.TEXT,
        )


def validate_response_schema(
    response_data: Dict[str, Any],
    expected_fields: Dict[str, type],
    allow_extra: bool = False,
) -> tuple[bool, Optional[str]]:
    """
    Validate response data against expected schema.

    Args:
        response_data: Response data to validate
        expected_fields: Dictionary of field names and their expected types
        allow_extra: Whether to allow extra fields in response

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        for field, expected_type in expected_fields.items():
            if field not in response_data:
                return False, f"Missing required field: {field}"

            if not isinstance(response_data[field], expected_type):
                return (
                    False,
                    f"Field {field} has incorrect type. "
                    f"Expected {expected_type}, got {type(response_data[field])}",
                )

        if not allow_extra and set(response_data.keys()) != set(expected_fields.keys()):
            extra_fields = set(response_data.keys()) - set(expected_fields.keys())
            return False, f"Unexpected extra fields in response: {extra_fields}"

        return True, None

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def create_test_step(step_name: str) -> allure.step:
    """
    Create an Allure test step with proper formatting.

    Args:
        step_name: Name of the test step

    Returns:
        allure.step context manager
    """
    return allure.step(step_name.strip().capitalize())


def format_error_message(error: Exception) -> str:
    """
    Format exception for better readability in test reports.

    Args:
        error: The exception to format

    Returns:
        Formatted error message
    """
    return f"{error.__class__.__name__}: {str(error)}"
