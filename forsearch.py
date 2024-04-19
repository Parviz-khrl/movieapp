import requests

def searchreq(searchquery, year=None, type=None, genre=None):
    params = {
        "apikey": 'ff72dc2b',
        "s": searchquery,
        "type": type,
        "y": year,
        "r": "json"
    }
    url = "http://www.omdbapi.com/"
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract genre information for each result
    for item in data.get("Search", []):
        imdb_id = item.get("imdbID")
        if imdb_id:
            # Fetch additional details using ID
            details_response = requests.get(url, params={"apikey": 'ff72dc2b', "i": imdb_id, "r": "json"})
            details_data = details_response.json()
            item["Genre"] = details_data.get("Genre", "N/A")
    
    return data