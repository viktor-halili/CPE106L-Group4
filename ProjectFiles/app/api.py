from fastapi import FastAPI, HTTPException
from typing import List 
from app.models import (
    Donor, Recipient, FoodItem, 
    PyObjectId, AvailableFood,
    MatchResult, Pickup, PickupStop
)
import app.data as db
import app.match as match # Import your new match file



app = FastAPI(title="Food Rescue API")

@app.get("/")
def read_root():
    """A simple root endpoint to check if the server is running."""
    return {"message": "Welcome to the Food Rescue API!"}

# --- Donor Endpoints ---

@app.post("/donors", response_model=Donor)
def register_donor(donor: Donor):
    """Registers a new donor in the system."""
    donor_id = db.create_donor(donor)
    new_donor = db.get_donor_by_id(donor_id)
    if not new_donor:
        raise HTTPException(status_code=500, detail="Error creating donor")
    return new_donor

@app.get("/donors", response_model=List[Donor])
def get_all_donors():
    """Gets a list of all donors."""
    return db.get_all_donors()

@app.get("/donors/{donor_id}", response_model=Donor)
def get_donor(donor_id: str):
    """Gets a specific donor by their ID."""
    donor = db.get_donor_by_id(donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor

@app.post("/donors/{donor_id}/food", response_model=Donor)
def add_food_to_donor_api(donor_id: str, food_item: FoodItem):
    """Adds a food item to a specific donor's list."""
    
    success = db.add_food_to_donor(donor_id, food_item)
    
    if not success:
        raise HTTPException(status_code=404, detail="Donor not found or error adding food")
    
    # Return the donor with the updated food list
    updated_donor = db.get_donor_by_id(donor_id)
    if not updated_donor:
        raise HTTPException(status_code=404, detail="Donor not found after adding food")
    return updated_donor

# --- Recipient Endpoints ---

@app.post("/recipients", response_model=Recipient)
def register_recipient(recipient: Recipient):
    """Registers a new recipient in the system."""
    recipient_id = db.create_recipient(recipient)
    new_recipient = db.get_recipient_by_id(recipient_id)
    if not new_recipient:
        raise HTTPException(status_code=500, detail="Error creating recipient")
    return new_recipient

@app.get("/recipients", response_model=List[Recipient])
def get_all_recipients():
    """Gets a list of all recipients."""
    return db.get_all_recipients()

@app.get("/recipients/{recipient_id}", response_model=Recipient)
def get_recipient(recipient_id: str):
    """Gets a specific recipient by their ID."""
    recipient = db.get_recipient_by_id(recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return recipient

# --- Food & Matching Endpoints ---

@app.get("/food/available", response_model=List[AvailableFood])
def list_available_food():
    """Returns a list of all currently available food items
    with their donor info."""
    return db.get_all_available_food()

@app.post("/matches/run", response_model=List[MatchResult])
def run_matchmaker():
    """
    Runs the matching algorithm.
    Fetches all recipients and all available food,
    and returns a list of proposed matches.
    """
    try:
        all_recipients = db.get_all_recipients()
        all_food = db.get_all_available_food()
        
        matches = match.run_matching_algorithm(all_recipients, all_food)
        
        return matches
        
    except Exception as e:
        print(f"Error running matchmaker: {e}")
        raise HTTPException(status_code=500, detail="Error running matching algorithm")

# --- Logistics / Pickup Endpoints ---

@app.get("/pickups", response_model=List[Pickup])
def get_pending_pickups():
    """Gets a list of all pickup routes (e.g., all_pickups)."""
    return db.get_all_pickups()

@app.post("/pickups", response_model=Pickup)
def create_pickup_route(matches: List[MatchResult]):
    """
    Creates a new pickup route from a list of matches.
    This is a simplified version; a real version would
    run a route optimization algorithm here.
    """
    if not matches:
        raise HTTPException(status_code=400, detail="No matches provided to create a pickup")

    # --- Simple "Route" Generation ---
    stops: List[PickupStop] = []
    addresses_seen = set() # To help de-duplicate

    for match in matches:
        # Stop 1: Go to the donor
        donor = db.get_donor_by_id(str(match.donor_id)) # Use str()
        if donor and donor.address not in addresses_seen:
            stops.append(PickupStop(
                stop_type="pickup",
                name=match.donor_name,
                address=donor.address
            ))
            addresses_seen.add(donor.address)

        # Stop 2: Go to the recipient
        recipient = db.get_recipient_by_id(str(match.recipient_id)) # Use str()
        if recipient and recipient.address not in addresses_seen:
            stops.append(PickupStop(
                stop_type="dropoff",
                name=match.recipient_name,
                address=recipient.address
            ))
            addresses_seen.add(recipient.address)
    
    # Create the new Pickup object
    new_pickup = Pickup(
        matches=matches,
        stops=stops
    )
    
    # Save to database
    pickup_id = db.create_pickup(new_pickup)
    created_pickup = db.get_pickup_by_id(pickup_id)
    
    if not created_pickup:
        raise HTTPException(status_code=500, detail="Error creating pickup route")
        
    return created_pickup

@app.put("/pickups/{pickup_id}/complete", response_model=Pickup)
def complete_pickup_route(pickup_id: str):
    """
    Marks a pickup as 'complete' and updates the food inventory.
    This is the final, critical step!
    """
    
    # 1. Get the pickup
    pickup = db.get_pickup_by_id(pickup_id)
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup route not found")
    
    if pickup.status == "complete":
        raise HTTPException(status_code=400, detail="This pickup is already complete")

    # 2. "Close the loop" - Update the inventory
    print(f"--- Completing Pickup {pickup.id} ---")
    
    errors = []
    for match in pickup.matches:
        print(f"  > Updating: {match.quantity_matched} {match.unit} of {match.food_name} from {match.donor_name}")
        
        # Call our new database function
        success = db.update_food_item_quantity(match)
        
        if not success:
            error_msg = f"  > FAILED to update quantity for {match.food_name} from {match.donor_name}"
            print(error_msg)
            errors.append(error_msg)

    if errors:
        # In a real app, you might handle this differently
        # (e.g., not mark as complete, or save the errors)
        print("WARNING: Some items failed to update.")

    print("--------------------------------------")

    # 3. Update the pickup status
    success = db.update_pickup_status(pickup_id, "complete")
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update pickup status")
        
    pickup.status = "complete"
    return pickup