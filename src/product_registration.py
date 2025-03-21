import sqlite3

class ProductRegistration:
    def __init__(self):
        self.conn = sqlite3.connect('produtos.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome TEXT,
                           categoria TEXT,
                           preco_custo REAL,
                           preco_venda REAL,
                           quantidade INTEGER,
                           etiqueta_gerada BOOLEAN DEFAULT 0)''')
        self.conn.commit()

    def validar_dados_produto(self, nome, preco_custo, quantidade):
        if not nome or preco_custo < 0 or quantidade < 0:
            raise ValueError("Dados do produto inválidos")

    def adicionar_produto(self, nome, categoria, preco_custo, preco_venda, quantidade):
        self.validar_dados_produto(nome, preco_custo, quantidade)
        if preco_venda is None:
            preco_venda = preco_custo * 2.3
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO produtos (nome, categoria, preco_custo, preco_venda, quantidade) VALUES (?, ?, ?, ?, ?)',
                       (nome, categoria, preco_custo, preco_venda, quantidade))
        self.conn.commit()

    def obter_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        return cursor.fetchall()

    def obter_produto_por_id(self, id_produto):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (id_produto,))
        produto = cursor.fetchone()
        if produto:
            return {
                'id': produto[0],
                'nome': produto[1],
                'categoria': produto[2],
                'preco_custo': produto[3],
                'preco_venda': produto[4],
                'quantidade': produto[5],
                'etiqueta_gerada': produto[6]
            }
        return None

    def exportar_para_csv(self, filename):
        import csv
        produtos = self.obter_produtos()
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nome', 'Categoria', 'Preço de Custo', 'Preço de Venda', 'Quantidade', 'Etiqueta Gerada'])
            writer.writerows(produtos)