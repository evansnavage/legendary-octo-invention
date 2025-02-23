from flask import Flask, request
from flask_cors import CORS
import backend.src.item_access as ia

app = Flask(__name__)
CORS(app)

@app.route('/get_all_items', methods=['GET'])
def get_all_items():
    return ia.get_all_items()

@app.route('/get_item', methods=['GET'])
def get_item():
    item_id = request.args.get('item_id')
    return ia.get_item(item_id)

@app.route('/create_item', methods=['POST'])
def create_item():
    item = request.json
    print(item)
    name = item.get('name', '')
    description = item.get('description', '')
    price = item.get('price', 0.0)
    quantity = item.get('quantity', 0)
    tags = item.get('tags', '')

    if tags:
        tags = tags.split(' ')
    else:
        tags = []

    if not name or not quantity:
        return 'Missing required fields, name or quantity', 400

    ia.create_item(name, quantity, price, description, tags)
    
    return ['Item created', 200]

@app.route('/update_item', methods=['POST'])
def update_item():
    item = request.json
    item_id = item.get('item_id')
    name = item.get('name')
    description = item.get('description')
    price = item.get('price')
    quantity = item.get('quantity')
    tags = item.get('tags')

    if tags:
        tags = tags.split(' ')

    if not name or not quantity:
        return 'Missing required fields, name or quantity', 400

    ia.update_item(item_id, name, description, price, quantity, tags)
    
    return ['Item updated', 200]

if __name__ == '__main__':
    app.run(debug=True)