import allure
import pytest
import time
from crewai import Agent, Crew, Task

@allure.epic("CrewAI Tests")
@allure.feature("Agent Tests")
@allure.story("Greeter Agent")
@allure.title("Test Greeter Agent Says Hello World")
@pytest.mark.smoke
def test_greeter_agent_hello_world():
    with allure.step("Define Agent, Task, and Crew"):
        agent = Agent(
            role="Greeter",
            goal="Say hello to the world",
            backstory="Loves greeting everyone.",
            verbose=True
        )
        task = Task(
            description="Say hello to the world.",
            expected_output="Hello, world!",
            agent=agent
        )
        crew = Crew(
            agents=[agent],
            tasks=[task]
        )

    with allure.step("Run the Crew and get the result"):
        result = crew.kickoff()

    with allure.step("Verify the result"):
        assert result.raw == "Hello, world!"
