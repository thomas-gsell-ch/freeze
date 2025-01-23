class Repository(object):
    def __init__(self, adapter=None):
        self.client = adapter()

    def find_all(self):
        return self.client.find_all()

    def create(self, product):
        return self.client.create(product)

    def update(self, selector, product):
        return self.client.update(selector, product)

    def delete(self, id):
        return self.client.delete(id)
