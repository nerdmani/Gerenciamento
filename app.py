from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('home.html')

# Rota para a página de adicionar produto
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Captura os dados do formulário
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']

        # Conectar ao banco e inserir o novo produto
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)',
                     (name, description, price, stock_quantity))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))  # Redireciona para a página inicial

    return render_template('add_product.html')  # Exibe o formulário de adicionar produto

# Rota para a página de inventário (mostrar produtos)
@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('inventory.html', products=products)

def get_filtered_products(filters):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Montagem da consulta SQL com filtros dinâmicos
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if filters.get('name'):
        query += " AND name LIKE ?"
        params.append(f"%{filters['name']}%")
    
    if filters.get('description'):
        query += " AND description LIKE ?"
        params.append(f"%{filters['description']}%")
    
    if filters.get('price_min'):
        query += " AND price >= ?"
        params.append(filters['price_min'])
    
    if filters.get('price_max'):
        query += " AND price <= ?"
        params.append(filters['price_max'])
    
    if filters.get('stock_quantity_min'):
        query += " AND stock_quantity >= ?"
        params.append(filters['stock_quantity_min'])
    
    if filters.get('stock_quantity_max'):
        query += " AND stock_quantity <= ?"
        params.append(filters['stock_quantity_max'])
    
    cursor.execute(query, params)
    products = cursor.fetchall()
    conn.close()
    
    return products

@app.route('/search', methods=['GET'])
def search():
    # Obtendo os parâmetros de filtro da query string
    filters = {
        'name': request.args.get('name'),
        'description': request.args.get('description'),
        'price_min': request.args.get('price_min'),
        'price_max': request.args.get('price_max'),
        'stock_quantity_min': request.args.get('stock_quantity_min'),
        'stock_quantity_max': request.args.get('stock_quantity_max')
    }
    
    # Convertendo para tipo numérico quando necessário
    if filters['price_min']:
        filters['price_min'] = float(filters['price_min'])
    if filters['price_max']:
        filters['price_max'] = float(filters['price_max'])
    if filters['stock_quantity_min']:
        filters['stock_quantity_min'] = int(filters['stock_quantity_min'])
    if filters['stock_quantity_max']:
        filters['stock_quantity_max'] = int(filters['stock_quantity_max'])
    
    # Obtendo os produtos filtrados
    products = get_filtered_products(filters)
    
    # Renderizando o template com os resultados
    return render_template('inventory.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
