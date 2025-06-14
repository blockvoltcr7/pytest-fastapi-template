from fastapi import APIRouter
from pydantic import BaseModel
from crewai import Agent, Crew, Task

router = APIRouter()


class CrewAIRequest(BaseModel):
    role: str = "Greeter"
    goal: str = "Say hello to the world"
    backstory: str = "Loves greeting everyone."
    task_description: str = "Say hello to the world."
    expected_output: str = "Hello, world!"


class CrewAIResponse(BaseModel):
    result: str
    status: str


@router.post(
    "/crewai/hello",
    summary="Run CrewAI Hello World Agent",
    description="Execute a CrewAI agent that says hello to the world",
    response_description="The result from the CrewAI agent execution",
    response_model=CrewAIResponse,
)
async def run_crewai_hello(request: CrewAIRequest = CrewAIRequest()) -> CrewAIResponse:
    """Run a CrewAI agent to say hello to the world

    Args:
        request: The CrewAI configuration request

    Returns:
        CrewAIResponse: The result from the agent execution
    """
    try:
        agent = Agent(
            role=request.role,
            goal=request.goal,
            backstory=request.backstory,
            verbose=True
        )

        task = Task(
            description=request.task_description,
            expected_output=request.expected_output,
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task]
        )

        result = crew.kickoff()

        return CrewAIResponse(
            result=result.raw,
            status="success"
        )
    except Exception as e:
        return CrewAIResponse(
            result=f"Error: {str(e)}",
            status="error"
        )
