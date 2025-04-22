from pydantic import BaseModel, Field, validator
from src.utils.logger import logger

class QueryRequest(BaseModel):
    """Model for query request"""
    question: str = Field(..., description="The natural language question to process")

    @validator('question')
    def validate_query(cls, v):
        """Validate the query string"""
        if not v:
            error_msg = "Query string cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)
        if len(v) > 1000:  # Maximum query length
            error_msg = f"Query too long ({len(v)} chars). Maximum length is 1000 characters"
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.debug(f"Query validation passed: {v[:100]}...")  # Log first 100 chars
        return v

class QueryResponse(BaseModel):
    """Model for query response"""
    answer: str = Field(..., description="The answer to the question")

    @validator('answer')
    def validate_result(cls, v):
        """Validate the response string"""
        if not v:
            error_msg = "Result cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.debug(f"Response validation passed: {v[:100]}...")  # Log first 100 chars
        return v

class ErrorResponse(BaseModel):
    """Model for error response"""
    detail: str = Field(..., description="Error detail message")