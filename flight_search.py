import requests
import os
import random
from datetime import datetime, timedelta

# 🔐 Amadeus Test API credentials (use environment variables or replace here)
API_KEY = os.getenv("AMADEUS_API_KEY", "LY9Xij5iQ0SHbImW5hQlLluMHxzoaLgJ
API_SECRET = os.getenv("AMADEUS_API_SECRET", "e3Ue4xUt6BwqitZ0")
BASE_URL = "https://test.api.amadeus.com"

# Destination airport codes
DESTINATIONS = ["DEN", "LON", "NYC"]
PRICE_CAP = 750

# Generate date ranges
def generate_date_pairs():
    today = datetime.today()
    date_pairs = []
    for days_out in range(30, 61):
        dep = today + timedelta(days=days_out)
        trip_length = random.randint(7, 10)
        ret = dep + timedelta(days=trip_length)
        date_pairs.append((dep.strftime("%Y-%m-%d"), ret.strftime("%Y-%m-%d")))
    return date_pairs

# Get Amadeus access token
def get_token():
    res = requests.post(
        f"{BASE_URL}/v1/security/oauth2/token",
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

# Search for cheap roundtrip flights
def find_cheap_flights(token):
    url = f"{BASE_URL}/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    date_pairs = generate_date_pairs()

    for destination in DESTINATIONS:
        print(f"\n🌍 Searching ATL → {destination}")
        for dep_date, ret_date in date_pairs:
            params = {
                "originLocationCode": "ATL",
                "destinationLocationCode": destination,
                "departureDate": dep_date,
                "returnDate": ret_date,
                "adults": 1,
                "max": 5,
                "currencyCode": "USD"
            }

            res = requests.get(url, headers=headers, params=params)

            if res.status_code == 200:
                offers = res.json().get("data", [])
                for offer in offers:
                    price = float(offer["price"]["total"])
                    if price <= PRICE_CAP:
                        outbound = offer["itineraries"][0]["segments"]
                        inbound = offer["itineraries"][1]["segments"]
                        out_dep = outbound[0]["departure"]["at"]
                        out_arr = outbound[-1]["arrival"]["at"]
                        in_dep = inbound[0]["departure"]["at"]
                        in_arr = inbound[-1]["arrival"]["at"]
                        airlines = set(seg["carrierCode"] for seg in outbound + inbound)

                        print(f"🛫 {dep_date} ➡️ {ret_date}")
                        print(f"   Outbound: {out_dep} ➡️ {out_arr}")
                        print(f"   Return:   {in_dep} ➡️ {in_arr}")
                        print(f"   Airline(s): {', '.join(airlines)}")
                        print(f"💵 Total Price: ${price}")
                        print("-" * 50)
            else:
                print(f"❌ Error for {destination} on {dep_date}: {res.status_code}")

# Main
if __name__ == "__main__":
    token = get_token()
    if token:
        find_cheap_flights(token)



