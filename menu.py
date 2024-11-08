import requests

def menu():
    while True:
        print("\n--- Gerenciamento de Estoque ---")
        print("1. Adicionar um novo produto")
        print("2. Listar todos os produtos")
        print("3. Buscar um produto pelo nome")
        print("4. Atualizar a quantidade de um produto")
        print("5. Remover um produto do estoque")
        print("6. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            list_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_quantity()
        elif choice == "5":
            remove_product()
        elif choice == "6":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Funções para interagir com os microsserviços

def add_product():
    name = input("Digite o nome do produto: ")
    quantity = int(input("Digite a quantidade: "))
    price = float(input("Digite o preço: "))

    data = {"name": name, "quantity": quantity, "price": price}
    response = requests.post("http://localhost:5000/products", json=data)

    if response.status_code == 201:
        print("Produto adicionado com sucesso!")
    else:
        print("Erro ao adicionar o produto. Verifique se o produto já existe.")

def list_products():
    response = requests.get("http://localhost:5000/products")
    if response.status_code == 200:
        products = response.json()
        if not products:
            print("Nenhum produto em estoque.")
        else:
            print("\n--- Produtos em Estoque ---")
            for product in products:
                print(f"ID: {product['id']}, Nome: {product['name']}, Quantidade: {product['quantity']}, Preço: R${product['price']}")
    else:
        print("Erro ao listar os produtos.")

def search_product():
    name = input("Digite o nome do produto a ser buscado: ")
    response = requests.get(f"http://localhost:5000/products/{name}")

    if response.status_code == 200:
        product = response.json()
        print(f"ID: {product['id']}, Nome: {product['name']}, Quantidade: {product['quantity']}, Preço: R${product['price']}")
    else:
        print("Produto não encontrado.")

def update_quantity():
    name = input("Digite o nome do produto: ")
    quantity = int(input("Digite a nova quantidade: "))

    data = {"quantity": quantity}
    response = requests.put(f"http://localhost:5001/stock/{name}", json=data)

    if response.status_code == 200:
        print("Quantidade atualizada com sucesso!")
    else:
        print("Erro ao atualizar a quantidade ou produto não encontrado.")

def remove_product():
    name = input("Digite o nome do produto a ser removido: ")
    response = requests.delete(f"http://localhost:5001/stock/{name}")

    if response.status_code == 200:
        print("Produto removido com sucesso!")
    else:
        print("Erro ao remover o produto ou produto não encontrado.")

if __name__ == "__main__":
    menu()
