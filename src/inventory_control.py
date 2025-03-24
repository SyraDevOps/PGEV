import sqlite3
from rich.console import Console
from rich.table import Table

class InventoryControl:
    def __init__(self):
        self.console = Console()
        self.conn = sqlite3.connect('estoque.db')
        self.criar_tabelas()
        self.inventory = self.obter_inventario()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome TEXT,
                           descricao TEXT,
                           categoria TEXT,
                           codigo_barras TEXT,
                           fornecedor TEXT,
                           preco REAL,
                           quantidade INTEGER,
                           local_armazenamento TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS movimentacoes
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_produto INTEGER,
                           tipo TEXT,
                           quantidade INTEGER,
                           data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                           local_armazenamento TEXT)''')
        self.conn.commit()

    def cadastrar_produto(self, nome, descricao, categoria, codigo_barras, fornecedor, preco, quantidade, local_armazenamento):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, categoria, codigo_barras, fornecedor, preco, quantidade, local_armazenamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, descricao, categoria, codigo_barras, fornecedor, preco, quantidade, local_armazenamento))
        self.conn.commit()

    def add_product(self, product_id, quantity, local_armazenamento):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE produtos SET quantidade = quantidade + ? WHERE id = ? AND local_armazenamento = ?', (quantity, product_id, local_armazenamento))
        cursor.execute('INSERT INTO movimentacoes (id_produto, tipo, quantidade, local_armazenamento) VALUES (?, ?, ?, ?)', (product_id, 'entrada', quantity, local_armazenamento))
        self.conn.commit()

    def remove_product(self, product_id, quantity, local_armazenamento):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ? AND local_armazenamento = ?', (quantity, product_id, local_armazenamento))
        cursor.execute('INSERT INTO movimentacoes (id_produto, tipo, quantidade, local_armazenamento) VALUES (?, ?, ?, ?)', (product_id, 'saida', quantity, local_armazenamento))
        self.conn.commit()

    def update_quantity(self, product_id, quantity, local_armazenamento):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ? AND local_armazenamento = ?', (quantity, product_id, local_armazenamento))
        self.conn.commit()

    def check_stock(self, product_id, local_armazenamento):
        cursor = self.conn.cursor()
        cursor.execute('SELECT quantidade FROM produtos WHERE id = ? AND local_armazenamento = ?', (product_id, local_armazenamento))
        stock = cursor.fetchone()[0]
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID do Produto", justify="center")
        table.add_column("Quantidade em Estoque", justify="center")
        table.add_row(str(product_id), str(stock))
        self.console.print(table)
        return stock

    def notify_low_stock(self, threshold):
        cursor = self.conn.cursor()
        cursor.execute('SELECT nome, quantidade FROM produtos WHERE quantidade < ?', (threshold,))
        low_stock_items = cursor.fetchall()
        return low_stock_items

    def obter_movimentacoes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM movimentacoes')
        return cursor.fetchall()

    def obter_inventario(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        return cursor.fetchall()

    def consultar_produto(self, codigo_barras):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
        produto = cursor.fetchone()
        if produto and produto[7] > 0:
            return produto
        return None

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        return cursor.fetchall()