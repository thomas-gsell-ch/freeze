const database = 'productsdb';
const collection = 'products';

// Create a new database.
use(database);

// Create a new collection.
db.createCollection(collection);

// Insert some test data
db.products.insertMany([
    { name: 'Rindfleisch', category: "Fleisch", amount: "1 Kg", location: "n/a", freezingDate: "10-12-2024", bestBefore: "01-01-2025" },
    { name: 'Fish', category: "Fisch", amount: "200 g", location: "n/a", freezingDate: "10-12-2024", bestBefore: "01-01-2025" },
    { name: 'Pizza', category: "Sonstiges", amount: "1", location: "n/a", freezingDate: "10-12-2024", bestBefore: "01-01-2025" },
    { name: 'Vanille Glace', category: "Sonstiges", amount: "5 Stück", location: "Küche", freezingDate: "10-12-2024", bestBefore: "01-03-2025" },
    { name: 'Chicken', category: "Fleisch", amount: "1 Stück", location: "n/a", freezingDate: "10-12-2024", bestBefore: "15-01-2025" },
    { name: 'Hacktätschli', category: "Fleisch", amount: "7 Stück", location: "Keller", freezingDate: "12-12-2024", bestBefore: "15-02-2025" },
    { name: 'Erdbeer Glace', category: "Sonstiges", amount: "2 Stück", location: "Küche", freezingDate: "12-06-2024", bestBefore: "15-01-2025" },
    { name: 'Schokoladen Glace', category: "Sonstiges", amount: "2 Stück", location: "Küche", freezingDate: "12-06-2024", bestBefore: "15-01-2025" },
    { name: 'Crevetten', category: "Fisch", amount: "10 Stück", location: "Keller", freezingDate: "10-06-2024", bestBefore: "10-01-2025" },
    { name: 'Frühlingsrollen', category: "Sonstiges", amount: "10 Stück", location: "Keller", freezingDate: "10-06-2024", bestBefore: "10-01-2025" },
    { name: 'Aprikosen', category: "Früchte", amount: "1 Kg", location: "Keller", freezingDate: "05-06-2024", bestBefore: "10-01-2025" },
    { name: 'Erbsen', category: "Gemüse", amount: "200 g", location: "Keller", freezingDate: "05-06-2024", bestBefore: "10-01-2025" },
    { name: 'Grünebohnen', category: "Gemüse", amount: "200 g", location: "Keller", freezingDate: "05-04-2024", bestBefore: "10-12-2024" },
    { name: 'Himbeeren', category: "Früchte", amount: "500 g", location: "Keller", freezingDate: "04-04-2024", bestBefore: "10-11-2024" },
]);

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