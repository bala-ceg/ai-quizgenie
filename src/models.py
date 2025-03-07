"""This module defines Pydantic models for this project.

These models are used mainly for the structured tool and LLM outputs.
Resources:
- https://docs.pydantic.dev/latest/concepts/models/
"""

from __future__ import annotations
from pydantic import BaseModel, Field

class QuizGenieState(BaseModel):
    """Represents the state in LangGraph workflow."""
    url: str
    num_questions: int = Field(default=5, description="Number of questions to generate")
    difficulty: str = Field(default="Medium", description="Quiz difficulty level")
    extracted_text: str = Field(default=None, description="Extracted text from URL")
    questions: list = Field(default=None, description="Generated quiz questions")
    model: str = Field(default="gpt-4o", description="LLM model to use for generation")
