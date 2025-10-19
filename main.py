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
    try:
        requests.get("http://localhost:11434").status_code == 200
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"Ollama service is not running: {e}")


@app.get(path="/")
async def root():
    poke_url = url()
    response = requests.get(poke_url)
    if response.status_code != 200:
        return "API Error"

    pokemon = response.json()
    data = []

    if pokemon:
        type = pokemon["types"][0]["type"]["name"]
        height = pokemon["height"]
        weight = pokemon["weight"]
        id = pokemon["id"]
        name = pokemon["forms"][0]["name"]

    data.append(
        {
            "Type": type,
            "Height": height,
            "Weight": weight,
            "id": id,
            "name": name,
        }
    )

    return data


@app.get(path="/hint")
async def get_hint():
    poke_hint = gen_hint()
    return {"Hint": poke_hint.lower()}


if __name__ == "__main__":
    main()
