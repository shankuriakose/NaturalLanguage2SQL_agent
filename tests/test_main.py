import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
# Import the FastAPI app instance from the new location
from ai_sql_agent.app import app

# Mark all tests in this module to be run with asyncio
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def client():
    """Create an AsyncClient for testing the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

async def test_read_root(client: AsyncClient):
    """Test the root endpoint '/'."""
    response = await client.get("/")
    assert response.status_code == 200
    expected_json = {"message": "Welcome to the LangChain SQL Q&A Agent API!"}
    assert response.json() == expected_json

async def test_query_endpoint_success(client: AsyncClient):
    """Test the '/query' endpoint with a mocked successful agent response."""
    # Mock the agent_executor's ainvoke method
    with patch('ai_sql_agent.app.agent_executor.ainvoke', new_callable=AsyncMock) as mock_ainvoke:
        # Configure the mock to return a specific dictionary when called
        mock_ainvoke.return_value = {'output': 'mocked answer'}

        # Send a POST request to the /query endpoint
        response = await client.post("/query", json={"question": "test question"})

        # Assert the status code is 200 OK
        assert response.status_code == 200
        # Assert the response body matches the expected mocked answer
        assert response.json() == {"answer": "mocked answer"}
        # Verify that ainvoke was called once with the correct input
        mock_ainvoke.assert_awaited_once_with({"input": "test question"})

async def test_query_endpoint_agent_initialization_error(client: AsyncClient):
    """Test the '/query' endpoint when the agent_executor is None (initialization failed)."""
    # Temporarily set agent_executor to None for this test
    with patch('ai_sql_agent.app.agent_executor', None):
        response = await client.post("/query", json={"question": "test question"})
        # Expect 503 Service Unavailable based on current implementation
        assert response.status_code == 503
        assert response.json() == {"detail": "Service Unavailable: The query agent is not initialized."}


async def test_query_endpoint_agent_invocation_error(client: AsyncClient):
    """Test the '/query' endpoint when agent invocation raises an exception."""
    # Mock agent_executor's ainvoke to raise an exception
    with patch('ai_sql_agent.app.agent_executor.ainvoke', new_callable=AsyncMock) as mock_ainvoke:
        mock_ainvoke.side_effect = Exception("Test agent error")

        # Send a POST request
        response = await client.post("/query", json={"question": "test question"})

        # Assert the status code is 500 Internal Server Error
        assert response.status_code == 500
        # Assert the response body contains the generic error detail message
        # Based on the current implementation in main.py
        assert response.json() == {"detail": "An internal error occurred while processing your query."}
        # Verify that ainvoke was called
        mock_ainvoke.assert_awaited_once_with({"input": "test question"})
