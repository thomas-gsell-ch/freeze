import json

data = [
    {
        "warndate": "2026-10-01",
        "items": [
            {"_id": "sdfjksk2893sdfljlejlföe0", "ort": "Dachboden", "name": "Kichererbsen", "amount": "10 kg", "bestBefore": "15-10-2025"},
            {"_id": "sdfjksk2893sdfljlejlföe1", "ort": "Dachboden", "name": "Wein", "amount": "20 Stk", "bestBefore": "15-10-2025"},
            {"_id": "sdfjksk2893sdfljlejlföe2", "ort": "Keller", "name": "Bananen", "amount": "10 kg", "bestBefore": "15-10-2025"}
        ]
    },
    {
        "warndate": "2025-12-07",
        "items": [
            {"_id": "sdfjksk2893sdfljlejlföe3", "ort": "Küche", "name": "Yogurt", "amount": "3 Stk", "bestBefore": "21-12-2025"},
            {"_id": "sdfjksk2893sdfljlejlföe4", "ort": "Keller", "name": "Schweinssteaks", "amount": "4 Stk", "bestBefore": "21-12-2025"}
        ]
    }
]

def format_warning(data):
    result = []
    for warning in data:
        warndate = warning["warndate"]
        result.append(f"Das Ablauf-Warndatum vom {warndate} ist überschritten für:")
        for item in warning["items"]:
            result.append(f"{item['name']}, {item['ort']}, {item['amount']}, {item['bestBefore']}")
        result.append("")  # Leere Zeile für bessere Lesbarkeit
    return "\n".join(result)

formatted_text = format_warning(data)
print(formatted_text)