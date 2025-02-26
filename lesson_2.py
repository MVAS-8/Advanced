import json
import xml.etree.ElementTree as ET

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

xml_filename = "data.xml"
create_xml(xml_filename)

query = "./користувач/ім'я"
result = search_in_xml(xml_filename, query)
print("Результат пошуку:", result)