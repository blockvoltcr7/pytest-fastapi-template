# Allure Report Framework - Installation & Usage Guide

Allure is a flexible, lightweight multi-language test reporting tool that provides clear graphical reports for test results. This guide will help you install and set up Allure Report on your machine for use with Python projects (e.g., pytest).

---

## 1. Prerequisites

- **Java**: Allure requires Java 8 or higher to be installed on your system.
- **Python**: Ensure Python 3.6+ is installed.
- **pip**: Python package manager.

### Check Java Installation

```bash
java -version
```

If Java is not installed:
- **macOS**: Install via Homebrew: `brew install openjdk@11`
- **Windows**: Download from [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.org/)

---

## 2. Install Allure Commandline

### **macOS Installation**

#### **Option 1: Using Homebrew (Recommended)**

```bash
# Install Homebrew ----> ****if not already installed**** <----
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Allure
brew install allure
```

#### **Option 2: Manual Installation**

```bash
# Download the latest release
curl -o allure-2.29.0.zip -L https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip

# Extract
unzip allure-2.29.0.zip

# Move to applications folder
sudo mv allure-2.29.0 /usr/local/

# Add to PATH in your shell profile (.zshrc, .bash_profile, etc.)
echo 'export PATH="/usr/local/allure-2.29.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### **Windows Installation**

#### **Option 1: Using Chocolatey (Recommended)**

```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Allure
choco install allure
```

#### **Option 2: Using Scoop**

```powershell
# Install Scoop if not already installed
iwr -useb get.scoop.sh | iex

# Install Allure
scoop install allure
```

#### **Option 3: Manual Installation**

1. **Download**: Go to [Allure Releases](https://github.com/allure-framework/allure2/releases) and download the latest ZIP file
2. **Extract**: Extract to a folder like `C:\allure-2.29.0`
3. **Add to PATH**:
   - Open System Properties → Advanced → Environment Variables
   - Add `C:\allure-2.29.0\bin` to your PATH variable
   - Restart Command Prompt/PowerShell

### **Linux Installation**

#### **Using Package Manager**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install allure

# CentOS/RHEL/Fedora
sudo yum install allure
# or
sudo dnf install allure
```

#### **Manual Installation**

```bash
# Download and extract
wget -O allure-2.29.0.zip https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip
unzip allure-2.29.0.zip
sudo mv allure-2.29.0 /opt/

# Add to PATH
echo 'export PATH="/opt/allure-2.29.0/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 3. Verify Installation

After installation, verify Allure is working:

```bash
allure --version
```

You should see something like:
```
2.29.0
```

---

## 4. Python Setup

Install the allure-pytest plugin:

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows

# Install allure-pytest (already included in this project)
uv pip install allure-pytest
```

---

## 5. Usage with This Project

### **Generate Test Results**

```bash
# Run tests and generate Allure results
pytest --alluredir=allure-results -v

# Run specific test file
pytest tests/test_fastapi_endpoints.py --alluredir=allure-results -v

# Run AI tests
pytest tests/ai-tests/ --alluredir=allure-results -v
```

### **Serve Allure Report**

```bash
# Generate and serve the report (opens in browser)
allure serve allure-results

# Or generate static report
allure generate allure-results -o allure-report --clean
```

### **Open Static Report**

```bash
# After generating static report
allure open allure-report
```

---

## 6. Troubleshooting

### **Common Issues**

**1. "allure: command not found"**
- Ensure Allure is properly added to your PATH
- Restart your terminal/command prompt
- Verify installation with `allure --version`

**2. "Java not found" error**
- Install Java 8 or higher
- Verify with `java -version`
- Set JAVA_HOME environment variable if needed

**3. "No test results found"**
- Ensure you're running pytest with `--alluredir=allure-results`
- Check that the allure-results directory contains XML files
- Verify allure-pytest is installed: `pip list | grep allure`

**4. Permission errors (macOS/Linux)**
- Use `sudo` for system-wide installation
- Or install to user directory: `--user` flag with pip

**5. Windows PATH issues**
- Restart Command Prompt/PowerShell after PATH changes
- Use full path to allure.bat if needed: `C:\allure-2.29.0\bin\allure.bat`

### **Alternative: Docker Usage**

If you prefer not to install Allure locally:

```bash
# Generate report using Docker
docker run --rm -v $(pwd)/allure-results:/app/allure-results -v $(pwd)/allure-report:/app/allure-report -p 4040:4040 frankescobar/allure-docker-service
```

---

## 7. Advanced Configuration

### **Custom Allure Configuration**

Create `allure.properties` in your project root:

```properties
allure.results.directory=allure-results
allure.link.issue.pattern=https://github.com/your-repo/issues/{}
allure.link.tms.pattern=https://your-tms.com/browse/{}
```

### **Environment Information**

The project automatically includes environment information in reports via `conftest.py`. You can customize this by editing the `pytest_configure` hook.

---

## 8. Resources

- **Official Documentation**: [https://docs.qameta.io/allure/](https://docs.qameta.io/allure/)
- **GitHub Repository**: [https://github.com/allure-framework/allure2](https://github.com/allure-framework/allure2)
- **Allure Pytest Plugin**: [https://github.com/allure-framework/allure-python](https://github.com/allure-framework/allure-python)
