from datetime import date

class ProductSchema():
    def __init__(self, id: int, name: str, category: str, amount:int, location: str, freezingDate: date, bestBefore: date):
        self.id = id
        self.name = name
        self.category = category
        self.amount = amount
        self.location = location
        self.freezingDate = freezingDate
        self.bestBefore = bestBefore