import requests
from datetime import datetime, timedelta

# Replace with your Amadeus API key/secret
API_KEY = "LY9Xij5iQ0SHbImW5hQlLluMHxzoaLgJ"
API_SECRET = "e3Ue4xUt6BwqitZ0"
BASE_URL = "https://test.api.amadeus.com"

departure_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

# Step 1: Get access token
def get_token():
    token_url = f"{BASE_URL}/v1/security/oauth2/token"
    res = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": API_SECRET
        }
    )
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        print("Failed to get token:", res.status_code)
        print(res.text)
        return None


def find_flights(token):
    url = f"{BASE_URL}/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    
    destinations = ["LON", "CDG", "AMS", "BCN"]  # London, Paris, Amsterdam, Barcelona

    for destination in destinations:
        print(f"\n🔎 Searching ATL → {destination}")
        
        params = {
            "originLocationCode": "ATL",
            "destinationLocationCode": destination,
            "departureDate": "2025-03-29",
            "adults": 1,
            "max": 5,
            "currencyCode": "USD"
        }

        res = requests.get(url, headers=headers, params=params)

        if res.status_code == 200:
            data = res.json()
            for offer in data.get("data", []):
                itinerary = offer["itineraries"][0]
                segments = itinerary["segments"]
                
                dep = segments[0]["departure"]["iataCode"]
                arr = segments[-1]["arrival"]["iataCode"]
                price = offer["price"]["total"]

                # Collect airline codes
                airlines = set(segment["carrierCode"] for segment in segments)
                airline_list = ", ".join(airlines)

                print(f"✈️ {dep} ➡️ {arr} for ${price}")
                print(f"🛫 Airline(s): {airline_list}")
                print("-" * 40)
        else:
            print(f"❌ Error searching for {destination}: {res.status_code}")
            print(res.text)



    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        data = res.json()
        for offer in data["data"]:
            dep = offer["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            arr = offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
            price = offer["price"]["total"]
            print(f"✈️ {dep} ➡️ {arr} for ${price}")
    else:
        print("Flight search failed:", res.status_code)
        print(res.text)


if __name__ == "__main__":
    token = get_token()
    find_flights(token)

