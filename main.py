#Завдання 1
import json

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

data = {
    "ім'я": "Михайло",
    "вік": 30,
    "місто": "Київ"
}

filename = "data.json"
save_to_json(data, filename)

loaded_data = load_from_json(filename)
print("Завантажені дані:", loaded_data)
