import sqlite3

class ClientManager:
    def __init__(self):
        self.conn = sqlite3.connect('clientes.db')
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome TEXT,
                           telefone TEXT,
                           email TEXT)''')
        self.conn.commit()

    def adicionar_cliente(self, nome, telefone, email):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)', (nome, telefone, email))
        self.conn.commit()

    def obter_clientes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT nome, telefone, email FROM clientes')
        return [{'nome': row[0], 'telefone': row[1], 'email': row[2]} for row in cursor.fetchall()]