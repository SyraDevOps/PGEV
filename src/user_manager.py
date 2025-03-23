import sqlite3

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect('usuarios.db')
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           usuario TEXT UNIQUE,
                           senha TEXT,
                           nivel_acesso TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS atividades
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           usuario TEXT,
                           acao TEXT,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS horarios
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           usuario TEXT,
                           entrada DATETIME,
                           saida DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS metas
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           usuario TEXT,
                           meta_vendas INTEGER)''')
        self.conn.commit()

    def criar_usuario(self, usuario, senha, nivel_acesso):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO usuarios (usuario, senha, nivel_acesso) VALUES (?, ?, ?)', (usuario, senha, nivel_acesso))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def autenticar_usuario(self, usuario, senha):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
        return cursor.fetchone() is not None

    def registrar_atividade(self, usuario, acao):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO atividades (usuario, acao) VALUES (?, ?)', (usuario, acao))
        self.conn.commit()

    def registrar_horario(self, usuario, entrada, saida):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO horarios (usuario, entrada, saida) VALUES (?, ?, ?)', (usuario, entrada, saida))
        self.conn.commit()

    def definir_meta_vendas(self, usuario, meta_vendas):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO metas (usuario, meta_vendas) VALUES (?, ?)', (usuario, meta_vendas))
        self.conn.commit()

    def obter_atividades(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM atividades')
        return cursor.fetchall()

    def obter_horarios(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM horarios')
        return cursor.fetchall()

    def obter_metas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM metas')
        return cursor.fetchall()