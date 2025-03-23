import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SalesManager:
    def __init__(self):
        self.conn = sqlite3.connect('vendas.db')
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vendas
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_produto INTEGER,
                           quantidade INTEGER,
                           preco_total REAL,
                           forma_pagamento TEXT,
                           desconto REAL,
                           id_cliente INTEGER,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome TEXT,
                           email TEXT,
                           telefone TEXT)''')
        self.conn.commit()

    def registrar_venda(self, id_produto, quantidade, preco_total, forma_pagamento, desconto, id_cliente):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO vendas (id_produto, quantidade, preco_total, forma_pagamento, desconto, id_cliente) VALUES (?, ?, ?, ?, ?, ?)',
                       (id_produto, quantidade, preco_total, forma_pagamento, desconto, id_cliente))
        self.conn.commit()
        return cursor.lastrowid

    def emitir_recibo(self, id_venda):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vendas WHERE id = ?', (id_venda,))
        venda = cursor.fetchone()
        c = canvas.Canvas(f'recibos/recibo_{id_venda}.pdf', pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, "Recibo de Venda")
        c.drawString(100, height - 120, f"ID Venda: {venda[0]}")
        c.drawString(100, height - 140, f"ID Produto: {venda[1]}")
        c.drawString(100, height - 160, f"Quantidade: {venda[2]}")
        c.drawString(100, height - 180, f"Preço Total: {venda[3]}")
        c.drawString(100, height - 200, f"Forma de Pagamento: {venda[4]}")
        c.drawString(100, height - 220, f"Desconto: {venda[5]}")
        c.drawString(100, height - 240, f"ID Cliente: {venda[6]}")
        c.drawString(100, height - 260, f"Data: {venda[7]}")
        c.save()

    def emitir_nota_fiscal(self, id_venda):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vendas WHERE id = ?', (id_venda,))
        venda = cursor.fetchone()
        c = canvas.Canvas(f'notas_fiscais/nf_{id_venda}.pdf', pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, "Nota Fiscal")
        c.drawString(100, height - 120, f"ID Venda: {venda[0]}")
        c.drawString(100, height - 140, f"ID Produto: {venda[1]}")
        c.drawString(100, height - 160, f"Quantidade: {venda[2]}")
        c.drawString(100, height - 180, f"Preço Total: {venda[3]}")
        c.drawString(100, height - 200, f"Forma de Pagamento: {venda[4]}")
        c.drawString(100, height - 220, f"Desconto: {venda[5]}")
        c.drawString(100, height - 240, f"ID Cliente: {venda[6]}")
        c.drawString(100, height - 260, f"Data: {venda[7]}")
        c.save()

    def registrar_cliente(self, nome, email, telefone):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
        self.conn.commit()
        return cursor.lastrowid

    def obter_historico_compras(self, id_cliente):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vendas WHERE id_cliente = ?', (id_cliente,))
        return cursor.fetchall()