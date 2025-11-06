import requests
import matplotlib.pyplot as plt
from collections import defaultdict

# The URL of your live FastAPI server
API_URL = "http://127.0.0.1:8000"

def fetch_all_data():
    """Fetches all donors, recipients, and match results from the API."""
    try:
        donors_res = requests.get(f"{API_URL}/donors")
        recipients_res = requests.get(f"{API_URL}/recipients")
        matches_res = requests.post(f"{API_URL}/matches/run")
        
        donors_res.raise_for_status()
        recipients_res.raise_for_status()
        matches_res.raise_for_status()
        
        print("Successfully fetched all data from API.")
        return donors_res.json(), recipients_res.json(), matches_res.json()
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not connect to API at {API_URL}.")
        print("Please make sure your Uvicorn server is running.")
        print(f"Details: {e}")
        return None, None, None

def plot_donor_participation(donors, ax):
    """Creates a bar chart of food items donated by each donor."""
    if not donors:
        ax.set_title("Donor Participation")
        ax.text(0.5, 0.5, "No donor data", ha='center')
        return

    names = [donor['name'] for donor in donors]
    # Count the number of *distinct* food items each donor has
    food_counts = [len(donor['current_donations']) for donor in donors]
    
    colors = plt.cm.viridis([0.2, 0.5, 0.8])
    
    ax.bar(names, food_counts, color=colors)
    ax.set_title("Donor Participation")
    ax.set_ylabel("Number of Active Food Donations")
    ax.set_xlabel("Donor")

def plot_recipient_needs(recipients, ax):
    """Creates a pie chart of the daily needs of all recipients."""
    if not recipients:
        ax.set_title("Recipient Needs")
        ax.text(0.5, 0.5, "No recipient data", ha='center')
        return

    names = [r['name'] for r in recipients]
    needs = [r['daily_need'] for r in recipients]
    
    ax.pie(needs, labels=names, autopct='%1.1f%%', startangle=90)
    ax.set_title("Share of Total Daily Need")
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

def plot_match_summary(matches, ax):
    """Creates a bar chart of the total quantity matched to each recipient."""
    if not matches:
        ax.set_title("Match Summary")
        ax.text(0.5, 0.5, "No match data", ha='center')
        return

    # Aggregate total quantity matched per recipient
    recipient_totals = defaultdict(float)
    for match in matches:
        recipient_totals[match['recipient_name']] += match['quantity_matched']

    names = list(recipient_totals.keys())
    quantities = list(recipient_totals.values())
    
    colors = plt.cm.plasma([0.3, 0.6, 0.9])
    
    ax.bar(names, quantities, color=colors)
    ax.set_title("Total Food Matched (by Recipient)")
    ax.set_ylabel("Total Quantity Matched (e.g., kg)")
    ax.set_xlabel("Recipient")

def main():
    """Main function to fetch data and plot all charts."""
    donors, recipients, matches = fetch_all_data()
    
    if donors is None:
        return # API connection failed

    # Create a figure with 3 subplots (1 row, 3 columns)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
    
    plot_donor_participation(donors, ax1)
    plot_recipient_needs(recipients, ax2)
    plot_match_summary(matches, ax3)
    
    fig.suptitle("Food Rescue Analytics Dashboard", fontsize=20)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()