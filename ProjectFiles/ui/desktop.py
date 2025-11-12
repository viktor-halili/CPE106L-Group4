import flet as ft
import requests
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "Food Rescue Platform"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # --- Donor Tab Controls ---
    donor_name = ft.TextField(label="Donor Name", width=300)
    donor_address = ft.TextField(label="Address", width=300)
    donor_phone = ft.TextField(label="Phone", width=300)
    donor_register_status = ft.Text(value="", color=ft.Colors.GREEN)
    donor_list = ft.ListView(expand=1, spacing=10)
    
    selected_donor_id = ft.Text("No donor selected")
    food_name = ft.TextField(label="Food Item Name", width=250)
    food_qty = ft.TextField(label="Quantity", width=100)
    food_unit = ft.TextField(label="Unit (e.g., kg)", width=100)
    add_food_status = ft.Text(value="", color=ft.Colors.GREEN)
    
    # --- Recipient Tab Controls ---
    recipient_name = ft.TextField(label="Recipient Name", width=300)
    recipient_address = ft.TextField(label="Address", width=300)
    recipient_phone = ft.TextField(label="Phone", width=300)
    recipient_need = ft.TextField(label="Daily Need (e.g., kg)", width=300)
    recipient_register_status = ft.Text(value="", color=ft.Colors.GREEN)
    recipient_list = ft.ListView(expand=1, spacing=10)

    # --- Matching Tab Controls ---
    match_run_status = ft.Text(value="", color=ft.Colors.BLUE)
    match_list = ft.ListView(expand=1, spacing=10)

    # --- Logistics Tab Controls (NEW) ---
    logistics_matches_list = ft.ListView(expand=1, spacing=10)
    logistics_pending_list = ft.ListView(expand=1, spacing=10)
    logistics_status = ft.Text(value="", color=ft.Colors.BLUE)
    
    # This will hold the raw JSON data of the matches
    page.client_storage.set("current_matches", []) 

    # --- Event Handlers (Donors) ---
    
    def register_donor_click(e):
        try:
            donor_data = {
                "name": donor_name.value,
                "address": donor_address.value,
                "phone": donor_phone.value,
                "current_donations": []
            }
            response = requests.post(f"{API_URL}/donors", json=donor_data)
            
            if response.status_code == 200:
                donor_register_status.value = f"Success! Donor '{donor_name.value}' created."
                donor_register_status.color = ft.Colors.GREEN
                donor_name.value, donor_address.value, donor_phone.value = "", "", ""
                refresh_donor_list(e)
            else:
                donor_register_status.value = f"Error: {response.json().get('detail')}"
                donor_register_status.color = ft.Colors.RED
        except Exception as ex:
            donor_register_status.value = f"API connection error: {ex}"
            donor_register_status.color = ft.Colors.RED
        page.update()

    def refresh_donor_list(e):
        try:
            response = requests.get(f"{API_URL}/donors")
            if response.status_code == 200:
                donors = response.json()
                donor_list.controls.clear()
                for donor in donors:
                    donor_list.controls.append(
                        ft.ListTile(
                            title=ft.Text(donor['name']),
                            subtitle=ft.Text(donor['address']),
                            data=donor['_id'],
                            on_click=select_donor_click
                        )
                    )
                donor_register_status.value = f"Loaded {len(donors)} donors."
                donor_register_status.color = ft.Colors.BLUE
            else:
                donor_register_status.value = "Error fetching donors."
                donor_register_status.color = ft.Colors.RED
        except Exception as ex:
            donor_register_status.value = f"API connection error: {ex}"
            donor_register_status.color = ft.Colors.RED
        
        if e:
            page.update()
        
    def select_donor_click(e):
        selected_donor_id.value = e.control.data
        add_food_status.value = f"Selected {e.control.title.value}"
        add_food_status.color = ft.Colors.BLUE
        page.update()

    def add_food_click(e):
        donor_id = selected_donor_id.value
        if donor_id == "No donor selected":
            add_food_status.value = "Error: Please select a donor first!"
            add_food_status.color = ft.Colors.RED
            page.update()
            return
        try:
            # TODO: Add a DatePicker for expiry
            expiry = (datetime.now() + timedelta(days=5)).isoformat()
            
            food_data = {
                "name": food_name.value,
                "quantity": float(food_qty.value),
                "unit": food_unit.value,
                "expiry_date": expiry
            }
            
            response = requests.post(f"{API_URL}/donors/{donor_id}/food", json=food_data)
            
            if response.status_code == 200:
                add_food_status.value = f"Added '{food_name.value}'!"
                add_food_status.color = ft.Colors.GREEN
                food_name.value, food_qty.value, food_unit.value = "", "", ""
            else:
                add_food_status.value = f"Error: {response.json().get('detail')}"
                add_food_status.color = ft.Colors.RED
                
        except Exception as ex:
            add_food_status.value = f"Error: {ex}"
            add_food_status.color = ft.Colors.RED
            
        page.update()

    # --- Event Handlers (Recipients) ---

    def register_recipient_click(e):
        try:
            try:
                daily_need_float = float(recipient_need.value)
            except ValueError:
                recipient_register_status.value = "Error: 'Daily Need' must be a number (e.g., 50)."
                recipient_register_status.color = ft.Colors.RED
                page.update()
                return 

            recipient_data = {
                "name": recipient_name.value,
                "address": recipient_address.value,
                "phone": recipient_phone.value,
                "daily_need": daily_need_float
            }
            
            response = requests.post(f"{API_URL}/recipients", json=recipient_data)
            
            if response.status_code == 200:
                recipient_register_status.value = f"Success! Recipient '{recipient_name.value}' created."
                recipient_register_status.color = ft.Colors.GREEN
                recipient_name.value, recipient_address.value, recipient_phone.value, recipient_need.value = "", "", "", ""
                refresh_recipient_list(e)
            else:
                recipient_register_status.value = f"Error: {response.json().get('detail')}"
                recipient_register_status.color = ft.Colors.RED
        
        except requests.exceptions.RequestException as ex:
            recipient_register_status.value = f"API connection error: {ex}"
            recipient_register_status.color = ft.Colors.RED
        except Exception as ex:
            recipient_register_status.value = f"An unexpected error occurred: {ex}"
            recipient_register_status.color = ft.Colors.RED
        page.update()

    def refresh_recipient_list(e):
        try:
            response = requests.get(f"{API_URL}/recipients")
            if response.status_code == 200:
                recipients = response.json()
                recipient_list.controls.clear()
                for recipient in recipients:
                    recipient_list.controls.append(
                        ft.ListTile(
                            title=ft.Text(recipient['name']),
                            subtitle=ft.Text(f"Need: {recipient['daily_need']} kg/day"),
                            data=recipient['_id'],
                        )
                    )
                recipient_register_status.value = f"Loaded {len(recipients)} recipients."
                recipient_register_status.color = ft.Colors.BLUE
            else:
                recipient_register_status.value = "Error fetching recipients."
                recipient_register_status.color = ft.Colors.RED
        except Exception as ex:
            recipient_register_status.value = f"API connection error: {ex}"
            recipient_register_status.color = ft.Colors.RED
            
        if e:
            page.update()

    # --- Event Handlers (Matching) (UPDATED) ---
    
    def run_match_click(e):
        match_run_status.value = "Running algorithm..."
        match_run_status.color = ft.Colors.BLUE
        match_list.controls.clear()
        page.client_storage.set("current_matches", []) # Clear old matches
        page.update()
        
        try:
            response = requests.post(f"{API_URL}/matches/run")
            
            if response.status_code == 200:
                matches = response.json()
                
                # --- NEW ---
                # Save matches for the logistics tab to use
                page.client_storage.set("current_matches", matches) 
                # --- END NEW ---

                match_run_status.value = f"Algorithm complete! Found {len(matches)} matches."
                match_run_status.color = ft.Colors.GREEN
                
                if not matches:
                    match_list.controls.append(ft.Text("No matches found."))
                
                for match in matches:
                    title = f"{match['food_name']} ({match['quantity_matched']} {match['unit']})"
                    subtitle = f"From: {match['donor_name']}  ->  To: {match['recipient_name']}"
                    match_list.controls.append(
                        ft.ListTile(
                            title=ft.Text(title),
                            subtitle=ft.Text(subtitle),
                            leading=ft.Icon(ft.Icons.ARROW_RIGHT_ALT)
                        )
                    )
            else:
                match_run_status.value = f"Error: {response.json().get('detail')}"
                match_run_status.color = ft.Colors.RED
                
        except Exception as ex:
            match_run_status.value = f"API connection error: {ex}"
            match_run_status.color = ft.Colors.RED
            
        page.update()

    # --- Event Handlers (Logistics) (NEW) ---
    
    def refresh_logistics_matches(e):
        """
        Loads the matches that were generated in the 'Matching' tab.
        """
        logistics_matches_list.controls.clear()
        logistics_status.value = "Loading proposed matches..."
        logistics_status.color = ft.Colors.BLUE
        
        matches = page.client_storage.get("current_matches")
        
        if not matches:
            logistics_matches_list.controls.append(ft.Text("No matches found. Run the algorithm on the 'Matching' tab first."))
            logistics_status.value = "No matches to show."
            page.update()
            return

        logistics_status.value = f"Loaded {len(matches)} proposed matches."
        
        for match in matches:
            title = f"{match['food_name']} ({match['quantity_matched']} {match['unit']})"
            subtitle = f"From: {match['donor_name']}  ->  To: {match['recipient_name']}"
            
            # We add a checkbox and store the raw match data
            logistics_matches_list.controls.append(
                ft.Checkbox(
                    label=f"{title}\n{subtitle}",
                    data=match # Store the full match dictionary
                )
            )
        page.update()

    def create_pickup_click(e):
        """
        Gathers all selected matches and sends them
        to the new /pickups endpoint.
        """
        logistics_status.value = "Creating pickup route..."
        logistics_status.color = ft.Colors.BLUE
        page.update()

        selected_matches = []
        for control in logistics_matches_list.controls:
            if isinstance(control, ft.Checkbox) and control.value:
                selected_matches.append(control.data) # Get the stored match dict

        if not selected_matches:
            logistics_status.value = "Error: Please select at least one match."
            logistics_status.color = ft.Colors.RED
            page.update()
            return

        try:
            # We send the list of match objects as the JSON body
            response = requests.post(f"{API_URL}/pickups", json=selected_matches)
            
            if response.status_code == 200:
                new_pickup = response.json()
                logistics_status.value = f"Success! Created pickup {new_pickup['_id']}"
                logistics_status.color = ft.Colors.GREEN
                
                # Clear the selected matches
                refresh_logistics_matches(None) 
                # Refresh the pending list
                refresh_pending_pickups(None)
            else:
                logistics_status.value = f"Error: {response.json().get('detail')}"
                logistics_status.color = ft.Colors.RED

        except Exception as ex:
            logistics_status.value = f"API connection error: {ex}"
            logistics_status.color = ft.Colors.RED
        
        page.update()

    def refresh_pending_pickups(e):
        """
        Gets all pickups from the /pickups endpoint.
        """
        logistics_pending_list.controls.clear()
        
        try:
            response = requests.get(f"{API_URL}/pickups")
            if response.status_code != 200:
                logistics_pending_list.append(ft.Text("Error fetching pickups."))
                page.update()
                return
            
            pickups = response.json()
            if not pickups:
                logistics_pending_list.append(ft.Text("No pending pickups."))

            for pickup in pickups:
                # We'll just show the status and ID for now
                logistics_pending_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(f"Pickup ID: {pickup['_id']}"),
                        subtitle=ft.Text(f"Status: {pickup['status']} | Stops: {len(pickup['stops'])}"),
                        leading=ft.Icon(ft.Icons.ROUTE)
                    )
                )
        except Exception as ex:
            logistics_pending_list.append(ft.Text(f"API Error: {ex}"))
        
        if e: # Only update the page if a user clicked
            page.update()

    # --- Page Layout (with Tabs) ---

    # --- Donor Tab Content ---
    donor_tab_content = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Register New Donor", size=24),
                    donor_name,
                    donor_address,
                    donor_phone,
                    ft.ElevatedButton("Register Donor", on_click=register_donor_click),
                    donor_register_status,
                    ft.Divider(),
                    ft.Text("All Donors", size=24),
                    ft.ElevatedButton("Refresh List", on_click=refresh_donor_list),
                    donor_list,
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            ),
            ft.VerticalDivider(),
            ft.Column(
                [
                    ft.Text("Add Food to Donor", size=24),
                    ft.Text("Selected Donor ID:"),
                    selected_donor_id,
                    ft.Divider(),
                    food_name,
                    ft.Row([food_qty, food_unit]),
                    ft.ElevatedButton("Add Food Item", on_click=add_food_click),
                    add_food_status
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            )
        ],
        expand=True
    )

    # --- Recipient Tab Content ---
    recipient_tab_content = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Register New Recipient", size=24),
                    recipient_name,
                    recipient_address,
                    recipient_phone,
                    recipient_need,
                    ft.ElevatedButton("Register Recipient", on_click=register_recipient_click),
                    recipient_register_status,
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            ),
            ft.VerticalDivider(),
            ft.Column(
                [
                    ft.Text("All Recipients", size=24),
                    ft.ElevatedButton("Refresh List", on_click=refresh_recipient_list),
                    recipient_list,
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            )
        ],
        expand=True
    )

    # --- Matching Tab Content ---
    match_tab_content = ft.Column(
        [
            ft.Text("Run Matchmaker", size=24),
            ft.Text("Click the button to run the algorithm based on all current donors, food, and recipients in the database."),
            ft.ElevatedButton("Run Matching Algorithm", on_click=run_match_click, icon=ft.Icons.PLAY_ARROW),
            match_run_status,
            ft.Divider(),
            ft.Text("Proposed Matches:", size=20),
            match_list,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )
    
    # --- Logistics Tab Content (NEW) ---
    logistics_tab_content = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("1. Proposed Matches", size=24),
                    ft.Text("Select matches to create a pickup route. (Run 'Matching' tab first)"),
                    ft.ElevatedButton("Refresh Match List", on_click=refresh_logistics_matches),
                    logistics_matches_list,
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            ),
            ft.VerticalDivider(),
            ft.Column(
                [
                    ft.Text("2. Create Route", size=24),
                    ft.ElevatedButton("Create Pickup Route from Selection", on_click=create_pickup_click, icon=ft.Icons.ADD_ROAD),
                    logistics_status,
                    ft.Divider(),
                    ft.Text("3. Pending Pickups", size=24),
                    ft.ElevatedButton("Refresh Pending List", on_click=refresh_pending_pickups),
                    logistics_pending_list,
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            )
        ],
        expand=True
    )

    # --- Main Page Setup (Tabs) ---
    page.add(
        ft.Tabs(
            [
                ft.Tab(
                    text="Donors & Food",
                    icon=ft.Icons.FASTFOOD,
                    content=donor_tab_content,
                ),
                ft.Tab(
                    text="Recipients",
                    icon=ft.Icons.PEOPLE,
                    content=recipient_tab_content,
                ),
                ft.Tab(
                    text="Matching",
                    icon=ft.Icons.HUB,
                    content=match_tab_content,
                ),
                # --- NEW TAB ---
                ft.Tab(
                    text="Logistics",
                    icon=ft.Icons.LOCAL_SHIPPING,
                    content=logistics_tab_content,
                ),
                # --- END NEW TAB ---
            ],
            expand=1,
            selected_index=0
        )
    )
    
    # Load initial data when app starts (UPDATED)
    def on_page_ready(e):
        refresh_donor_list(None)
        refresh_recipient_list(None)
        refresh_pending_pickups(None) # <-- Add this line
        page.update()

    page.on_ready = on_page_ready
    page.update()

# --- Run the App ---
if __name__ == "__main__":
    ft.app(target=main)