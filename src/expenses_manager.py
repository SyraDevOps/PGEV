import sqlite3

class ExpensesManager:
    def __init__(self):
        self.conn = sqlite3.connect('gastos.db')
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gastos
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           descricao TEXT,
                           valor REAL,
                           data DATE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS salarios
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           funcionario TEXT,
                           valor REAL,
                           data DATE)''')
        self.conn.commit()

    def registrar_gasto(self, descricao, valor, data):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO gastos (descricao, valor, data) VALUES (?, ?, ?)', (descricao, valor, data))
        self.conn.commit()

    def registrar_salario(self, funcionario, valor, data):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO salarios (funcionario, valor, data) VALUES (?, ?, ?)', (funcionario, valor, data))
        self.conn.commit()

    def obter_gastos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM gastos')
        return cursor.fetchall()

    def obter_salarios(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM salarios')
        return cursor.fetchall()