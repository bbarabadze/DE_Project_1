"""
    This module contains pydantic data models and validation functions for the API
"""
from pydantic import BaseModel, Field
from fastapi import HTTPException


class NameOccurrence(BaseModel):
    """ Data model for top names list"""
    name: str = Field(..., alias="Name")
    occurrences: int = Field(..., alias="Occurrences")


class UserActivity(BaseModel):
    """Data model for top active users' list"""
    user_id: int = Field(..., alias="User ID")
    name: str = Field(..., alias="Name")
    surname: str = Field(..., alias="Surname")
    activities: int = Field(..., alias="Activities")


def validate_top_number(number: int) -> None:
    """
    Validates top number, cannot be negative or greater than number of all users
    :param number: Number of top records
    :return: None
    """
    if not (0 < number <= 1000):
        raise HTTPException(status_code=400, detail="Input must be an integer between 1 and 1000")
