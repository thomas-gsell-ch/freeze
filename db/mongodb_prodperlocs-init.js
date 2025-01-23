const database = 'prodperlocsdb';
const collection = 'prodperlocs';

// Create a new database.
use(database);

// Create a new collection.
db.createCollection(collection);


// Insert some test data
db.prodperlocs.insertMany([
  {
    loc: "Dachboden",
    items: [
      { name: "Kichererbsen", amount: "10 kg", warndate: "2026-02-06" },
      { name: "Wein", amount: "20 Stk", warndate: "2030-10-01" }
    ]
  },
  {
    loc: "Küche",
    items: [
      { name: "Yogurt", amount: "3 Stk", warndate: "2025-02-01" }
    ]
  },
  {
    loc: "Keller",
    items: [
      { name: "Butter", amount: "500g", warndate: "2025-09-06" },
      { name: "Bananen", amount: "10 kg", warndate: "2025-12-07" },
      { name: "Schweinssteaks", amount: "4 Stk", warndate: "2025-06-01" }
    ]
  }
]);

//print("Database initialized with inventory data!");


db.createUser(
    {
        user: "dbuser", // user for database which shall be created
        pwd: "hellouser",
        roles: [
            {
                role: "readWrite",
                db: "productsdb"
            }
        ]
    }
);