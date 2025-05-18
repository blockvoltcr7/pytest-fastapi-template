FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv tool for Python package management
RUN pip install uv

# Copy requirements files
COPY requirements.in requirements.txt ./

# Install dependencies using uv
RUN uv pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Create directory for allure results
RUN mkdir -p allure-results

# Command to run tests
CMD ["pytest", "--alluredir=allure-results"] 