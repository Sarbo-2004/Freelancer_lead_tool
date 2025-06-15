import httpx
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json
import os 

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_google_places(keyword: str):
    params = {
        "engine": "google_maps",
        "q": keyword,
        "type": "search",
        "api_key": SERPAPI_KEY
    }
    response = GoogleSearch(params)
    results = response.get_dict()

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
