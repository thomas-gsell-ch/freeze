# from ..repository import Repository
# from ..repository.mongo import MongoRepository
# TODO: for docker container relative imports are not working
from repository import Repository
from repository.mongo import MongoRepository
from .schema import ProductSchema


class Service(object):
    def __init__(self, repo_client=Repository(adapter=MongoRepository)):
        self.repo_client = repo_client

    def find_all_products(self):
        products = self.repo_client.find_all()
        return products

    def create_product(self, product):
        productId = self.repo_client.create(product)
        return productId

    def update_product_with(self, product_id, product):
        records_affected = self.repo_client.update(
            {'product_id': product_id}, product)
        return records_affected > 0

    def delete_product_by_id(self, id):
        records_affected = self.repo_client.delete(id)
        return records_affected > 0
