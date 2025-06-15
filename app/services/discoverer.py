import httpx
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json
import os 

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
CACHE_FILE = "response.json"
def search_google_places(keyword: str,use_cache=True):
    if use_cache and os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cached_data = json.load(f)
            print("📁 Using cached results...")
            return cached_data
    params = {
        "engine": "google_maps",
        "q": keyword,
        "type": "search",
        "api_key": SERPAPI_KEY
    }
    response = GoogleSearch(params)
    results = response.get_dict()
    # with httpx.Client() as client:
    #     response = client.get(url, params=params)
    #     print("Status:", response.status_code)
    #     data = response.json()
    #     print("Raw data:", data)

    #     results = []
    #    
    res1=[]
    for place in results.get("local_results", []):
            res1.append({
                "name": place.get("title"),
                "address": place.get("address"),
                "phone": place.get("phone"),
                "email": place.get("email","Not available"),
                "website": place.get("website"),
                "category": place.get("type")
            })
    return res1
