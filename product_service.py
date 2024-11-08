import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Inicializando o banco de dados SQLite
def init_db():
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
''')
    connection.commit()
    connection.close()

# Inicializar o banco de dados na primeira execução
init_db()

# Adicionar um novo produto
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    price = data.get('price')

    try:
        connection = sqlite3.connect('inventory.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
        connection.commit()
        connection.close()
        return jsonify({"message": "Produto adicionado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Erro: Produto já existe."}), 400

# Listar todos os produtos
@app.route('/products', methods=['GET'])
def list_products():
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    connection.close()

    product_list = [{"id": row[0], "name": row[1], "quantity": row[2], "price": row[3]} for row in products]
    return jsonify(product_list), 200

# Buscar um produto pelo nome
@app.route('/products/<string:name>', methods=['GET'])
def get_product(name):
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products WHERE name = ?', (name,))
    product = cursor.fetchone()
    connection.close()

    if product:
        product_data = {"id": product[0], "name": product[1], "quantity": product[2], "price": product[3]}
        return jsonify(product_data), 200
    else:
        return jsonify({"message": "Produto não encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000)
