from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.database.connection import DatabaseConnection
from src.config.settings import get_settings

app = FastAPI(
    title="SQL Q&A Agent API",
    description="API for natural language to SQL queries using LangChain",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # Get settings and initialize database connection
    settings = get_settings()
    DatabaseConnection.get_connection()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    DatabaseConnection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)