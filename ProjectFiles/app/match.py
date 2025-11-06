from app.models import Recipient, AvailableFood, MatchResult
from typing import List

def run_matching_algorithm(
    all_recipients: List[Recipient], 
    all_food: List[AvailableFood]
) -> List[MatchResult]:
    """
    Runs a greedy matching algorithm.
    Sorts recipients by need and tries to fulfill that need
    with the available food items.
    """
    
    # 1. Sort recipients by need (neediest first)
    # We make a copy so we can modify their 'daily_need'
    recipients_sorted = sorted(
        [r.model_copy(deep=True) for r in all_recipients], 
        key=lambda r: r.daily_need, 
        reverse=True
    )
    
    # 2. Create a mutable list of available food
    # We'll "use up" food items by reducing their quantity
    food_available = [f.model_copy(deep=True) for f in all_food]
    
    proposed_matches: List[MatchResult] = []

    # 3. Iterate through each recipient and try to match
    for recipient in recipients_sorted:
        need_remaining = recipient.daily_need
        
        # Keep matching food until this recipient's need is met
        # or we run out of food items
        for food in food_available:
            
            # Skip food that's already used up
            if food.quantity <= 0:
                continue
                
            # For simplicity, we assume all units are compatible (e.g., "kg")
            # A real app would have unit conversion
            
            if food.quantity >= need_remaining:
                # This food item can fulfill the rest of the need
                quantity_to_match = need_remaining
                
                # Create the match record
                match = MatchResult(
                    recipient_id=recipient.id,
                    recipient_name=recipient.name,
                    donor_id=food.donor_id,
                    donor_name=food.donor_name,
                    food_name=food.name,
                    quantity_matched=quantity_to_match,
                    unit=food.unit
                )
                proposed_matches.append(match)
                
                # Update the food quantity and the recipient's remaining need
                food.quantity -= quantity_to_match
                need_remaining = 0
                
                # This recipient is done, break to the next recipient
                break
                
            else:
                # This food item can be partially used
                quantity_to_match = food.quantity
                
                match = MatchResult(
                    recipient_id=recipient.id,
                    recipient_name=recipient.name,
                    donor_id=food.donor_id,
                    donor_name=food.donor_name,
                    food_name=food.name,
                    quantity_matched=quantity_to_match,
                    unit=food.unit
                )
                proposed_matches.append(match)
                
                # Update the food quantity and the recipient's remaining need
                food.quantity = 0 # Food item is used up
                need_remaining -= quantity_to_match
                
                # Continue to the next food item for this recipient
    
    return proposed_matches