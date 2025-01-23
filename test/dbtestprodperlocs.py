from pymongo import MongoClient
from pprint import pprint

# Verbindung zur MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")  # Passe die Verbindung an, falls nötig
db = client["myDatabase"]  # Datenbankname
collection = db["inventory"]  # Sammlungsname

def main():
    # Datensatz für den Dachboden
    test_data = {
        "ort": "Dachboden",
        "items": [
            {"name": "Kichererbsen", "amount": "10 kg", "warndate": "2026-02-06"},
            {"name": "Wein", "amount": "20 Stk", "warndate": "2030-10-01"}
        ]
    }

    print("\n--- Lösche vorhandenen Datensatz ---")
    # Datensatz löschen
    result = collection.delete_one({"ort": "Dachboden"})
    print(f"Gelöschte Dokumente: {result.deleted_count}")

    print("\n--- Füge neuen Datensatz hinzu ---")
    # Datensatz neu erzeugen
    result = collection.insert_one(test_data)
    print(f"Neu hinzugefügtes Dokument mit ID: {result.inserted_id}")

    print("\n--- Suche nach dem Datensatz ---")
    # Suche nach dem Datensatz
    found_doc = collection.find_one({"ort": "Dachboden"})
    print("Gefundener Datensatz:")
    pprint(found_doc)

    print("\n--- Ändere den Datensatz ---")
    # Datensatz ändern (z. B. Menge von "Wein" auf 30 Stk setzen)
    updated_items = [
        {"name": "Kichererbsen", "amount": "10 kg", "warndate": "2026-02-06"},
        {"name": "Wein", "amount": "30 Stk", "warndate": "2030-10-01"}
    ]
    collection.update_one(
        {"ort": "Dachboden"},
        {"$set": {"items": updated_items}}
    )

    print("\n--- Suche nach aktualisiertem Datensatz ---")
    # Aktualisierten Datensatz suchen
    updated_doc = collection.find_one({"ort": "Dachboden"})
    print("Aktualisierter Datensatz:")
    pprint(updated_doc)

if __name__ == "__main__":
    main()