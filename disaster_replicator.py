import requests
import pandas as pd
from datetime import datetime

class DisasterDataReplicator:
    def __init__(self):
        self.nws_base_url = "https://api.weather.gov"
        self.fema_base_url = "https://www.fema.gov/api/open/v2"
        self.headers = {
            "User-Agent": "DisasterDataReplicator/1.0",
            "Content-Type": "application/json"
        }

    def fetch_nws_alerts(self, start_date=None, end_date=None, area=None):
        """
        Retrieve weather alerts from NWS API for the US.
        """
        url = f"{self.nws_base_url}/alerts/active"
        params = {}
        if area:
            params["area"] = area
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching NWS data: {response.status_code} - {response.text}")
                return {"features": []}
        except Exception as e:
            print(f"Exception fetching NWS data: {str(e)}")
            return {"features": []}

    def fetch_fema_disaster_data(self, start_date="1980-01-01", end_date="2024-12-31", state=None):
        """
        Retrieve historical disaster declarations from OpenFEMA API.
        """
        url = f"{self.fema_base_url}/DisasterDeclarationsSummaries"
        params = {
            "$filter": f"declarationDate ge '{start_date}T00:00:00.000Z' and declarationDate le '{end_date}T23:59:59.999Z'",
            "$inlinecount": "allpages",
            "$top": 1000,
            "$skip": 0
        }
        if state:
            params["$filter"] += f" and state eq '{state}'"

        all_data = []
        try:
            while True:
                response = requests.get(url, params=params, headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("DisasterDeclarationsSummaries", [])
                    all_data.extend(records)
                    if len(records) < 1000:  # Less than page size, no more data
                        break
                    params["$skip"] += 1000
                else:
                    print(f"Error fetching FEMA data: {response.status_code} - {response.text}")
                    break
        except Exception as e:
            print(f"Exception fetching FEMA data: {str(e)}")

        return all_data

    def calculate_economic_impact(self, nws_alerts, fema_disasters):
        """
        Process NWS alerts and FEMA disaster data to estimate significant events.
        """
        # Process FEMA disaster data
        fema_df = pd.DataFrame(fema_disasters)
        processed = []
        if not fema_df.empty:
            for _, event in fema_df.iterrows():
                # Fix: Use incidentType instead of disasterType
                disaster_type = event.get("incidentType", "Unknown")
                declaration_date = event.get("declarationDate", "Unknown")
                state = event.get("state", "Unknown")
                estimated_loss = self.estimate_loss(disaster_type)
                processed.append({
                    "date": declaration_date,
                    "type": disaster_type,
                    "estimated_loss": estimated_loss,
                    "location": state,
                    "source": "FEMA",
                    "disaster_number": event.get("disasterNumber", "N/A")
                })

        # Process NWS alerts
        alerts = nws_alerts.get("features", [])
        for alert in alerts:
            properties = alert.get("properties", {})
            event_type = properties.get("event", "Unknown")
            # Filter for severe events
            if any(severe in event_type.lower() for severe in ["hurricane", "tornado", "flood", "blizzard"]):
                headline = properties.get("headline", "No headline")
                area_desc = properties.get("areaDesc", "Unknown")
                effective_date = properties.get("effective", "Unknown")
                estimated_loss = self.estimate_loss(event_type)
                processed.append({
                    "date": effective_date,
                    "type": event_type,
                    "estimated_loss": estimated_loss,
                    "location": area_desc,
                    "source": "NWS",
                    "disaster_number": "N/A",
                    "headline": headline
                })

        return pd.DataFrame(processed)

    def estimate_loss(self, event_type):
        """
        Placeholder for economic impact calculation based on event type.
        """
        if not event_type:
            return 100000000  # Default for unknown events
            
        event_type = str(event_type).lower()
        if "hurricane" in event_type or "tropical storm" in event_type:
            return 1000000000
        elif "tornado" in event_type or "flood" in event_type:
            return 500000000
        elif "blizzard" in event_type or "winter storm" in event_type:
            return 250000000
        else:
            return 100000000

    def save_data(self, dataset, filename="us_disaster_database.csv"):
        """Save the processed dataset to a file."""
        dataset.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# Test with a small sample
replicator = DisasterDataReplicator()

# Fetch limited data for testing
nws_alerts = replicator.fetch_nws_alerts()
fema_disasters = replicator.fetch_fema_disaster_data(start_date="2023-01-01", end_date="2023-12-31")

# Process data
print(f"NWS alerts: {len(nws_alerts.get('features', []))}")
print(f"FEMA disasters: {len(fema_disasters)}")

# Process a small sample for testing
full_dataset = replicator.calculate_economic_impact(nws_alerts, fema_disasters)
print(f"Total events processed: {len(full_dataset)}")
print("\nSample of processed data:")
print(full_dataset.head())

# Save to both CSV and Excel
full_dataset.to_csv("us_disaster_database.csv", index=False)
full_dataset.to_excel("us_disaster_database.xlsx", index=False)

print("\nData saved to us_disaster_database.csv and us_disaster_database.xlsx")
