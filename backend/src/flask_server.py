from flask import Flask, request
import backend.src.item_access as ia

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/get_all_items')
def get_all_items():
    return ia.get_all_items()

@app.route('/get_item')
def get_item():
    name = request.args.get('name')
    return ia.get_items_by_name(name)

@app.route('/update_item_quantity')
def update_item_quantity():
    name = request.args.get('name')
    quantity = request.args.get('quantity')
    return ia.update_item_quantity(name, quantity)

@app.route('/update_item_price')
def update_item_price():
    name = request.args.get('name')
    price = request.args.get('price')
    return ia.update_item_price(name, price)

@app.route('/update_item_description')
def update_item_description():
    name = request.args.get('name')
    description = request.args.get('description')
    return ia.update_item_description(name, description)

@app.route('/add_tags')
def add_tags():
    name = request.args.get('name')
    tags = request.args.get('tags')
    return ia.add_tags(name, tags)

@app.route('/remove_tags')
def remove_tags():
    name = request.args.get('name')
    tags = request.args.get('tags')
    return ia.remove_tags(name, tags)

@app.route('/delete_item')
def delete_item_by_name():
    name = request.args.get('name')
    return ia.delete_item_by_name(name)

@app.route('/create_item')
def create_item():
    name = request.args.get('name')
    quantity = request.args.get('quantity')
    price = request.args.get('price')
    description = request.args.get('description')
    tags = request.args.get('tags')
    return ia.create_item(name, quantity, price, description, tags)

@app.route('/get_price')
def get_price():
    name = request.args.get('name')
    return ia.get_price(name)

@app.route('/get_quantity')
def get_quantity():
    name = request.args.get('name')
    return ia.get_item_quantity(name)

if __name__ == '__main__':
    app.run(debug=True)