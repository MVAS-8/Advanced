import json
import xml.etree.ElementTree as ET
import csv

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_xml(filename):
    root = ET.Element("користувачі")
    user = ET.SubElement(root, "користувач")
    ET.SubElement(user, "ім'я").text = "Михайло"
    ET.SubElement(user, "вік").text = "30"
    ET.SubElement(user, "місто").text = "Київ"
    
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

def search_in_xml(filename, query):
    tree = ET.parse(filename)
    root = tree.getroot()
    return [elem.text for elem in root.findall(query)]

def register_csv_dialect():
    csv.register_dialect("custom_dialect", delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

def save_to_csv(data, filename, mode='w'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, dialect="custom_dialect")
        if mode == 'w':
            writer.writerow(["Ім'я", "Прізвище", "Дата народження", "Місто"])
        writer.writerow(data)

def load_from_csv(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, dialect="custom_dialect")
        next(reader)
        return list(reader)

def csv_to_json(csv_filename, json_filename):
    data = load_from_csv(csv_filename)
    keys = ["Ім'я", "Прізвище", "Дата народження", "Місто"]
    json_data = [dict(zip(keys, row)) for row in data]
    save_to_json(json_data, json_filename)

def csv_to_xml(csv_filename, xml_filename):
    data = load_from_csv(csv_filename)
    root = ET.Element("користувачі")
    for row in data:
        user = ET.SubElement(root, "користувач")
        ET.SubElement(user, "ім'я").text = row[0]
        ET.SubElement(user, "прізвище").text = row[1]
        ET.SubElement(user, "дата_народження").text = row[2]
        ET.SubElement(user, "місто").text = row[3]
    tree = ET.ElementTree(root)
    tree.write(xml_filename, encoding="utf-8", xml_declaration=True)

register_csv_dialect()
csv_filename = "users.csv"
json_filename = "users.json"
xml_filename = "users.xml"

while True:
    user_data = input("Введіть дані (Ім'я, Прізвище, Дата народження, Місто) або 'stop' для завершення: ")
    if user_data.lower() == 'stop':
        break
    save_to_csv(user_data.split(','), csv_filename, mode='a')

csv_to_json(csv_filename, json_filename)
csv_to_xml(csv_filename, xml_filename)

print("Дані збережено у CSV, JSON та XML файлах.")
