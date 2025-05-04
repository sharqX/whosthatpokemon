import requests
from get_name import url
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

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
    return hint

def gen_hint():
    poke_hint = hint()
    print(poke_hint)
    template = """
    Change the hint below and generate a new hint if it contains a Pokemon name else just pass the original hint to "New hint:".

    Instruction: {instruction} 
    Here is the hint: {hint}

    New hint: 
    """

    model = OllamaLLM(model="llama3")
    promt = ChatPromptTemplate.from_template(template)
    chain = promt | model

    ai_generated_hint = chain.invoke({
    "instruction":
    "Write the hint in 3rd person if it contains a pokemon do not use pronous such as he/she",
    "hint":
    {poke_hint}
    })
    print(ai_generated_hint)


gen_hint()