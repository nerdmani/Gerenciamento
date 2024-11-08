import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Atualizar a quantidade de um produto
@app.route('/stock/<string:name>', methods=['PUT'])
def update_quantity(name):
    quantity = request.get_json().get("quantity")

    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products WHERE name = ?', (name,))
    product = cursor.fetchone()

    if product:
        cursor.execute('UPDATE products SET quantity = ? WHERE name = ?', (quantity, name))
        connection.commit()
        connection.close()
        return jsonify({"message": "Quantidade atualizada com sucesso!"}), 200
    else:
        connection.close()
        return jsonify({"message": "Produto não encontrado"}), 404

# Remover um produto do estoque
@app.route('/stock/<string:name>', methods=['DELETE'])
def remove_product(name):
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products WHERE name = ?', (name,))
    product = cursor.fetchone()

    if product:
        cursor.execute('DELETE FROM products WHERE name = ?', (name,))
        connection.commit()
        connection.close()
        return jsonify({"message": "Produto removido com sucesso!"}), 200
    else:
        connection.close()
        return jsonify({"message": "Produto não encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5001)
