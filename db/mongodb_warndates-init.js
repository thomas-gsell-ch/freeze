const database = 'warndatesdb';
const collection_warndates = 'warndates';
const collection_subscriptions = 'subscriptions';

// Create a new database.
use(database);

// Create a new collection.
db.createCollection(collection_warndates);
db.createCollection(collection_subscriptions);

// Datensätze nach `warndate` gruppieren und einfügen
db.warndates.insertMany([
  {
    warndate: "2026-10-01",
    items: [
      { _id: "sdfjksk2893sdfljlejlföe0", ort: "Dachboden", name: "Kichererbsen", amount: "10 kg", bestBefore:"15-10-2025"},
      { _id: "sdfjksk2893sdfljlejlföe1", ort: "Dachboden", name: "Wein", amount: "20 Stk", bestBefore:"15-10-2025" },
      { _id: "sdfjksk2893sdfljlejlföe2", ort: "Keller", name: "Bananen", amount: "10 kg", bestBefore:"15-10-2025" }
    ]
  },
  {
    warndate: "2025-12-07",
    items: [
      { _id: "sdfjksk2893sdfljlejlföe3", ort: "Küche", name: "Yogurt", amount: "3 Stk", bestBefore:"21-12-2025" },
      { _id: "sdfjksk2893sdfljlejlföe4", ort: "Keller", name: "Schweinssteaks", amount: "4 Stk", bestBefore:"21-12-2025" }
    ]
  }
]);

db.subscriptions.insertMany([
  {
    "endpoint": "https://fcm.googleapis.com/fcm/send/e8KaETkV-GA:APA91bHzu4z6BoQIiaenAVTSL-NNAyU-9OclB5o81pPx54MmhDmHKgk-F0Cr37evPTgg-xYJomduoH9npii8_WBZHI7KssbAmJWz8Se14ZWl5DQ4VsYTeOa6_FnFyN6uQjg1XtI7TAdf",
    "expirationTime": "None",
    "keys": {
        "p256dh": "BI1RCOjvqfRQzbRJNzMPcX5oALXg4kN_bqxceIydAqgzi92KHA79JcYBzhJHcIM3srInmFTM7D_LzlnaI-vWC9Q",
        "auth": "oDcDHYsaBebQIP2RXAOgGQ"
    }
  },
  {
    "endpoint": "https://fcm.googleapis.com/fcm/send/e8KaETkV-GA:APA91bHzu4z6BoQIiaenAVTSL-NNAyU-9OclB5o81pPx54MmhDmHKgk-F0Cr37evPTgg-xYJomduoH9npii8_WBZHI7KssbAmJWz8Se14ZWl5DQ4VsYTeOa6_FnFyN6uQjg1XtI7TAdf",
    "expirationTime": "None",
    "keys": {
        "p256dh": "BI1RCOjvqfRQzbRJNzMPcX5oALXg4kN_bqxceIydAqgzi92KHA79JcYBzhJHcIM3srInmFTM7D_LzlnaI-vWC9Q",
        "auth": "oDcDHYsaBebQIP2RXAOgGQ"
    }
  }
]);




//print("Database initialized with grouped inventory data!");


db.createUser(
    {
        user: "dbuser", // user for database which shall be created
        pwd: "hellouser",
        roles: [
            {
                role: "readWrite",
                db: "warndatesdb"
            }
        ]
    }
);