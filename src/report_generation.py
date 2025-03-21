import sqlite3

class GeracaoRelatorios:
    def __init__(self, dados_vendas, dados_inventario):
        self.dados_vendas = dados_vendas
        self.dados_inventario = dados_inventario
        self.conn = sqlite3.connect('relatorios.db')
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS relatorios
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome TEXT,
                           comentario TEXT,
                           ocorrido TEXT)''')
        self.conn.commit()

    def gerar_relatorio_vendas(self, id_produto=None):
        if id_produto:
            vendas = [venda for venda in self.dados_vendas if venda['id_produto'] == id_produto]
        else:
            vendas = self.dados_vendas
        return vendas

    def gerar_relatorio_inventario(self):
        return self.dados_inventario

    def produtos_mais_vendidos(self):
        pass

    def exportar_relatorio(self, dados_relatorio, formato='csv'):
        import csv
        if formato == 'csv':
            with open('relatorio.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(dados_relatorio)
        elif formato == 'json':
            import json
            with open('relatorio.json', 'w') as file:
                json.dump(dados_relatorio, file)

    def adicionar_comentario(self, nome, comentario, ocorrido=None):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO relatorios (nome, comentario, ocorrido) VALUES (?, ?, ?)',
                       (nome, comentario, ocorrido))
        self.conn.commit()

    def exportar_comentarios_para_csv(self, filename):
        import csv
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM relatorios')
        comentarios = cursor.fetchall()
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nome', 'Comentário', 'Ocorrido'])
            writer.writerows(comentarios)