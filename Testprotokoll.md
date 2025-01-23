# Testprotokoll

**Offline-Funktion:**

1. Liste mit den Produkten anzeigen lassen.
2. Offline gehen: Im Browser Inspect Tools - Network auf offline klicken.
3. Auf die Liste mit den Produkten gehen => Sie muss immer noch ersichtlich sein. Zusammen mit den Details.

**Produkt anlegen:**

1. Ein Produkt angelegt und hernach speichern.
2. Zurück in den Katalog wechseln.
3. Das Produkt in der Liste anwählen => Das neue Produkt ist ersichtlich, zusammen mit den Details.

**Produkt bearbeiten:**

1. Aus der Liste mit den Produkten eins auswählen.
2. Auf der Detaillisten den Bearbeiten-Button drücken => Die einzelnen Felder werden veränderbar.
3. Einzelne Felder bearbeiten.
4. Den Speichern-Button drücken.
5. Zurück auf die Produkt-Liste wechseln und Ctrl+Shift+F5 drücken.
6. Das geänderte Produkt aufgerufen => Die Änderungen wurden übernommen.

**PushNotification werden gesendet:**

1. In den Browser-Optionen und Benachrichtigungen allfällige PushNotifications löschen.
2. Die Anwendung anwählen mit localhost:8080 => Aufforderung PushNotifications zu erlauben erscheint.
3. PushNotification erlauben.
4. Ein Produkt anwählen.
5. Auf Bearbeiten klicken und das Ablaufdatum so setzen das es in drei Tagen erreicht wird => Jede Minute muss eine Push-Nachricht kommen.
   (Der Intervall muss im Code des PushNotification-Service gesetzt werden. Auf 1 Stunde.)

**PushNotification-Service ist bearbeitbar:**

Voraussetzung: Der Container mit der RabbitMQ muss laufen und PushNotifications müssen zugelassen worden sein.

1. Auf dem Docker-Desktop den Container mit dem PushNotification-Service(bestreachedpnservice) stoppen.
2. Auf der Liste mit den Produkten ein neues Produkt erstellen.
3. Das Ablaufdatum so setzen, dass es in drei Tagen erreicht wird und speichern. => Es kommen keine PushNotifications. Die Events werden in der RabbitMQ gestaut.
4. Im Docker-Desktop den Container mit dem PushNotifications wieder starten. => Es kommen nun PushNotifications.

**PushNotification-Service läuft autonom:**

Voraussetzung: PushNotifications erscheinen.

1. Im Docker-Desktop den Container mit dem ProduktProvider-Service(productproviderservice) ausschalten => Die PushNotifications kommen trotzdem noch.

**Produkt entnehmen:**

Voraussetzung: Ein Produkt ist gespeichert und es erscheinen PushNotifications.

1. Die Liste mit den Produkten aufrufen.
2. Auf dem betreffenden Produkt den Löschen Button anklicken => Das Produkt wird nicht mehr angezeigt und es kommen keine PushNotifications mehr.
