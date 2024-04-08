import requests

url = "http://localhost:8000/personajes"
headers = {'Content-type': 'application/json'}

# POST /characters 
print("\n Personaje Nuevo")
mi_personaje = {
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma" : 15,
    "strength": 10,
    "dexterity" : 10
}
response = requests.post(url, json=mi_personaje, headers=headers)
print(response.json())

mi_personaje = {
    "name": "Aragorn",
    "level": 10,
    "role": "Warrior",
    "charisma": 10,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=mi_personaje, headers=headers)

mi_personaje = {
    "name": "Robin",
    "level": 5,
    "role": "Archer",
    "charisma": 10,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=mi_personaje, headers=headers)
print("\n Lista de personajes")
# GET /characters
response = requests.get(url)
print(response.json())

# GET /characters/?role=Archer&level=5&charisma=10
print("\n Búsqueda")



# PUT /characters/2
print("\n update")
update_data = {
    "charisma": 20,
    "strength": 15,
    "dexterity": 15
}
response = requests.put(url + "/2", json=update_data, headers=headers)
print(response.json())

# DELETE /characters/3
print("\n Eliminacion ")
response = requests.delete(url + "/3")
print(response.json())

print("\n Personaje Nuevo")
# POST /characters
mi_personaje_nuevo = {
    "name": "Legolas",
    "level": 5,
    "role": "Archer",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=mi_personaje_nuevo, headers=headers)
print(response.json())

# GET /characters
print("\n LISTA ULTIMA PERSONAJES")
response = requests.get(url)
print(response.json())
