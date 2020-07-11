from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
stores = [
    {'store_name': 'Amazon',
     'items': [
         {'item_name': 'keyboards', 'price': 50}
     ]}
]


# POST - used to receive data
# GET - used to send data back only

@app.route('/')
def home():
    return render_template('index.html')


# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    store = request.get_json()
    stores.append({
        'store_name': store['name'],
        'items': []
    })
    return f"Store {store['name']} was successfully created"


# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['store_name'] == name:
            return jsonify(store)
    return f"The store {name} was not found"


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {item:, price:}
@app.route('/store/<string:store_name>/item', methods=['POST'])
def create_item_in_store(store_name):
    item = request.get_json()
    for store in stores:
        if store['store_name'] == store_name:
            store['items'].append(item)
            return jsonify(store)
    return "store not found"

# GET /store/<string:name>/<string:name>
@app.route('/store/<string:store_name>/<string:item_name>')
def get_items_in_store(store_name, item_name):
    for store in stores:
        if store['store_name'] == store_name:
            for item in store['items']:
                if item['item_name'] == item_name:
                    return jsonify(item)
    return 'item not found'


app.run(port=5000)
