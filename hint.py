import requests
from get_name import url

def get_id():
    response = requests.get(url())
    pokemon =  response.json()

    if pokemon:
        id = pokemon["id"]
        return id
    else:
        assert id != range(1,1025), "Error getting id!"

def hint():
    id = get_id()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}/")
    if response.status_code != 200:
        return f"Failed to fetch data for ID"
    
    data = response.json()
    for entry in data["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            hint = entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
    return f"Hint: {hint}"