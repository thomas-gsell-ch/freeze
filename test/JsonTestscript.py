import json



def create_json(topic, command, data):
    """Erstellt die JSON-Struktur aus einzelnen Strings und Datensätzen."""
    # JSON-Daten aus den übergebenen Parametern zusammensetzen
    print(f'The type of data is: {type(data)}')
    
    json_data = {
        "topic": topic,
        "command": command,
        "data": data
    }
    # JSON-String aus Python-Datenstruktur erstellen
    json_string = json.dumps(json_data, indent=4)
    return json_string

def main():
    # Einzelne Strings und Datensätze definieren
    topic = "Product"
    command = "CREATE"
    data = {
        "Id": "24-digit",
        "name": "Apfel",
        "category": "Obst",
        "amount": "1kg",
        "location": "Keller",
        "freezingDate": "05-07-2024",
        "bestBefore": "01-05-2025"
    }
    
    # JSON-String aus den Einzelteilen erstellen
    json_string = create_json(topic, command, data)
    
    # JSON-String ausgeben
    print("Erstellter JSON-String:")
    print(json_string)

if __name__ == "__main__":
    main()






# Beispiel-JSON-Struktur als String
#json_string = '''
#{
#    "topic": "Product",
#    "command": "CREATE",
#    "data": {
#        "Id": "24-digit",
#        "name": "Apfel",
#        "category": "Obst",
#        "amount": "1kg",
#        "location": "Keller",
#        "freezingDate": "05-07-2024",
#        "bestBefore": "01-05-2025"
#    }
#}
#'''

def extract_topic_and_command(json_obj):
    """Extrahiert das Topic und das Command aus dem JSON."""
    topic = json_obj.get("topic", None)
    command = json_obj.get("command", None)
    return topic, command

def extract_data(json_obj):
    """Extrahiert die 'data'-Datenstruktur aus dem JSON."""
    data = json_obj.get("data", {})
    return data

def main():
    # Parsen der JSON-Struktur
    parsed_json = json.loads(json_string)
    
    # Extrahieren von Topic und Command
    topic, command = extract_topic_and_command(parsed_json)
    print(f"Topic: {topic}, Command: {command}")
    
    # Extrahieren der Datenstruktur
    data = extract_data(parsed_json)
    print("Data Structure:")
    for key, value in data.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()