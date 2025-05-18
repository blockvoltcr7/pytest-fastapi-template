# UV Package Manager: Core Concepts

## What is UV?
UV is a fast, modern Python package manager and build backend, designed as a drop-in replacement for pip, pip-tools, and virtualenv. It aims to provide reproducible, reliable, and efficient Python environments.

---

## Core Concepts

### 1. Installation
- **Install via pipx (recommended):**
  ```sh
  pipx install uv
  ```
- **Or via pip:**
  ```sh
  pip install uv
  ```

### 2. Creating a Virtual Environment
- Create a new environment in the current directory:
  ```sh
  uv venv
  ```
- Activate the environment:
  - **Unix/macOS:** `source .venv/bin/activate`
  - **Windows:** `.venv\Scripts\activate`

### 3. Installing Packages
- Install a package:
  ```sh
  uv pip install requests
  ```
- Install from a requirements file:
  ```sh
  uv pip install -r requirements.txt
  ```

### 4. Managing Dependencies
- **Lock dependencies for reproducibility:**
  ```sh
  uv pip compile requirements.in
  ```
- **Sync environment to lock file:**
  ```sh
  uv pip sync requirements.txt
  ```

### 5. Upgrading Packages
- Upgrade a package:
  ```sh
  uv pip install --upgrade package_name
  ```

### 6. Listing Installed Packages
- List all installed packages:
  ```sh
  uv pip list
  ```

### 7. Removing Packages
- Uninstall a package:
  ```sh
  uv pip uninstall package_name
  ```

### 8. Checking for Outdated Packages
- Check for outdated packages:
  ```sh
  uv pip list --outdated
  ```

---

## Best Practices
- Always use a virtual environment for your projects.
- Use lock files for reproducible builds.
- Regularly update your dependencies and lock files.
- Use `uv` commands as drop-in replacements for pip and virtualenv.

---

## Resources
- [UV Documentation](https://github.com/astral-sh/uv)
- [PyPI: uv](https://pypi.org/project/uv/) 