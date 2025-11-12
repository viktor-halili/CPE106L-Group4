classDiagram
    direction LR  % Makes the diagram flow left-to-right

    class FoodItem {
        +String name
        +Float quantity
        +String unit
        +DateTime expiry_date
    }

    class AvailableFood {
        «Subclass»
        +PyObjectId donor_id
        +String donor_name
    }
    AvailableFood --|> FoodItem : Inherits

    class Donor {
        +PyObjectId id
        +String name
        +String address
        +String phone
        +FoodItem[*] current_donations
    }
    Donor "1" *-- "0..*" FoodItem : Contains

    class Recipient {
        +PyObjectId id
        +String name
        +String address
        +String phone
        +Float daily_need
    }

    class MatchResult {
        +PyObjectId recipient_id
        +String recipient_name
        +PyObjectId donor_id
        +String donor_name
        +String food_name
        +Float quantity_matched
        +String unit
        +DateTime expiry_date
    }

    class PickupStop {
        +String stop_type
        +String name
        +String address
    }

    class Pickup {
        +PyObjectId id
        +DateTime created_at
        +String status
        +MatchResult[*] matches
        +PickupStop[*] stops
    }
    Pickup "1" *-- "1..*" MatchResult : Fulfills
    Pickup "1" *-- "1..*" PickupStop : Has