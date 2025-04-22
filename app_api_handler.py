from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

# Custom imports
from src.agent.agent import run_sql_query_agent  # Update path as needed
from src.models.api_models import QueryRequest
from src.utils.logger import logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests and responses"""
    start_time = time.time()
    logger.info(f"Request started: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Request completed: {request.method} {request.url} - Status: {response.status_code} - Duration: {process_time:.2f}s")
    
    return response

@app.on_event("startup")
async def startup_event():
    """Log when the application starts"""
    logger.info("Application starting up")

@app.on_event("shutdown")
async def shutdown_event():
    """Log when the application shuts down"""
    logger.info("Application shutting down")

@app.get("/")
async def read_root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the LangChain SQL Q&A Agent API!"}

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process a natural language query"""
    logger.info(f"Received query request: {request.question}")
    try:
        result = run_sql_query_agent(request.question)
        logger.info("Query processed successfully")
        return {"answer": result}
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
