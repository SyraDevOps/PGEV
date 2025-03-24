import sqlite3

class RegistroVendas:
    def __init__(self):
        self.conn = sqlite3.connect('vendas.db')
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vendas
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_produto INTEGER,
                           quantidade INTEGER,
                           preco REAL,
                           desconto REAL,
                           preco_total REAL,
                           vendedora TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lucro
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lucro_total REAL)''')
        self.conn.commit()

    def registrar_venda(self, id_produto, quantidade, preco, desconto=0, vendedora=""):
        preco_total = (preco * quantidade) - desconto
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO vendas (id_produto, quantidade, preco, desconto, preco_total, vendedora) VALUES (?, ?, ?, ?, ?, ?)',
                       (id_produto, quantidade, preco, desconto, preco_total, vendedora))
        cursor.execute('INSERT INTO lucro (lucro_total) VALUES (?)', (preco_total,))
        self.conn.commit()
        return {
            'id_produto': id_produto,
            'quantidade': quantidade,
            'preco': preco,
            'desconto': desconto,
            'preco_total': preco_total,
            'vendedora': vendedora
        }

    def obter_resumo_vendas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vendas')
        return cursor.fetchall()

    def exportar_vendas_para_csv(self, filename):
        import csv
        vendas = self.obter_resumo_vendas()
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'ID Produto', 'Quantidade', 'Preço', 'Desconto', 'Preço Total', 'Vendedora'])
            writer.writerows(vendas)