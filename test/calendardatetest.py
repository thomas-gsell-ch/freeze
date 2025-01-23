from datetime import datetime, timedelta

# 1. Ausgangsdatum als String
date_str = "01-05-2025"
print("bestBefore Datum: ", date_str)

# 2. String in ein Datumsobjekt umwandeln
date_format = "%d-%m-%Y"
date_obj = datetime.strptime(date_str, date_format)

# 3. "Warndatum" berechnen (eine Woche früher)
warning_date_obj = date_obj - timedelta(weeks=1)

# 4. "Warndatum" als String ausgeben
warning_date_str = warning_date_obj.strftime(date_format)
print("Warndatum:", warning_date_str)

# 5. Aktuelles Datum als String ausgeben
current_date_obj = datetime.now()
current_date_str = current_date_obj.strftime(date_format)
print("Aktuelles Datum:", current_date_str)

# 6. Prüfen, ob das aktuelle Datum älter als das "Warndatum" ist
is_current_date_older = current_date_obj >= warning_date_obj
print("Ist das aktuelle Datum älter als das Warndatum?", is_current_date_older)