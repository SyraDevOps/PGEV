import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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
        cursor = self.conn.cursor()
        cursor.execute('SELECT id_produto, SUM(quantidade) as total_vendido FROM vendas GROUP BY id_produto ORDER BY total_vendido DESC')
        return cursor.fetchall()

    def produtos_menos_vendidos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id_produto, SUM(quantidade) as total_vendido FROM vendas GROUP BY id_produto ORDER BY total_vendido ASC')
        return cursor.fetchall()

    def analise_rentabilidade(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id_produto, SUM(preco_total) as total_vendas, SUM(preco_custo * quantidade) as total_custo FROM vendas JOIN produtos ON vendas.id_produto = produtos.id GROUP BY id_produto')
        return cursor.fetchall()

    def exportar_relatorio(self, dados_relatorio, formato='csv'):
        if formato == 'csv':
            df = pd.DataFrame(dados_relatorio)
            df.to_csv('relatorio.csv', index=False)
        elif formato == 'excel':
            df = pd.DataFrame(dados_relatorio)
            df.to_excel('relatorio.xlsx', index=False)
        elif formato == 'pdf':
            c = canvas.Canvas('relatorio.pdf', pagesize=letter)
            width, height = letter
            c.drawString(100, height - 100, "Relatório")
            c.drawString(100, height - 120, "----------------")
            y = height - 140
            for linha in dados_relatorio:
                c.drawString(100, y, str(linha))
                y -= 20
            c.save()

    def adicionar_comentario(self, nome, comentario, ocorrido=None):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO relatorios (nome, comentario, ocorrido) VALUES (?, ?, ?)',
                       (nome, comentario, ocorrido))
        self.conn.commit()

    def exportar_comentarios_para_csv(self, filename):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM relatorios')
        comentarios = cursor.fetchall()
        df = pd.DataFrame(comentarios, columns=['ID', 'Nome', 'Comentário', 'Ocorrido'])
        df.to_csv(filename, index=False)

    def exportar_relatorio_fiscal_para_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, "Relatório Fiscal")
        c.drawString(100, height - 120, "----------------")
        y = height - 140
        for venda in self.dados_vendas:
            c.drawString(100, y, f"ID Produto: {venda['id_produto']}, Quantidade: {venda['quantidade']}, Preço Total: {venda['preco_total']}")
            y -= 20
        c.save()

    def gerar_relatorio_kpis(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT SUM(preco_total) as faturamento, COUNT(*) as total_vendas FROM vendas')
        resultado = cursor.fetchone()
        kpis = {
            'faturamento': resultado[0],
            'total_vendas': resultado[1]
        }
        return kpis

    def gerar_graficos_faturamento_fluxo_caixa(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT DATE(timestamp) as data, SUM(preco_total) as faturamento FROM vendas GROUP BY data')
        dados = cursor.fetchall()
        df = pd.DataFrame(dados, columns=['data', 'faturamento'])
        df['data'] = pd.to_datetime(df['data'])
        df.set_index('data', inplace=True)
        df.plot(kind='line', y='faturamento', title='Faturamento Diário')
        plt.savefig('graficos/faturamento_diario.png')

    def gerar_relatorios_preditivos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT DATE(timestamp) as data, SUM(quantidade) as quantidade FROM vendas GROUP BY data')
        dados = cursor.fetchall()
        df = pd.DataFrame(dados, columns=['data', 'quantidade'])
        df['data'] = pd.to_datetime(df['data'])
        df.set_index('data', inplace=True)
        df['dia_juliano'] = df.index.to_julian_date()
        X = df['dia_juliano'].values.reshape(-1, 1)
        y = df['quantidade'].values
        modelo = LinearRegression()
        modelo.fit(X, y)
        previsoes = modelo.predict(X)
        df['previsao'] = previsoes
        df.plot(kind='line', y=['quantidade', 'previsao'], title='Previsão de Demanda')
        plt.savefig('graficos/previsao_demanda.png')

    def gerar_relatorios_sazonalidade(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT strftime("%m", timestamp) as mes, SUM(quantidade) as quantidade FROM vendas GROUP BY mes')
        dados = cursor.fetchall()
        df = pd.DataFrame(dados, columns=['mes', 'quantidade'])
        df['mes'] = df['mes'].astype(int)
        df.plot(kind='bar', x='mes', y='quantidade', title='Sazonalidade de Vendas')
        plt.savefig('graficos/sazonalidade_vendas.png')

    def auditoria_movimentacao_estoque_vendas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM movimentacoes')
        movimentacoes = cursor.fetchall()
        cursor.execute('SELECT * FROM vendas')
        vendas = cursor.fetchall()
        return movimentacoes, vendas

    def comparacao_periodos(self, periodo1_inicio, periodo1_fim, periodo2_inicio, periodo2_fim):
        cursor = self.conn.cursor()
        cursor.execute('SELECT SUM(preco_total) as faturamento FROM vendas WHERE timestamp BETWEEN ? AND ?', (periodo1_inicio, periodo1_fim))
        faturamento_periodo1 = cursor.fetchone()[0]
        cursor.execute('SELECT SUM(preco_total) as faturamento FROM vendas WHERE timestamp BETWEEN ? AND ?', (periodo2_inicio, periodo2_fim))
        faturamento_periodo2 = cursor.fetchone()[0]
        comparacao = {
            'periodo1': faturamento_periodo1,
            'periodo2': faturamento_periodo2,
            'crescimento': (faturamento_periodo2 - faturamento_periodo1) / faturamento_periodo1 * 100 if faturamento_periodo1 else 0
        }
        return comparacao