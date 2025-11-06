from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# This class allows us to handle MongoDB's _id
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *_):
        # Handle both string and ObjectId
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

# --- Your Data Models ---

class FoodItem(BaseModel):
    name: str
    quantity: float  # e.g., 10 (units), 2.5 (kg)
    unit: str        # e.g., "units", "kg", "liters"
    expiry_date: datetime
    
class Donor(BaseModel):
    # This setup allows MongoDB's '_id' to work with Pydantic's 'id'
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    address: str
    phone: str
    current_donations: List[FoodItem] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Recipient(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str         # e.g., "Downtown Shelter"
    address: str
    phone: str
    daily_need: float # e.g., "needs 50 kg of food per day"

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# --- ADD THIS NEW MODEL: ---
# Represents a food item available in the system,
# including *which* donor it came from.
class AvailableFood(FoodItem):
    donor_id: PyObjectId
    donor_name: str

# --- ADD THIS NEW MODEL: ---
# Represents a single proposed match
class MatchResult(BaseModel):
    recipient_id: PyObjectId
    recipient_name: str
    donor_id: PyObjectId
    donor_name: str
    food_name: str
    quantity_matched: float
    unit: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}