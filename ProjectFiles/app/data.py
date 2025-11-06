from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.models import (
    Donor, Recipient, FoodItem, 
    PyObjectId, AvailableFood
)
from typing import List, Optional
from bson import ObjectId

# --- Database Connection ---
try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command('ping')
    print("MongoDB connection successful.")
except ConnectionFailure:
    print("MongoDB connection failed. Is the server running?")
    client = None

if client:
    db = client.food_rescue_db
    donors_collection = db.donors
    recipients_collection = db.recipients
else:
    db = None
    donors_collection = None
    recipients_collection = None

# --- Donor Functions ---

def create_donor(donor: Donor) -> str:
    """Adds a new donor to the DB and returns their new ID."""
    donor_dict = donor.model_dump(by_alias=True, exclude=["id"])
    result = donors_collection.insert_one(donor_dict)
    return str(result.inserted_id)

def get_donor_by_id(donor_id: str) -> Optional[Donor]:
    """Fetches a single donor from the DB by their string ID."""
    try:
        data = donors_collection.find_one({"_id": ObjectId(donor_id)})
        if data:
            return Donor(**data)
    except Exception as e:
        print(f"Error finding donor: {e}")
        return None
    return None

def get_all_donors() -> List[Donor]:
    """Fetches all donors from the DB."""
    donors = []
    for data in donors_collection.find():
        donors.append(Donor(**data))
    return donors

# --- Recipient Functions ---

def create_recipient(recipient: Recipient) -> str:
    """Adds a new recipient to the DB and returns their new ID."""
    recipient_dict = recipient.model_dump(by_alias=True, exclude=["id"])
    result = recipients_collection.insert_one(recipient_dict)
    return str(result.inserted_id)

def get_recipient_by_id(recipient_id: str) -> Optional[Recipient]:
    """Fetches a single recipient from the DB."""
    try:
        data = recipients_collection.find_one({"_id": ObjectId(recipient_id)})
        if data:
            return Recipient(**data)
    except Exception as e:
        print(f"Error finding recipient: {e}")
        return None
    return None

def get_all_recipients() -> List[Recipient]:
    """Fetches all recipients from the DB."""
    recipients = []
    for data in recipients_collection.find():
        recipients.append(Recipient(**data))
    return recipients

# --- Food/Donation Functions ---

def add_food_to_donor(donor_id: str, food_item: FoodItem) -> bool:
    """Adds a new food item to a specific donor's 'current_donations' list."""
    food_dict = food_item.model_dump()
    result = donors_collection.update_one(
        {"_id": ObjectId(donor_id)},
        {"$push": {"current_donations": food_dict}}
    )
    return result.modified_count > 0

def get_all_available_food() -> List[AvailableFood]:
    """Finds all food items and includes their donor's ID and name."""
    pipeline = [
        {"$unwind": "$current_donations"}, # De-nest the food items
        {
            "$project": { # Reshape the document to include donor info
                "_id": 0, # Exclude the default _id
                "donor_id": "$_id",
                "donor_name": "$name",
                "name": "$current_donations.name",
                "quantity": "$current_donations.quantity",
                "unit": "$current_donations.unit",
                "expiry_date": "$current_donations.expiry_date"
            }
        }
    ]
    available_food_list = []
    for food_data in donors_collection.aggregate(pipeline):
        available_food_list.append(AvailableFood(**food_data))
    return available_food_list