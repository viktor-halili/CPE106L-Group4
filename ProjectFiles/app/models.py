from pydantic import BaseModel, Field
from pydantic_core import core_schema
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# This class allows us to handle MongoDB's _id
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: any, handler: any
    ) -> core_schema.CoreSchema:
        """
        Defines the Pydantic v2 CoreSchema for handling ObjectId.
        """
        
        # Validation chain for strings: first ensure it's a string,
        # then run our ObjectId validator. We DO NOT put this chain
        # into the JSON schema generation path below (we expose a
        # plain string schema for OpenAPI/JSON Schema generation).
        str_validator = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls._validate_str),
            ]
        )

        # Build a json_or_python schema that uses a plain string
        # for the JSON representation (so the JsonSchema generator
        # doesn't try to interpret our validator function), but
        # accepts either ObjectId instances or strings when parsing
        # Python input.
        schema = core_schema.json_or_python_schema(
            # When producing JSON / OpenAPI, represent as a string
            json_schema=core_schema.str_schema(),

            # When parsing Python input, accept either an ObjectId
            # instance or a string that will be validated by
            # `str_validator` defined above.
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    str_validator,
                ]
            ),

            # How to serialize (ObjectId -> str)
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v)
            ),
        )

        return schema

    @classmethod
    def _validate_str(cls, v: str) -> ObjectId:
        """Helper to validate a string as an ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

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

    model_config = {
        "arbitrary_types_allowed": True
    }

class Recipient(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str         # e.g., "Downtown Shelter"
    address: str
    phone: str
    daily_need: float # e.g., "needs 50 kg of food per day"

    model_config = {
        "arbitrary_types_allowed": True
    }

# Represents a food item available in the system,
# including *which* donor it came from.
class AvailableFood(FoodItem):
    donor_id: PyObjectId
    donor_name: str

# Represents a single proposed match
class MatchResult(BaseModel):
    recipient_id: PyObjectId
    recipient_name: str
    donor_id: PyObjectId
    donor_name: str
    food_name: str
    quantity_matched: float
    unit: str
    expiry_date: datetime  # <-- ADD THIS LINE

    model_config = {
        "arbitrary_types_allowed": True
    }

class PickupStop(BaseModel):
    """Represents a single stop (pickup or dropoff) in a delivery route."""
    stop_type: str  # "pickup" or "dropoff"
    name: str       # Donor or Recipient name
    address: str
    
class Pickup(BaseModel):
    """Repfresents a single, planned pickup/delivery route."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "pending" # "pending", "in_progress", "complete"
    
    # Stores the actual matches this pickup is fulfilling
    matches: List[MatchResult]
    
    # Stores the optimized list of stops
    stops: List[PickupStop]

    model_config = {
        "arbitrary_types_allowed": True
    }