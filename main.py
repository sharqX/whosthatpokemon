import requests
import uvicorn
from get_name import url
from hint import gen_hint
from fastapi import FastAPI

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
        "Type" : type,
        "Height" : height,
        "Weight" : weight,
        "Hint" : poke_hint,
        "id" : id,
    })

    return data
            
if __name__ == "__main__":
    main()
