from bson import ObjectId

def convert_objectid_to_string(data):
    """
    Konvertiert ObjectId-Werte in einem Dictionary in Strings und setzt sie zurück ins Dictionary.
    
    :param data: Dictionary, das ein ObjectId-Objekt enthält.
    :return: Dictionary mit ObjectId-Werten als Strings.
    """
    for key, value in data.items():
        if isinstance(value, ObjectId):
            # Konvertiere ObjectId zu String
            data[key] = str(value)
    return data

def main():
    # Beispiel-Dictionary mit einem ObjectId
    data = {
        "id": ObjectId("64bfe77d14d2a1e2d5e58baf"),
        "name": "Apfel",
        "category": "Obst"
    }
    
    print("Original Dictionary:")
    print(data)
    
    # Konvertiere ObjectId zu String
    updated_data = convert_objectid_to_string(data)
    
    print("\nUpdated Dictionary:")
    print(updated_data)

if __name__ == "__main__":
    main()