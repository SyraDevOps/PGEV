from flask import Flask, request, jsonify, render_template, send_from_directory
import logging
import qrcode
import os
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configurar logging
logging.basicConfig(
    filename='logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Diretórios para armazenamento
QRCODE_DIR = '../qrcode'
os.makedirs(QRCODE_DIR, exist_ok=True)

# Arquivos de dados
PRODUTOS_FILE = 'produtos.json'
CLIENTES_FILE = 'clientes.json'
VENDAS_FILE = 'vendas.json'

# Funções auxiliares para manipulação de dados
def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

# Rotas para Produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = carregar_dados(PRODUTOS_FILE)
    return jsonify(produtos)

@app.route('/api/produtos/<codigo_barras>', methods=['GET'])
def obter_produto(codigo_barras):
    produtos = carregar_dados(PRODUTOS_FILE)
    produto = next((p for p in produtos if p['codigo_barras'] == codigo_barras), None)
    if produto:
        return jsonify(produto)
    return jsonify({"error": "Produto não encontrado"}), 404

@app.route('/api/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados inválidos"}), 400
        
    produtos = carregar_dados(PRODUTOS_FILE)
    
    # Verificar se o código de barras já existe
    if any(p['codigo_barras'] == dados['codigo_barras'] for p in produtos):
        return jsonify({"error": "Produto com este código de barras já existe"}), 409
    
    produtos.append(dados)
    salvar_dados(PRODUTOS_FILE, produtos)
    
    # Registrar no log
    logging.info(
        f"Produto cadastrado: {dados['nome']}, Descrição: {dados['descricao']}, "
        f"Categoria: {dados['categoria']}, Código de Barras: {dados['codigo_barras']}, "
        f"Fornecedor: {dados['fornecedor']}, Preço: {dados['preco']}, "
        f"Quantidade: {dados['quantidade']}, Local de Armazenamento: {dados['local_armazenamento']}"
    )
    
    # Gerar QR codes
    for unidade in range(1, int(dados['quantidade']) + 1):
        gerar_qrcode(dados['nome'], dados['codigo_barras'], unidade)
    
    return jsonify({"message": "Produto cadastrado com sucesso", "produto": dados}), 201

@app.route('/api/produtos/<codigo_barras>', methods=['PUT'])
def atualizar_produto(codigo_barras):
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados inválidos"}), 400
        
    produtos = carregar_dados(PRODUTOS_FILE)
    index = next((i for i, p in enumerate(produtos) if p['codigo_barras'] == codigo_barras), None)
    
    if index is None:
        return jsonify({"error": "Produto não encontrado"}), 404
        
    produtos[index] = dados
    salvar_dados(PRODUTOS_FILE, produtos)
    
    logging.info(f"Produto atualizado: {dados['nome']}, Código de Barras: {codigo_barras}")
    
    return jsonify({"message": "Produto atualizado com sucesso", "produto": dados})

@app.route('/api/produtos/<codigo_barras>', methods=['DELETE'])
def excluir_produto(codigo_barras):
    produtos = carregar_dados(PRODUTOS_FILE)
    index = next((i for i, p in enumerate(produtos) if p['codigo_barras'] == codigo_barras), None)
    
    if index is None:
        return jsonify({"error": "Produto não encontrado"}), 404
        
    produto = produtos.pop(index)
    salvar_dados(PRODUTOS_FILE, produtos)
    
    logging.info(f"Produto excluído: {produto['nome']}, Código de Barras: {codigo_barras}")
    
    return jsonify({"message": "Produto excluído com sucesso"})

# Função para gerar QR code
def gerar_qrcode(nome_produto, codigo_barras, unidade):
    dados_qr = f"Produto: {nome_produto}\nCódigo: {codigo_barras}\nUnidade: {unidade}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(dados_qr)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Salvar o QR code
    filename = f"{nome_produto}_{unidade}.png"
    filepath = os.path.join(QRCODE_DIR, filename)
    img.save(filepath)
    
    logging.info(f"QR Code gerado para o produto: {nome_produto}, Unidade: {unidade}")
    return filename

@app.route('/api/qrcode/<nome_produto>/<int:unidade>', methods=['GET'])
def obter_qrcode(nome_produto, unidade):
    filename = f"{nome_produto}_{unidade}.png"
    filepath = os.path.join(QRCODE_DIR, filename)
    
    if os.path.exists(filepath):
        return jsonify({"qrcode_path": filepath})
    else:
        return jsonify({"error": "QR code não encontrado"}), 404

# Rotas para Vendas
@app.route('/api/vendas', methods=['GET'])
def listar_vendas():
    vendas = carregar_dados(VENDAS_FILE)
    return jsonify(vendas)

@app.route('/api/vendas', methods=['POST'])
def registrar_venda():
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados inválidos"}), 400
        
    vendas = carregar_dados(VENDAS_FILE)
    
    # Adicionar timestamp
    dados['data_hora'] = datetime.now().isoformat()
    
    vendas.append(dados)
    salvar_dados(VENDAS_FILE, vendas)
    
    # Registrar no log
    logging.info(
        f"Venda registrada: Código de Barras: {dados['codigo_barras']}, "
        f"Quantidade: {dados['quantidade']}, Preço Total: {dados['preco_total']}, "
        f"Forma de Pagamento: {dados['forma_pagamento']}, Desconto: {dados['desconto']}, "
        f"Nome do Cliente: {dados['nome_cliente']}"
    )
    
    # Atualizar estoque
    atualizar_estoque(dados['codigo_barras'], dados['quantidade'])
    
    return jsonify({"message": "Venda registrada com sucesso", "venda": dados}), 201

def atualizar_estoque(codigo_barras, quantidade_vendida):
    produtos = carregar_dados(PRODUTOS_FILE)
    index = next((i for i, p in enumerate(produtos) if p['codigo_barras'] == codigo_barras), None)
    
    if index is not None:
        produtos[index]['quantidade'] = int(produtos[index]['quantidade']) - int(quantidade_vendida)
        salvar_dados(PRODUTOS_FILE, produtos)

# Rotas para Clientes
@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    clientes = carregar_dados(CLIENTES_FILE)
    return jsonify(clientes)

@app.route('/api/clientes/<nome>', methods=['GET'])
def obter_cliente(nome):
    clientes = carregar_dados(CLIENTES_FILE)
    cliente = next((c for c in clientes if c['nome'].lower() == nome.lower()), None)
    if cliente:
        return jsonify(cliente)
    return jsonify({"error": "Cliente não encontrado"}), 404

@app.route('/api/clientes', methods=['POST'])
def adicionar_cliente():
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados inválidos"}), 400
        
    clientes = carregar_dados(CLIENTES_FILE)
    
    # Verificar se o cliente já existe
    if any(c['nome'].lower() == dados['nome'].lower() for c in clientes):
        return jsonify({"error": "Cliente já cadastrado"}), 409
    
    clientes.append(dados)
    salvar_dados(CLIENTES_FILE, clientes)
    
    # Registrar no log
    logging.info(f"Cliente adicionado: {dados['nome']}, Telefone: {dados['telefone']}, Email: {dados['email']}.")
    
    return jsonify({"message": "Cliente adicionado com sucesso", "cliente": dados}), 201

# Adicione estas rotas para servir a página HTML e os QR codes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qrcode/<path:filename>')
def qrcode_file(filename):
    return send_from_directory(QRCODE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)