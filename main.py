import requests
import uvicorn
from get_name import url
from hint import gen_hint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    print("Hello from pokemon!")
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get(path="/")
async def root():
    poke_url = url()
    poke_hint = gen_hint()
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
        "Hint" : poke_hint.lower(),
        "id" : id,
    })

    return data
            
if __name__ == "__main__":
    main()