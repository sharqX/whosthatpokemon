import re
import requests
from get_name import url
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def get_id():
    response = requests.get(url())
    pokemon =  response.json()

    if pokemon and "id" in pokemon:
        id = pokemon["id"]
        assert 1 <= id <= 1025, "Error: id is out of valid range!"
        return id
    else:
        raise ValueError("Error getting id: pokemon data is invalid or missing")


def hint():
    id = get_id()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}/")
    if response.status_code != 200:
        return f"Failed to fetch data for ID"
    
    data = response.json()
    for entry in data["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            hint = entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
    return hint

def gen_hint():
    poke_hint = hint()
    template = """
    Change the hint below and generate a new hint if it contains a Pokémon name else just pass the original hint to "New hint:".

    Instruction: {instruction} 
    Here is the hint: {hint}

    New hint: 
    """

    model = OllamaLLM(model="llama3") # Gotta cache responds mannn !!! AI toooooooo SLOW 
    promt = ChatPromptTemplate.from_template(template)
    chain = promt | model

    ai_generated_hint = chain.invoke({
    "instruction":
    "Write the hint in 3rd person if it contains a pokemon DO NOT use pronous such as he/she",
    "hint":
    {poke_hint}
    })

    match = re.search(r"New hint:\s*((?:.|\n)*?)(?:\n\s*\n|$)", ai_generated_hint)
    if match:
        hint_block = match.group(1)

        cleaned = re.sub(r'[\"“”\'`{}]', '', hint_block)

        return cleaned.strip()
    else:
        return "No hint found :("