# Pytest for API Testing: Quick Start Guide

## What is Pytest?
Pytest is a powerful and easy-to-use testing framework for Python. It is widely used for unit, integration, and API testing.

---

## Installation
Install pytest and requests (for API testing):
```sh
pip install pytest requests
```

For reporting options:
```sh
# For HTML reports
pip install pytest-html

# For Allure reports
pip install allure-pytest
```

---

## Basic Pytest Commands
- Run all tests:
  ```sh
  pytest
  ```
- Run tests in a specific file:
  ```sh
  pytest tests/test_api.py
  ```
- Show detailed output:
  ```sh
  pytest -v
  ```
- Stop after first failure:
  ```sh
  pytest -x
  ```
- Generate an HTML report:
  ```sh
  pytest --html=report.html
  ```
- Generate Allure report data:
  ```sh
  pytest --alluredir=allure-results
  ```

---

## Writing API Tests with Pytest
Create a `tests/` folder and add a file like `test_api.py`:

```python
import requests

def test_status_code():
    response = requests.get('https://api.example.com/endpoint')
    assert response.status_code == 200

def test_json_response():
    response = requests.get('https://api.example.com/endpoint')
    data = response.json()
    assert 'key' in data
```

### Tips for API Testing
- Use fixtures for setup/teardown (e.g., authentication tokens).
- Parametrize tests to cover multiple cases.
- Use `requests` or `httpx` for making HTTP calls.

---

## Reporting Frameworks

### pytest-html
- **pytest-html** is a simple plugin to generate attractive HTML reports.
- To use:
  ```sh
  pytest --html=report.html
  ```
- Open `report.html` in your browser to view results.

### Allure Report
- **Allure Report** provides beautiful, interactive test reports with rich details and visualizations.

#### Allure Report Setup
1. Install Allure command-line tool:
   - macOS: `brew install allure`
   - Windows: `scoop install allure` or download from [GitHub releases](https://github.com/allure-framework/allure2/releases)
   - Linux: See [installation instructions](https://allurereport.org/docs/install-linux/)

2. Run tests with Allure data collection:
   ```sh
   pytest --alluredir=allure-results
   ```

3. Generate and open the report:
   ```sh
   allure serve allure-results
   ```

#### Enhancing Tests with Allure Features
```python
import allure
import requests

@allure.feature("API")
@allure.story("Authentication")
def test_login_endpoint():
    with allure.step("Send login request"):
        response = requests.post(
            'https://api.example.com/login', 
            json={"username": "test", "password": "test"}
        )
    
    with allure.step("Verify status code"):
        assert response.status_code == 200
        
    with allure.step("Verify token is present"):
        data = response.json()
        assert "token" in data
        
        # Attach the response data to the report
        allure.attach(
            str(data), 
            name="Response JSON",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

## Resources
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [pytest-html Plugin](https://github.com/pytest-dev/pytest-html)
- [Requests Library](https://docs.python-requests.org/en/latest/)
- [Allure Report Documentation](https://allurereport.org/docs/pytest/) 