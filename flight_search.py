import requests
import random
from datetime import datetime, timedelta

# 🔐 Amadeus API credentials
API_KEY = "LY9Xij5iQ0SHbImW5hQlLluMHxzoaLgJ"
API_SECRET = "e3Ue4xUt6BwqitZ0"
BASE_URL = "https://test.api.amadeus.com"

# 📅 Generate departure/return dates
departure_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
trip_length = random.randint(7, 10)
return_date = (datetime.today() + timedelta(days=1 + trip_length)).strftime("%Y-%m-%d")

# 🔑 Get access token
def get_token():
    token_url = f"{BASE_URL}/v1/security/oauth2/token"
    res = requests.post(
        token_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": API_SECRET
        }
    )
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        print("❌ Failed to get token:", res.status_code)
        print(res.text)
        return None

# ✈️ Find roundtrip flights from ATL to multiple destinations
def find_flights(token):
    url = f"{BASE_URL}/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    destinations = ["LON", "CDG", "AMS", "BCN"]  # London, Paris, Amsterdam, Barcelona

    for destination in destinations:
        print(f"\n🔎 Searching ATL → {destination} ({departure_date} to {return_date})")

        params = {
            "originLocationCode": "ATL",
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "max": 5,
            "currencyCode": "USD"
        }

        res = requests.get(url, headers=headers, params=params)

        if res.status_code == 200:
            data = res.json()
            for offer in data.get("data", []):
                itineraries = offer["itineraries"]
                price = offer["price"]["total"]

                for direction, itinerary in zip(["Outbound", "Return"], itineraries):
                    segments = itinerary["segments"]
                    dep_code = segments[0]["departure"]["iataCode"]
                    dep_time = segments[0]["departure"]["at"]
                    arr_code = segments[-1]["arrival"]["iataCode"]
                    arr_time = segments[-1]["arrival"]["at"]
                    airlines = set(segment["carrierCode"] for segment in segments)
                    airline_list = ", ".join(airlines)

                    print(f"📍 {direction}: {dep_code} ➡️ {arr_code}")
                    print(f"   🕓 Depart: {dep_time}")
                    print(f"   🛬 Arrive: {arr_time}")
                    print(f"   🛫 Airline(s): {airline_list}")
                print(f"💵 Total Price: ${price}")
                print("-" * 60)
        else:
            print(f"❌ Error searching for {destination}: {res.status_code}")
            print(res.text)

# 🚀 Run the script
if __name__ == "__main__":
    token = get_token()
    if token:
        find_flights(token)


