import requests
import uvicorn
from fastapi import FastAPI
from get_name import url
from hint import gen_hint

app = FastAPI()
poke_url = url()
poke_hint = gen_hint()

def main():
    print("Hello from pokemon!")
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get(path="/")
async def root():
    response = requests.get(poke_url)
    if response.status_code != 200:
        return "API Error"
    
    pokemon =  response.json()
    data = []

    if pokemon:
        type = pokemon["types"][0]["type"]["name"]
        height = pokemon["height"]
        weight = pokemon["weight"]
        id = pokemon["id"]
    
    data.append({
        "type" : type,
        "height" : height,
        "weight" : weight,
        "id" : id,
        "hint" : poke_hint 
    })

    return data
            
if __name__ == "__main__":
    main()


# type
# height & weight
# ability
# id for poekedex flavor