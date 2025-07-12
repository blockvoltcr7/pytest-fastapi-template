# Gamma Presentation Prompt: FastAPI GenAI Template Demo

**Audience**: Technical developers, DevOps teams, AI engineers  
**Goal**: Demonstrate a production-ready FastAPI template with AI integrations and comprehensive testing

---

## 1. Project Anatomy (Overview)
**Slide Title**: "Built for AI Development Excellence"

**Key Points**:
- **`.cursor/rules/`** → Smart AI assistant configuration
  - `dependency-mgmt.mdc`: Always use UV, never pip
  - `testing-rules.mdc`: Pytest + Allure integration standards
  - `pydanticv2-rules.mdc`: API validation best practices
- **`CLAUDE.md`** → AI-powered development guidance
  - Focus on `/init` command for instant codebase understanding
  - Claude Code integration for intelligent assistance
- **`.mcp.json`** → Model Context Protocol configuration
  - Structured AI interaction capabilities
- **`ai-docs/`** → Comprehensive AI development documentation
- **`pyproject.toml` + `uv.lock`** → Modern Python dependency management

**Why This Matters**: "Skip the setup headaches. Start building AI features on Day 1."

---

## 2. Setup & Installation
**Slide Title**: "From Zero to AI API in Under 60 Seconds"

**Key Points**:
- **UV Package Manager Benefits**:
  - 10x faster than pip
  - Reliable dependency resolution
  - Automatic virtual environment management
- **One-Command Setup**:
  ```bash
  git clone repo && cd repo && uv sync
  ```
- **Instant Development Server**:
  ```bash
  uv run uvicorn app.main:app --reload
  ```
- **No Manual Environment Management**: UV handles everything automatically

**Demo Flow**:
1. Clone repository
2. Run `uv sync` (show speed)
3. Start server with `uv run uvicorn app.main:app --reload`
4. API running at `http://localhost:8000`

**Why This Matters**: "Eliminate environment issues. Get your team productive immediately."

---

## 3. API Documentation
**Slide Title**: "Self-Documenting APIs That Actually Work"

**Key Points**:
- **Automatic Documentation Generation**:
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`
- **Real API Endpoints**:
  - `GET /health` → System health check
  - `GET /api/v1/hello` → Basic endpoint
  - `POST /api/v1/crewai` → AI agent execution
  - `POST /api/v1/content-crew` → Content creation workflows
  - `POST /api/v1/gemini/podcast` → Multi-speaker TTS generation
- **Interactive Testing**: Try endpoints directly in browser
- **Type Safety**: Pydantic V2 validation with clear error messages

**Demo Flow**:
1. Open `/docs` endpoint
2. Explore API schema
3. Test a live endpoint
4. Show validation error handling

**Why This Matters**: "Your API documentation is always up-to-date and testable."

---

## 4. Testing Framework
**Slide Title**: "Production-Grade Testing Made Simple"

**Key Points**:
- **Pytest + Allure Integration** (configured by default):
  ```bash
  # pytest.ini automatically includes --alluredir=allure-results
  uv run pytest -v
  ```
- **Convenience Test Runner**:
  ```bash
  ./test_runner.sh all                    # Run all tests
  ./test_runner.sh file tests/demo/test_hello.py  # Specific file
  ./test_runner.sh group "API Tests"      # By feature group
  ./test_runner.sh list-groups           # See available groups
  ```
- **Multi-Environment Support**: dev/uat/prod configurations
- **Rich Test Reporting**: Allure generates beautiful HTML reports
- **Test Categories**: API, integration, smoke tests with markers

**Demo Flow**:
1. Run `./test_runner.sh all`
2. Show test execution with real-time results
3. Generate Allure report: `allure serve allure-results`
4. Explore rich test reporting interface
5. Demo a failing test and error reporting

**Why This Matters**: "Catch issues before they reach production. Beautiful reports for stakeholders."

---

## 5. Project Functionality
**Slide Title**: "Multi-AI Provider Architecture in Action"

**Key Points**:
- **AI Provider Integrations**:
  - **OpenAI**: GPT models and DALL-E image generation
  - **Google Gemini**: Advanced language models and TTS
  - **ElevenLabs**: High-quality voice synthesis
  - **CrewAI**: Multi-agent AI orchestration
- **Real Use Cases**:
  - Content creation workflows
  - Multi-speaker podcast generation
  - Image generation with prompts
  - Agent-based task execution
- **Project Architecture**:
  - `app/services/`: AI service integrations
  - `app/agents/`: CrewAI agent implementations
  - `app/tools/`: AI workflow utilities
- **Environment Configuration**: Secure API key management

**Demo Flow**:
1. Show project structure
2. Explore `app/services/image_service.py`
3. Demo actual API call (if keys available)
4. Show response handling and validation

**Why This Matters**: "Build sophisticated AI features without vendor lock-in."

---

## 6. Deployment
**Slide Title**: "Deploy Anywhere in Minutes"

**Key Points**:
- **Multiple Deployment Targets**:
  - **Render**: `render.yaml` configuration
  - **Railway**: `railway.json` + specialized Dockerfile
  - **Docker**: Multi-stage builds with UV optimization
- **Production-Ready Features**:
  - Health check endpoints
  - Environment variable management
  - Automatic dependency installation
  - Zero-downtime deployment support
- **One-Command Deploy**:
  ```bash
  # Railway example
  railway up
  
  # Docker example  
  docker build -t genai-api . && docker run -p 8000:8000 genai-api
  ```

**Demo Flow**:
1. Show `render.yaml` and `railway.json` configs
2. Demonstrate Docker build process
3. Show deployed API with live endpoints
4. Verify `/docs` accessibility in production

**Why This Matters**: "From development to production without DevOps complexity."

---

## 7. Integration Demo
**Slide Title**: "Real-World AI Automation"

**Key Points**:
- **n8n Workflow Integration**:
  - Trigger: Google Sheets new row / webhook / schedule
  - Action: POST to `/api/v1/content-crew`
  - Process: AI-generated content creation
  - Result: Update sheet / send email / publish content
- **Business Scenarios**:
  - **Podcast Generation**: Multi-speaker TTS from scripts
  - **Content Marketing**: Trend-based article creation
  - **Email Campaigns**: Personalized content generation
- **API Integration Points**:
  - Webhook endpoints for external triggers
  - Async processing for long-running tasks
  - Status checking and result retrieval

**Demo Flow**:
1. Show n8n workflow canvas
2. Configure API connection
3. Trigger workflow with sample data
4. Show real-time processing
5. Display generated results

**Why This Matters**: "Turn AI capabilities into business automation. Scale content creation effortlessly."

---

## Presentation Guidelines for Gamma

**Slide Design**:
- 1-2 key concepts per slide
- Clean, minimal layout
- Code blocks with syntax highlighting
- Screenshots of actual interfaces
- Consistent color scheme

**Visual Elements**:
- Architecture diagrams for project structure
- Before/after comparisons for setup speed
- Live terminal/browser screenshots
- Workflow diagrams for integrations

**Speaker Notes Include**:
- Exact commands to run
- Expected output descriptions
- Troubleshooting common issues
- Technical details for Q&A

**Call to Action**:
"Ready to build production-grade AI APIs? Clone this template and ship your first AI feature today."

---

**Total Presentation Time**: 15-20 minutes + Q&A
**Demo Preparation**: Have local environment running, API keys configured, test data ready