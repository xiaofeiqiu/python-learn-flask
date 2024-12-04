import uuid

from flask import Flask, request
from db import stores, items

app = Flask(__name__)


@app.get('/stores')
def hello_world():  # put application's code here
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**request_data, "id": store_id}
    stores[store_id] = new_store
    return new_store


@app.post("/item")
def create_item():
    request_data = request.get_json()
    if request_data["store_id"] not in stores:
        return {"message": "store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**request_data, "id": item_id}
    items[item_id] = item
    return item


@app.get("/item/<string:id>")
def get_item(id):
    try:
        return items[id]
    except KeyError:
        return {"message": "item not found"}, 404


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "store not found"}, 404


@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return store["items"]
    return {"message": "store not found"}, 404


if __name__ == '__main__':
    app.run()
