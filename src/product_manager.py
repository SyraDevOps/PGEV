# Este arquivo implementa a interface de usuário no terminal para o sistema de gestão de produtos.
import csv
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from barcode_reader import BarcodeReader
from inventory_control import InventoryControl
from sales_recording import RegistroVendas
from report_generation import GeracaoRelatorios
import logging

# Configuração do logger
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class TUI:
    def __init__(self):
        self.console = Console()
        self.product_registration = ProductRegistration()
        self.barcode_reader = BarcodeReader()
        self.inventory_control = InventoryControl()
        self.sales_recording = RegistroVendas()
        self.report_generation = GeracaoRelatorios(self.sales_recording.obter_resumo_vendas(), self.inventory_control.inventory)

    def exibir_menu(self):
        self.console.clear()
        self.console.print("[bold cyan]Sistema de Gestão de Produtos[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Opção", justify="center")
        table.add_column("Descrição", justify="left")
        table.add_row("1", "Cadastrar um novo produto")
        table.add_row("2", "Exibir Dashboard")
        table.add_row("3", "Gerenciar inventário")
        table.add_row("4", "Registrar uma venda")
        table.add_row("5", "Gerar relatórios")
        table.add_row("6", "Exportar dados para CSV")
        table.add_row("7", "Consultar preço de um item")
        table.add_row("0", "Sair")
        self.console.print(table)

    def obter_escolha_usuario(self):
        escolha = Prompt.ask("Por favor, selecione uma opção")
        return escolha

    def run(self):
        while True:
            self.exibir_menu()
            escolha = self.obter_escolha_usuario()
            if escolha == "1":
                self.console.print("Você selecionou: Cadastrar um novo produto")
                self.cadastrar_produto()
            elif escolha == "2":
                self.console.print("Você selecionou: Exibir Dashboard")
                self.exibir_dashboard()
            elif escolha == "3":
                self.console.print("Você selecionou: Gerenciar inventário")
                self.gerenciar_inventario()
            elif escolha == "4":
                self.console.print("Você selecionou: Registrar uma venda")
                self.registrar_venda()
            elif escolha == "5":
                self.console.print("Você selecionou: Gerar relatórios")
                self.gerar_relatorios()
            elif escolha == "6":
                self.console.print("Você selecionou: Exportar dados para CSV")
                self.exportar_dados_para_csv()
            elif escolha == "7":
                self.console.print("Você selecionou: Consultar preço de um item")
                self.consultar_preco_item()
            elif escolha == "0":
                self.console.print("Saindo da aplicação...")
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def cadastrar_produto(self):
        nome = Prompt.ask("Digite o nome do produto")
        categoria = Prompt.ask("Digite a categoria do produto")
        preco_custo = float(Prompt.ask("Digite o preço de custo do produto"))
        preco_venda = Prompt.ask("Digite o preço de venda do produto (opcional)", default=None)
        if preco_venda:
            preco_venda = float(preco_venda)
        quantidade = int(Prompt.ask("Digite a quantidade do produto"))
        self.product_registration.adicionar_produto(nome, categoria, preco_custo, preco_venda, quantidade)
        self.console.print(f"Produto '{nome}' cadastrado com sucesso.")
        logging.info(f"Produto cadastrado: {nome}, Categoria: {categoria}, Preço de Custo: {preco_custo}, Preço de Venda: {preco_venda}, Quantidade: {quantidade}")

    def cdbr(self):
        acao = Prompt.ask("Digite a ação (1: Gerar código de barras, 2: Ler código de barras)")
        if acao == "1":
            self.gerar_codigo_barras()
        elif acao == "2":
            self.ler_codigo_barras()
        else:
            self.console.print("[bold red]Ação inválida, por favor, tente novamente.[/bold red]")

    def gerar_codigo_barras(self):
        id_produto = Prompt.ask("Digite o ID do produto para geração do código de barras")
        filename = self.barcode_reader.generate_barcode(id_produto)
        self.console.print(f"Código de barras gerado e salvo como {filename}")
        logging.info(f"Código de barras gerado para o produto ID: {id_produto}")

    def ler_codigo_barras(self):
        caminho_imagem = Prompt.ask("Digite o caminho da imagem do código de barras")
        codigos = self.barcode_reader.read_barcode(caminho_imagem)
        self.console.print(f"Códigos de barras lidos: {codigos}")
        logging.info(f"Códigos de barras lidos da imagem: {caminho_imagem}")

    def gerenciar_inventario(self):
        id_produto = Prompt.ask("Digite o ID do produto")
        acao = Prompt.ask("Digite a ação (1: adicionar, 2: remover, 3: atualizar, 4: verificar)")
        if acao == "1":
            quantidade = int(Prompt.ask("Digite a quantidade a adicionar"))
            self.inventory_control.add_product(id_produto, quantidade)
            self.console.print(f"Adicionado {quantidade} unidades do produto ID {id_produto} ao inventário.")
            logging.info(f"Adicionado {quantidade} unidades do produto ID {id_produto} ao inventário.")
        elif acao == "2":
            quantidade = int(Prompt.ask("Digite a quantidade a remover"))
            self.inventory_control.remove_product(id_produto, quantidade)
            self.console.print(f"Removido {quantidade} unidades do produto ID {id_produto} do inventário.")
            logging.info(f"Removido {quantidade} unidades do produto ID {id_produto} do inventário.")
        elif acao == "3":
            quantidade = int(Prompt.ask("Digite a nova quantidade"))
            self.inventory_control.update_quantity(id_produto, quantidade)
            self.console.print(f"Quantidade do produto ID {id_produto} atualizada para {quantidade}.")
            logging.info(f"Quantidade do produto ID {id_produto} atualizada para {quantidade}.")
        elif acao == "4":
            estoque = self.inventory_control.check_stock(id_produto)
            self.console.print(f"O produto ID {id_produto} tem {estoque} unidades em estoque.")
            logging.info(f"O produto ID {id_produto} tem {estoque} unidades em estoque.")
            acao_verificar = Prompt.ask("Digite a ação (1: sair, 2: atualizar)")
            if acao_verificar == "2":
                self.gerenciar_inventario()
        else:
            self.console.print("[bold red]Ação inválida, por favor, tente novamente.[/bold red]")

    def registrar_venda(self):
        id_produto = Prompt.ask("Digite o ID do produto")
        quantidade = int(Prompt.ask("Digite a quantidade vendida"))
        preco = float(Prompt.ask("Digite o preço por unidade"))
        desconto = float(Prompt.ask("Digite o desconto (se houver)", default="0"))
        vendedora = Prompt.ask("Digite o nome da vendedora")
        registro_venda = self.sales_recording.registrar_venda(id_produto, quantidade, preco, desconto, vendedora)
        self.console.print(f"Venda registrada: {registro_venda}")
        logging.info(f"Venda registrada: Produto ID {id_produto}, Quantidade {quantidade}, Preço {preco}, Desconto {desconto}, Vendedora {vendedora}")

    def gerar_relatorios(self):
        tipo_relatorio = Prompt.ask("Digite o tipo de relatório (1: vendas, 2: inventário, 3: mais vendidos)")
        if tipo_relatorio == "1":
            id_produto = Prompt.ask("Digite o ID do produto (opcional)", default=None)
            if id_produto:
                id_produto = int(id_produto)
            relatorio = self.report_generation.gerar_relatorio_vendas(id_produto)
            self.console.print(f"Relatório de vendas: {relatorio}")
            logging.info(f"Relatório de vendas gerado para o produto ID: {id_produto}")
        elif tipo_relatorio == "2":
            relatorio = self.report_generation.gerar_relatorio_inventario()
            self.console.print(f"Relatório de inventário: {relatorio}")
            logging.info("Relatório de inventário gerado")
        elif tipo_relatorio == "3":
            relatorio = self.report_generation.produtos_mais_vendidos()
            self.console.print(f"Relatório dos produtos mais vendidos: {relatorio}")
            logging.info("Relatório dos produtos mais vendidos gerado")
        else:
            self.console.print("[bold red]Tipo de relatório inválido, por favor, tente novamente.[/bold red]")

    def exportar_dados_para_csv(self):
        nome_grupo = Prompt.ask("Digite o nome do grupo para exportação CSV")
        self.product_registration.exportar_para_csv(f"{nome_grupo}_produtos.csv")
        self.sales_recording.exportar_vendas_para_csv(f"{nome_grupo}_vendas.csv")
        self.report_generation.exportar_comentarios_para_csv(f"{nome_grupo}_comentarios.csv")
        self.console.print(f"Dados exportados para {nome_grupo}_produtos.csv, {nome_grupo}_vendas.csv e {nome_grupo}_comentarios.csv")
        logging.info(f"Dados exportados para {nome_grupo}_produtos.csv, {nome_grupo}_vendas.csv e {nome_grupo}_comentarios.csv")

    def adicionar_comentario(self):
        nome = Prompt.ask("Digite seu nome")
        comentario = Prompt.ask("Digite seu comentário")
        ocorrido = Prompt.ask("Digite o ocorrido (se houver)", default=None)
        self.report_generation.adicionar_comentario(nome, comentario, ocorrido)
        self.console.print(f"Comentário adicionado com sucesso.")
        logging.info(f"Comentário adicionado: Nome {nome}, Comentário {comentario}, Ocorrido {ocorrido}")

    def consultar_preco_item(self):
        id_produto = Prompt.ask("Digite o ID do produto")
        produto = self.product_registration.obter_produto_por_id(id_produto)
        if produto:
            self.console.print(f"Produto: {produto['nome']}")
            self.console.print(f"Preço de Custo: {produto['preco_custo']}")
            self.console.print(f"Preço de Venda: {produto['preco_venda']}")
            logging.info(f"Consulta de preço: Produto ID {id_produto}, Preço de Custo {produto['preco_custo']}, Preço de Venda {produto['preco_venda']}")
        else:
            self.console.print("[bold red]Produto não encontrado.[/bold red]")
            logging.warning(f"Produto não encontrado: ID {id_produto}")

    def exibir_dashboard(self):
        # Exemplo simples de dashboard
        self.console.print("Dashboard de Análise")
        self.console.print("Total de Produtos: 100")
        self.console.print("Produtos em Baixo Estoque: 5")
        self.console.print("Produtos Mais Vendidos: Produto A, Produto B")

class ProductRegistration:
    def __init__(self):
        self.produtos = []
        self.notificacoes = []

    def validar_dados_produto(self, nome, preco_custo, quantidade):
        if not nome:
            raise ValueError("O nome do produto não pode ser vazio.")
        if preco_custo < 0:
            raise ValueError("O preço de custo não pode ser negativo.")
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

    def adicionar_produto(self, nome, categoria, preco_custo, preco_venda, quantidade):
        self.validar_dados_produto(nome, preco_custo, quantidade)
        produto = (nome, categoria, preco_custo, preco_venda, quantidade)
        self.produtos.append(produto)
        if quantidade < 10:
            self.notificacoes.append(f"Produto {nome} está com baixo estoque!")

    def obter_produtos(self, categoria=None):
        if categoria:
            return [produto for produto in self.produtos if produto[1] == categoria]
        return self.produtos

    def obter_notificacoes(self):
        return self.notificacoes

    def exportar_dados(self, filepath):
        produtos = self.obter_produtos()
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nome', 'Categoria', 'Preço de Custo', 'Preço de Venda', 'Quantidade'])
            for produto in produtos:
                writer.writerow(produto)