# Standard library imports
import os

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain related imports
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_sql_agent, AgentExecutor # AgentExecutor needed for type hinting

# --- Load Environment Variables ---
# Load variables from the .env file into the environment
load_dotenv()

# --- Environment Variable Check ---
# Retrieve the Google API Key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")
# Ensure the Google API Key is set, raise error if not
if not google_api_key:
    raise ValueError("FATAL: GOOGLE_API_KEY environment variable not set.")

# --- FastAPI Application Initialization ---
# Create an instance of the FastAPI application
app = FastAPI(
    title="LangChain SQL Q&A Agent API",
    description="An API to query a SQL database using natural language via LangChain.",
    version="1.0.0",
)

# --- Database Connection Setup ---
# Define the database connection URI, using environment variable or a default SQLite DB
db_uri = os.getenv("DATABASE_URI", "sqlite:///data/northwind.db")
try:
    # Create the LangChain SQLDatabase connector instance
    db = SQLDatabase.from_uri(db_uri)
    print(f"Successfully connected to database: {db_uri}")
except Exception as e:
    # Handle potential errors during database connection setup
    print(f"FATAL: Error connecting to database ({db_uri}): {e}")
    # Exit if DB connection fails at startup, as the app is unusable
    exit(1)

# --- LLM and Agent Initialization ---
# Initialize agent_executor to None; it will be set if initialization succeeds
agent_executor: AgentExecutor | None = None
try:
    # Initialize the Google Generative AI model (Gemini Pro)
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=google_api_key,
        temperature=0.0  # Use low temperature for more deterministic SQL generation
    )
    # Create the LangChain SQL Agent Executor
    # agent_type="openai-tools" is used here; might require adjustments based on LLM capabilities
    # verbose=True enables detailed logging of the agent's thought process
    agent_executor = create_sql_agent(
        llm,
        db=db,
        agent_type="openai-tools",
        verbose=True
    )
    print("LLM and Agent initialized successfully.")
except Exception as e:
    # Handle potential errors during LLM or agent initialization
    print(f"WARNING: Error initializing LLM or Agent: {e}. Query endpoint will be disabled.")
    # agent_executor remains None if initialization fails

# --- API Endpoints ---

# --- Root Endpoint ---
@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint to check if the API server is running.
    Returns a simple welcome message.
    """
    return {"message": "Welcome to the LangChain SQL Q&A Agent API!"}


# --- Pydantic Model for Query Request ---
class QueryRequest(BaseModel):
    """
    Defines the structure for the request body of the /query endpoint.
    Requires a 'question' field containing the natural language query.
    """
    question: str


# --- Query Endpoint ---
@app.post("/query", tags=["Query"])
async def query_database(query: QueryRequest):
    """
    Handles natural language queries directed to the connected SQL database.

    - Accepts a POST request with a JSON body: `{"question": "Your question here"}`
    - Uses the initialized LangChain SQL agent to process the question.
    - Returns a JSON response: `{"answer": "The agent's answer"}`
    - Returns appropriate HTTP errors if the agent is not available or if processing fails.
    """
    # Check if the agent executor was successfully initialized
    if agent_executor is None:
        # Return a 503 Service Unavailable error if the agent isn't ready
        raise HTTPException(
            status_code=503, # Use 503 Service Unavailable
            detail="Service Unavailable: The query agent is not initialized."
        )

    try:
        # Invoke the agent asynchronously with the user's question
        # Potential errors handled: LLM interaction issues, SQL generation/execution failures,
        # database connection problems during query execution.
        agent_response = await agent_executor.ainvoke({"input": query.question})

        # Extract the answer from the agent's response dictionary
        # Assumes the answer is stored under the 'output' key
        answer = agent_response.get("output", "Sorry, I couldn't find an answer.")

        return {"answer": answer}
    except Exception as e:
        # Catch-all for unexpected errors during agent execution
        # It's recommended to log the detailed error `e` internally for debugging
        print(f"Error during agent invocation: {e}") # Basic logging
        # Return a generic 500 Internal Server Error to the client
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your query."
        )