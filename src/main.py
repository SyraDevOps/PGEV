from tui import TUI
from user_manager import UserManager
from sales_manager import SalesManager
from inventory_control import InventoryControl
from expenses_manager import ExpensesManager

def criar_usuario(user_manager):
    usuario = input("Novo Usuário: ")
    senha = input("Nova Senha: ")
    nivel_acesso = input("Nível de Acesso (admin/usuario): ")
    if user_manager.criar_usuario(usuario, senha, nivel_acesso):
        print("Usuário criado com sucesso!")
    else:
        print("Erro: Usuário já existe.")

def autenticar_usuario(user_manager):
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    if user_manager.autenticar_usuario(usuario, senha):
        return usuario
    else:
        print("Autenticação falhou!")
        return None

if __name__ == "__main__":
    user_manager = UserManager()
    sales_manager = SalesManager()
    inventory_control = InventoryControl()
    expenses_manager = ExpensesManager()
    while True:
        print("1. Criar Usuário")
        print("2. Autenticar Usuário")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            criar_usuario(user_manager)
        elif escolha == "2":
            usuario = autenticar_usuario(user_manager)
            if usuario:
                user_manager.registrar_atividade(usuario, "Login")
                tui = TUI(usuario, user_manager, sales_manager, inventory_control, expenses_manager)
                tui.run()
                break
        else:
            print("Opção inválida!")