# Presentation Notes: FastAPI Allure Pytest Template

## 1. Brief Intro of the Template

This repository is a comprehensive template for building robust and scalable APIs using FastAPI. It's designed for rapid development and includes pre-configured tools for testing, documentation, and deployment.

Key Features:
- **FastAPI**: For building high-performance APIs with Python.
- **Pytest**: For writing clean and maintainable tests.
- **Allure**: For generating beautiful and detailed test reports.
- **Docker**: For containerizing the application for consistent environments.
- **Pre-commit hooks**: For maintaining code quality and consistency.
- **Deployment Ready**: Scripts and configurations for deploying to Render and Railway.
- **CrewAI Integration**: Examples of how to integrate CrewAI for building AI-powered features.

## 2. Skip the installation step

(Self-explanatory - we will skip this during the demo)

## 3. Deploy the application locally

To run the application locally, we use `uv`, a fast Python package installer and resolver.

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### Run through the API endpoints

The following endpoints are available:

- **`GET /api/v1/hello`**: A simple "Hello World" endpoint.
- **`POST /api/v1/crewai/hello`**: A simple endpoint to test the CrewAI integration.
- **`POST /api/v1/content/create`**: Creates optimized content based on trends. This is a synchronous endpoint.
- **`POST /api/v1/content/create/async`**: Creates optimized content based on trends. This is an asynchronous endpoint.
- **`GET /api/v1/content/status/{task_id}`**: Checks the status of an asynchronous content creation task.
- **`POST /api/v1/content/trends`**: A quick endpoint for trend analysis only.
- **`GET /api/v1/content/health`**: Health check for the content creation service.
- **`DELETE /api/v1/content/cleanup/{task_id}`**: Cleans up a completed task.

## 4. Show the docs

FastAPI automatically generates interactive API documentation.

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 5. Show the pytests

The project uses `pytest` for testing. Tests are located in the `tests/` directory.

To run the tests:

```bash
pytest
```

## 6. Run the shell scripts

The project includes several shell scripts for common tasks:

- **`test_runner.sh`**: A comprehensive script to run tests, generate reports, and manage the environment.
- **`deploy.sh`**: A general-purpose deployment script.
- **`deploy-railway.sh`**: A script specifically for deploying to Railway.

Example of running the test runner:
```bash
./test_runner.sh
```

## 7. Show the reports

Allure is used to generate detailed test reports.

To generate and view the Allure report:

1.  Run tests with Allure:
    ```bash
    pytest --alluredir=allure-results
    ```
2.  Serve the report:
    ```bash
    allure serve allure-results
    ```

## 8. Show an example failure

To demonstrate a test failure, we can temporarily modify a test to make it fail. For example, change an assertion in `tests/test_api.py`.

(Live demo: modify a test, run pytest, show the failure in the console and in the Allure report).

## 9. Pre-commit example demo

This project uses `pre-commit` to enforce code quality before committing.

To demonstrate:
1.  Make a code change that violates a rule (e.g., bad formatting).
2.  Try to commit the change.
3.  `pre-commit` will run, detect the issue, and prevent the commit.
4.  Fix the issue (or let the hook fix it automatically) and commit again.

## 10. Deploy to Render

The `render.yaml` file defines the infrastructure for deploying to Render. The `README_RENDER_DEPLOYMENT.md` contains detailed instructions.

(Show the `render.yaml` file and walk through the deployment process on the Render dashboard).

## 11. Deploy to Railway

The `railway.json` and `Dockerfile.railway` files are used for deploying to Railway. The `README_RAILWAY_DEPLOYMENT.md` has the details.

(Show the `railway.json` file and walk through the deployment process on the Railway dashboard).

## 12. Show integration of CrewAI API in n8n

The `/api/v1/content/create` endpoint is designed for integration with n8n.

- **Workflow**:
    1. An n8n workflow is triggered (e.g., by a new row in a Google Sheet).
    2. The workflow sends a POST request to the `/api/v1/content/create` endpoint with the content ideas.
    3. The API processes the ideas using CrewAI.
    4. The results are sent back to n8n, which can then update the Google Sheet or perform other actions.

(Show the n8n workflow and demonstrate the end-to-end process).
