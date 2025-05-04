import csv
import random

baseUrl = "https://pokeapi.co/api/v2/pokemon/"

def url():
    name = get_name()
    url = build_url(name, baseUrl)
    return url

def get_name():
    with open("Pokemon.csv" ,mode="r", newline="") as file:
        content = csv.reader(file)
        next(content)
        name = [row[1] for row in content if row]
    return name

def build_url(name, baseURL):
    pokemon = random.choice(name)
    url = f"{baseURL}{pokemon}"
    return url
