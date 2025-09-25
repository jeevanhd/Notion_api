from sys import version
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from notion_service import saveToNotion

version = "1.0.0"

app = FastAPI(
    title="Notion Integration API",
    description="API for saving topics to Notion database",
    version=version
)

class Topic(BaseModel):
    name: str = Field(..., min_length=1, max_length=2000, description="The title of the topic")
    content: str = Field(..., min_length=1, description="The content of the topic")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Python Basics",
                "content": "Python is a high-level programming language known for its simplicity and readability."
            }
        }

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    page_id: Optional[str] = None
    url: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_type: Optional[str] = None

@app.get("/", tags=["General"])
def home():
    """Root endpoint - returns a welcome message"""
    return {"message": "Welcome to Notion Integration API", "status": "active"}

@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "notion-integration-api"}

@app.get("/info", tags=["General"])
def api_info():
    """Get API information and available endpoints"""
    return {
        "name": "Notion Integration API",
        "version": version,
        "description": "API for saving topics to Notion database",
        "endpoints": {
            "GET /": "Welcome message",
            "GET /health": "Health check",
            "GET /info": "API information",
            "POST /save_topic": "Save a topic to Notion",
            "GET /docs": "Interactive API documentation"
        },
        "documentation": "/docs"
    }

@app.post("/save_topic", response_model=SuccessResponse, tags=["Topics"])
def save_topic(topic: Topic):
    """
    Save a new topic to Notion database
    
    - **name**: The title of the topic (required)
    - **content**: The content/description of the topic (required)
    
    Returns the created page details including URL if successful.
    """
    result = saveToNotion(topic.name, topic.content)
    
    if result["success"]:
        return SuccessResponse(
            message=result["message"],
            page_id=result.get("page_id"),
            url=result.get("url")
        )
    else:
        # Determine appropriate HTTP status code
        status_code = result.get("status_code", 500)
        if status_code == 401:
            status_code = 401  # Unauthorized
        elif status_code == 400:
            status_code = 400  # Bad Request
        elif status_code == 404:
            status_code = 404  # Not Found
        else:
            status_code = 500  # Internal Server Error
            
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "message": result["message"],
                "error_type": result.get("error_type")
            }
        )