"""
schemas/response_models.py — Pydantic response schemas for all API endpoints.
Using strict typing ensures Flutter always receives consistent JSON structures.
"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response schema for the GET /health endpoint."""
    healthy: bool = Field(..., description="True if the service is healthy.")


class VersionResponse(BaseModel):
    """Response schema for the GET /version endpoint."""
    version: str = Field(..., description="Current API version string.")


class RootResponse(BaseModel):
    """Response schema for the GET / endpoint."""
    service: str = Field(..., description="Service name.")
    status: str = Field(..., description="Current service status.")


class PredictionResponse(BaseModel):
    """Response schema for single-model prediction endpoints."""
    prediction: str = Field(..., description="The predicted label (e.g., 'A').")
    confidence: float = Field(..., description="Confidence percentage (0-100).")


class CombinedPredictionResponse(BaseModel):
    """Response schema for the POST /predict-both endpoint."""
    alphabet: str = Field(..., description="Predicted letter from the image model.")
    speech: str = Field(..., description="Predicted label from the speech model.")
    match: bool = Field(..., description="True if both predictions match.")
    confidence: float = Field(..., description="Averaged confidence percentage (0-100).")


class ErrorResponse(BaseModel):
    """Standard error response returned on all failures."""
    error: str = Field(..., description="Human-readable error description.")
