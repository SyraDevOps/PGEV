import os
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from product_manager import ProductRegistration
from barcode_reader import BarcodeReader
from inventory_control import InventoryControl
from sales_recording import RegistroVendas
from report_generation import GeracaoRelatorios
from client_manager import ClientManager
from expenses_manager import ExpensesManager
import logging
import matplotlib.pyplot as plt

# Configuração do logger
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class TUI:
    def __init__(self, usuario, user_manager, sales_manager, inventory_control, expenses_manager):
        self.console = Console()
        self.usuario = usuario
        self.user_manager = user_manager
        self.sales_manager = sales_manager
        self.inventory_control = inventory_control
        self.expenses_manager = expenses_manager
        self.product_registration = ProductRegistration()
        self.barcode_reader = BarcodeReader()
        self.sales_recording = RegistroVendas()
        self.report_generation = GeracaoRelatorios(self.sales_recording.obter_resumo_vendas(), self.inventory_control.inventory)
        self.client_manager = ClientManager()

    def exibir_menu_principal(self):
        self.console.clear()
        self.console.print("[bold cyan]Sistema de Gestão de Produtos[/bold cyan]", justify="center")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Opção", justify="center")
        table.add_column("Descrição", justify="left")
        table.add_row("1", "Gestão de Produtos")
        table.add_row("2", "Gestão de Vendas")
        table.add_row("3", "Gestão de Inventário")
        table.add_row("4", "Gestão de Relatórios")
        table.add_row("5", "Gestão de Clientes")
        table.add_row("6", "Gestão de Funcionários")
        table.add_row("7", "Gestão de Gastos")
        table.add_row("0", "Sair")
        self.console.print(table)

    def obter_escolha_usuario(self):
        escolha = Prompt.ask("Por favor, selecione uma opção")
        return escolha

    def run(self):
        while True:
            self.exibir_menu_principal()
            escolha = self.obter_escolha_usuario()
            if escolha == "1":
                self.gestao_produtos()
            elif escolha == "2":
                self.gestao_vendas()
            elif escolha == "3":
                self.gestao_inventario()
            elif escolha == "4":
                self.gestao_relatorios()
            elif escolha == "5":
                self.gestao_clientes()
            elif escolha == "6":
                self.gestao_funcionarios()
            elif escolha == "7":
                self.gestao_gastos()
            elif escolha == "0":
                self.console.print("Saindo do sistema...")
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def gestao_produtos(self):
        while True:
            self.console.print("[bold cyan]Gestão de Produtos[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", justify="center")
            table.add_column("Descrição", justify="left")
            table.add_row("1", "Ver todos os produtos")
            table.add_row("2", "Cadastrar produto")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.ver_todos_produtos()
            elif escolha == "2":
                self.cadastrar_produto()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def ver_todos_produtos(self):
        produtos = self.inventory_control.obter_inventario()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="center")
        table.add_column("Nome", justify="center")
        table.add_column("Descrição", justify="center")
        table.add_column("Categoria", justify="center")
        table.add_column("Código de Barras", justify="center")
        table.add_column("Fornecedor", justify="center")
        table.add_column("Preço", justify="center")
        table.add_column("Quantidade", justify="center")
        table.add_column("Local de Armazenamento", justify="center")
        table.add_column("Data de Vencimento", justify="center")

        for produto in produtos:
            table.add_row(
                str(produto[0]), produto[1], produto[2], produto[3], produto[4], produto[5],
                str(produto[6]), str(produto[7]), produto[8], produto[9]
            )
        self.console.print(table)

    def gestao_vendas(self):
        while True:
            self.console.print("[bold cyan]Gestão de Vendas[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", justify="center")
            table.add_column("Descrição", justify="left")
            table.add_row("1", "Registrar uma venda")
            table.add_row("2", "Ver histórico de compras")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.registrar_venda()
            elif escolha == "2":
                self.ver_historico_compras()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def gestao_inventario(self):
        while True:
            self.console.print("[bold cyan]Gestão de Inventário[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", justify="center")
            table.add_column("Descrição", justify="left")
            table.add_row("1", "Gerenciar inventário")
            table.add_row("2", "Ver movimentações")
            table.add_row("3", "Alertas de estoque")
            table.add_row("4", "Alertas de vencimento")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.gerenciar_inventario()
            elif escolha == "2":
                self.ver_movimentacoes()
            elif escolha == "3":
                self.alertas_estoque()
            elif escolha == "4":
                self.alertas_vencimento()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def gestao_relatorios(self):
        while True:
            self.console.print("[bold cyan]Gestão de Relatórios[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", justify="center")
            table.add_column("Descrição", justify="left")
            table.add_row("1", "Gerar relatórios")
            table.add_row("2", "Exportar dados para CSV")
            table.add_row("3", "Exportar relatório fiscal para PDF")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.gerar_relatorios()
            elif escolha == "2":
                self.exportar_dados_para_csv()
            elif escolha == "3":
                self.exportar_relatorio_fiscal_para_pdf()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def gestao_clientes(self):
        while True:
            self.console.print("[bold cyan]Gestão de Clientes[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add.column("Descrição", justify="left")
            table.add_row("1", "Adicionar cliente")
            table.add_row("2", "Ver todos os clientes")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.adicionar_cliente()
            elif escolha == "2":
                self.ver_todos_clientes()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def gestao_funcionarios(self):
        while True:
            self.console.print("[bold cyan]Gestão de Funcionários[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Opção", justify="center")
            table.add_column("Descrição", justify="left")
            table.add_row("1", "Registrar horário")
            table.add_row("2", "Definir meta de vendas")
            table.add_row("3", "Ver horários")
            table.add_row("4", "Ver metas")
            table.add_row("5", "Ver atividades")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.registrar_horario()
            elif escolha == "2":
                self.definir_meta_vendas()
            elif escolha == "3":
                self.ver_horarios()
            elif escolha == "4":
                self.ver_metas()
            elif escolha == "5":
                self.ver_atividades()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def gestao_gastos(self):
        while True:
            self.console.print("[bold cyan]Gestão de Gastos[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add.column("Descrição", justify="left")
            table.add_row("1", "Registrar gasto")
            table.add_row("2", "Registrar salário")
            table.add_row("3", "Ver gastos")
            table.add_row("4", "Ver salários")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.registrar_gasto()
            elif escolha == "2":
                self.registrar_salario()
            elif escolha == "3":
                self.ver_gastos()
            elif escolha == "4":
                self.ver_salarios()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def registrar_gasto(self):
        descricao = Prompt.ask("Digite a descrição do gasto")
        valor = float(Prompt.ask("Digite o valor do gasto"))
        data = Prompt.ask("Digite a data do gasto (YYYY-MM-DD)")
        self.expenses_manager.registrar_gasto(descricao, valor, data)
        self.console.print(f"Gasto registrado: {descricao}, Valor: {valor}, Data: {data}")
        logging.info(f"Gasto registrado: Descrição {descricao}, Valor {valor}, Data {data}")

    def registrar_salario(self):
        funcionario = Prompt.ask("Digite o nome do funcionário")
        valor = float(Prompt.ask("Digite o valor do salário"))
        data = Prompt.ask("Digite a data do salário (YYYY-MM-DD)")
        self.expenses_manager.registrar_salario(funcionario, valor, data)
        self.console.print(f"Salário registrado: {funcionario}, Valor: {valor}, Data: {data}")
        logging.info(f"Salário registrado: Funcionário {funcionario}, Valor {valor}, Data {data}")

    def ver_gastos(self):
        gastos = self.expenses_manager.obter_gastos()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="center")
        table.add.column("Descrição", justify="center")
        table.add.column("Valor", justify="center")
        table.add.column("Data", justify="center")
        for gasto in gastos:
            table.add_row(str(gasto[0]), gasto[1], str(gasto[2]), gasto[3])
        self.console.print(table)

    def ver_salarios(self):
        salarios = self.expenses_manager.obter_salarios()
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("ID", justify="center")
        table.add.column("Funcionário", justify="center")
        table.add.column("Valor", justify="center")
        table.add.column("Data", justify="center")
        for salario in salarios:
            table.add_row(str(salario[0]), salario[1], str(salario[2]), salario[3])
        self.console.print(table)

    def cadastrar_produto(self):
        nome = Prompt.ask("Digite o nome do produto")
        descricao = Prompt.ask("Digite a descrição do produto")
        categoria = Prompt.ask("Digite a categoria do produto")
        codigo_barras = Prompt.ask("Digite o código de barras do produto")
        fornecedor = Prompt.ask("Digite o fornecedor do produto")
        preco = float(Prompt.ask("Digite o preço do produto"))
        quantidade = int(Prompt.ask("Digite a quantidade do produto"))
        local_armazenamento = Prompt.ask("Digite o local de armazenamento do produto")
        data_vencimento = Prompt.ask("Digite a data de vencimento do produto (YYYY-MM-DD)")
        self.inventory_control.cadastrar_produto(nome, descricao, categoria, codigo_barras, fornecedor, preco, quantidade, local_armazenamento, data_vencimento)
        self.console.print(f"Produto '{nome}' cadastrado com sucesso.")
        logging.info(f"Produto cadastrado: {nome}, Descrição: {descricao}, Categoria: {categoria}, Código de Barras: {codigo_barras}, Fornecedor: {fornecedor}, Preço: {preco}, Quantidade: {quantidade}, Local de Armazenamento: {local_armazenamento}, Data de Vencimento: {data_vencimento}")
        
        # Gerar QR codes para cada unidade do produto
        for i in range(quantidade):
            data = f"Nome: {nome}\nDescrição: {descricao}\nPreço: {preco}"
            filename = f"{nome}_{i+1}"
            self.barcode_reader.generate_qrcode(data, filename)
            self.console.print(f"QR Code gerado e salvo como qrcode/{filename}.png")
            logging.info(f"QR Code gerado para o produto: {nome}, Unidade: {i+1}")

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
        local_armazenamento = Prompt.ask("Digite o local de armazenamento")
        acao = Prompt.ask("Digite a ação (1: adicionar, 2: remover, 3: atualizar, 4: verificar)")
        if acao == "1":
            quantidade = int(Prompt.ask("Digite a quantidade a adicionar"))
            self.inventory_control.add_product(id_produto, quantidade, local_armazenamento)
            self.console.print(f"Adicionado {quantidade} unidades do produto ID {id_produto} ao inventário no local {local_armazenamento}.")
            logging.info(f"Adicionado {quantidade} unidades do produto ID {id_produto} ao inventário no local {local_armazenamento}.")
        elif acao == "2":
            quantidade = int(Prompt.ask("Digite a quantidade a remover"))
            self.inventory_control.remove_product(id_produto, quantidade, local_armazenamento)
            self.console.print(f"Removido {quantidade} unidades do produto ID {id_produto} do inventário no local {local_armazenamento}.")
            logging.info(f"Removido {quantidade} unidades do produto ID {id_produto} do inventário no local {local_armazenamento}.")
        elif acao == "3":
            quantidade = int(Prompt.ask("Digite a nova quantidade"))
            self.inventory_control.update_quantity(id_produto, quantidade, local_armazenamento)
            self.console.print(f"Quantidade do produto ID {id_produto} atualizada para {quantidade} no local {local_armazenamento}.")
            logging.info(f"Quantidade do produto ID {id_produto} atualizada para {quantidade} no local {local_armazenamento}.")
        elif acao == "4":
            estoque = self.inventory_control.check_stock(id_produto, local_armazenamento)
            self.console.print(f"O produto ID {id_produto} tem {estoque} unidades em estoque no local {local_armazenamento}.")
            logging.info(f"O produto ID {id_produto} tem {estoque} unidades em estoque no local {local_armazenamento}.")
            acao_verificar = Prompt.ask("Digite a ação (1: sair, 2: atualizar)")
            if acao_verificar == "2":
                self.gerenciar_inventario()
        else:
            self.console.print("[bold red]Ação inválida, por favor, tente novamente.[/bold red]")

    def registrar_venda(self):
        codigo_barras = Prompt.ask("Digite o código de barras do produto")
        quantidade = int(Prompt.ask("Digite a quantidade"))
        preco_total = float(Prompt.ask("Digite o preço total"))
        forma_pagamento = Prompt.ask("Digite a forma de pagamento")
        desconto = float(Prompt.ask("Digite o desconto"))
        nome_cliente = Prompt.ask("Digite o nome do cliente")
        id_venda = self.sales_manager.registrar_venda(codigo_barras, quantidade, preco_total, forma_pagamento, desconto, nome_cliente)
        self.console.print(f"Venda registrada com sucesso. ID da venda: {id_venda}")
        logging.info(f"Venda registrada: Código de Barras: {codigo_barras}, Quantidade: {quantidade}, Preço Total: {preco_total}, Forma de Pagamento: {forma_pagamento}, Desconto: {desconto}, Nome do Cliente: {nome_cliente}")
        self.sales_manager.emitir_recibo(id_venda)
        self.sales_manager.emitir_nota_fiscal(id_venda)

    def gerar_relatorios(self):
        tipo_relatorio = Prompt.ask("Digite o tipo de relatório (1: vendas, 2: inventário, 3: mais vendidos, 4: menos vendidos, 5: rentabilidade, 6: KPIs, 7: gráficos, 8: preditivo, 9: sazonalidade, 10: auditoria, 11: comparação)")
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
        elif tipo_relatorio == "4":
            relatorio = self.report_generation.produtos_menos_vendidos()
            self.console.print(f"Relatório dos produtos menos vendidos: {relatorio}")
            logging.info("Relatório dos produtos menos vendidos gerado")
        elif tipo_relatorio == "5":
            relatorio = self.report_generation.analise_rentabilidade()
            self.console.print(f"Análise de rentabilidade: {relatorio}")
            logging.info("Análise de rentabilidade gerada")
        elif tipo_relatorio == "6":
            kpis = self.report_generation.gerar_relatorio_kpis()
            self.console.print(f"KPIs de desempenho: {kpis}")
            logging.info("Relatório de KPIs gerado")
        elif tipo_relatorio == "7":
            self.report_generation.gerar_graficos_faturamento_fluxo_caixa()
            self.console.print("Gráficos de faturamento e fluxo de caixa gerados: gráficos/faturamento_diario.png")
            logging.info("Gráficos de faturamento e fluxo de caixa gerados")
        elif tipo_relatorio == "8":
            self.report_generation.gerar_relatorios_preditivos()
            self.console.print("Relatórios preditivos gerados: gráficos/previsao_demanda.png")
            logging.info("Relatórios preditivos gerados")
        elif tipo_relatorio == "9":
            self.report_generation.gerar_relatorios_sazonalidade()
            self.console.print("Relatórios de sazonalidade gerados: gráficos/sazonalidade_vendas.png")
            logging.info("Relatórios de sazonalidade gerados")
        elif tipo_relatorio == "10":
            movimentacoes, vendas = self.report_generation.auditoria_movimentacao_estoque_vendas()
            self.console.print(f"Auditoria de movimentação de estoque: {movimentacoes}")
            self.console.print(f"Auditoria de vendas: {vendas}")
            logging.info("Auditoria de movimentação de estoque e vendas gerada")
        elif tipo_relatorio == "11":
            periodo1_inicio = Prompt.ask("Digite a data de início do período 1 (YYYY-MM-DD)")
            periodo1_fim = Prompt.ask("Digite a data de fim do período 1 (YYYY-MM-DD)")
            periodo2_inicio = Prompt.ask("Digite a data de início do período 2 (YYYY-MM-DD)")
            periodo2_fim = Prompt.ask("Digite a data de fim do período 2 (YYYY-MM-DD)")
            comparacao = self.report_generation.comparacao_periodos(periodo1_inicio, periodo1_fim, periodo2_inicio, periodo2_fim)
            self.console.print(f"Comparação entre períodos: {comparacao}")
            logging.info("Comparação entre períodos gerada")
        else:
            self.console.print("[bold red]Tipo de relatório inválido, por favor, tente novamente.[/bold red]")

    def exportar_dados_para_csv(self):
        nome_grupo = Prompt.ask("Digite o nome do grupo para exportação CSV")
        self.product_registration.exportar_dados(f"{nome_grupo}_produtos.csv")
        self.sales_recording.exportar_vendas_para_csv(f"{nome_grupo}_vendas.csv")
        self.report_generation.exportar_comentarios_para_csv(f"{nome_grupo}_comentarios.csv")
        self.console.print(f"Dados exportados para {nome_grupo}_produtos.csv, {nome_grupo}_vendas.csv e {nome_grupo}_comentarios.csv")
        logging.info(f"Dados exportados para {nome_grupo}_produtos.csv, {nome_grupo}_vendas.csv e {nome_grupo}_comentarios.csv")

    def exportar_relatorio_fiscal_para_pdf(self):
        filename = Prompt.ask("Digite o nome do arquivo PDF")
        self.report_generation.exportar_relatorio_fiscal_para_pdf(f"{filename}.pdf")
        self.console.print(f"Relatório fiscal exportado para {filename}.pdf")
        logging.info(f"Relatório fiscal exportado para {filename}.pdf")

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
        produtos = self.product_registration.obter_produtos()
        notificacoes = self.product_registration.obter_notificacoes()
        self.console.print("[bold cyan]Dashboard de Análise[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("Nome", justify="center")
        table.add.column("Categoria", justify="center")
        table.add.column("Preço de Custo", justify="center")
        table.add.column("Preço de Venda", justify="center")
        table.add.column("Quantidade", justify="center")
        for produto in produtos:
            table.add_row(*map(str, produto))
        self.console.print(table)
        if notificacoes:
            self.console.print("[bold red]Notificações:[/bold red]")
            for notificacao in notificacoes:
                self.console.print(notificacao)
        self.gerar_graficos_dashboard()

    def gerar_graficos_dashboard(self):
        # Exemplo de gráfico usando matplotlib
        produtos = self.product_registration.obter_produtos()
        nomes = [produto[0] for produto in produtos]
        quantidades = [produto[4] for produto in produtos]
        plt.bar(nomes, quantidades)
        plt.xlabel('Produtos')
        plt.ylabel('Quantidade')
        plt.title('Quantidade de Produtos em Estoque')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('graficos/dashboard_estoque.png')
        plt.show()

    def pesquisar_produto(self):
        nome_produto = Prompt.ask("Digite o nome do produto")
        produtos = self.product_registration.pesquisar_produto(nome_produto)
        if produtos:
            table = Table(show_header=True, header_style="bold magenta")
            table.add.column("Nome", justify="center")
            table.add.column("Categoria", justify="center")
            table.add.column("Preço de Custo", justify="center")
            table.add.column("Preço de Venda", justify="center")
            table.add.column("Quantidade", justify="center")
            for produto in produtos:
                table.add_row(*map(str, produto))
            self.console.print(table)
        else:
            self.console.print("[bold red]Produto não encontrado.[/bold red]")

    def gerar_qrcodes(self, nome, categoria, preco_custo, preco_venda, quantidade):
        import qrcode
        if not os.path.exists('qrcode'):
            os.makedirs('qrcode')
        data = f"Nome: {nome}\nCategoria: {categoria}\nPreço de Custo: {preco_custo}\nPreço de Venda: {preco_venda}\nQuantidade: {quantidade}"
        for i in range(quantidade):
            img = qrcode.make(data)
            img.save(f"qrcode/{nome}_{i+1}.png")
        self.console.print(f"{quantidade} QR Codes gerados e salvos na pasta qrcode")
        logging.info(f"{quantidade} QR Codes gerados para o produto: {nome}")

    def gerenciar_clientes(self):
        while True:
            self.console.print("[bold cyan]Gerenciamento de Clientes[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add.column("Opção", justify="center")
            table.add.column("Descrição", justify="left")
            table.add_row("1", "Adicionar cliente")
            table.add_row("2", "Ver todos os clientes")
            table.add_row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.adicionar_cliente()
            elif escolha == "2":
                self.ver_todos_clientes()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")

    def adicionar_cliente(self):
        nome = Prompt.ask("Digite o nome do cliente")
        telefone = Prompt.ask("Digite o telefone do cliente")
        email = Prompt.ask("Digite o email do cliente")
        self.client_manager.adicionar_cliente(nome, telefone, email)
        self.console.print(f"Cliente '{nome}' adicionado com sucesso.")
        logging.info(f"Cliente adicionado: {nome}, Telefone: {telefone}, Email: {email}")

    def ver_todos_clientes(self):
        clientes = self.client_manager.obter_clientes()
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("Nome", justify="center")
        table.add.column("Telefone", justify="center")
        table.add.column("Email", justify="center")
        for cliente in clientes:
            table.add_row(cliente['nome'], cliente['telefone'], cliente['email'])
        self.console.print(table)

    def ver_atividades(self):
        atividades = self.user_manager.obter_atividades()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="center")
        table.add.column("Usuário", justify="center")
        table.add.column("Ação", justify="center")
        table.add.column("Timestamp", justify="center")
        for atividade in atividades:
            table.add_row(str(atividade[0]), atividade[1], atividade[2], atividade[3])
        self.console.print(table)

    def registrar_cliente(self):
        nome = Prompt.ask("Digite o nome do cliente")
        email = Prompt.ask("Digite o email do cliente")
        telefone = Prompt.ask("Digite o telefone do cliente")
        id_cliente = self.sales_manager.registrar_cliente(nome, email, telefone)
        self.console.print(f"Cliente registrado com sucesso! ID Cliente: {id_cliente}")
        logging.info(f"Cliente registrado: Nome: {nome}, Email: {email}, Telefone: {telefone}")

    def ver_historico_compras(self):
        id_cliente = Prompt.ask("Digite o ID do cliente")
        historico = self.sales_manager.obter_historico_compras(id_cliente)
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("ID Venda", justify="center")
        table.add.column("ID Produto", justify="center")
        table.add.column("Quantidade", justify="center")
        table.add.column("Preço Total", justify="center")
        table.add.column("Forma de Pagamento", justify="center")
        table.add.column("Desconto", justify="center")
        table.add.column("Data", justify="center")
        for venda in historico:
            table.add_row(str(venda[0]), str(venda[1]), str(venda[2]), str(venda[3]), venda[4], str(venda[5]), venda[7])
        self.console.print(table)

    def ver_movimentacoes(self):
        movimentacoes = self.inventory_control.obter_movimentacoes()
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("ID", justify="center")
        table.add.column("ID Produto", justify="center")
        table.add.column("Tipo", justify="center")
        table.add.column("Quantidade", justify="center")
        table.add.column("Data", justify="center")
        table.add.column("Local de Armazenamento", justify="center")
        for movimentacao in movimentacoes:
            table.add.row(str(movimentacao[0]), str(movimentacao[1]), movimentacao[2], str(movimentacao[3]), movimentacao[4], movimentacao[5])
        self.console.print(table)

    def alertas_estoque(self):
        threshold = int(Prompt.ask("Digite o limite de estoque mínimo"))
        low_stock_items = self.inventory_control.notify_low_stock(threshold)
        if low_stock_items:
            self.console.print("[bold red]Produtos com estoque baixo:[/bold red]")
            for item in low_stock_items:
                self.console.print(f"Produto: {item[0]}, Quantidade: {item[1]}")
        else:
            self.console.print("[bold green]Nenhum produto com estoque baixo.[/bold green]")

    def alertas_vencimento(self):
        days = int(Prompt.ask("Digite o número de dias para alerta de vencimento"))
        expiring_products = self.inventory_control.notify_expiring_products(days)
        if expiring_products:
            self.console.print("[bold red]Produtos próximos do vencimento:[/bold red]")
            for item in expiring_products:
                self.console.print(f"Produto: {item[0]}, Data de Vencimento: {item[1]}")
        else:
            self.console.print("[bold green]Nenhum produto próximo do vencimento.[/bold green]")

    def registrar_horario(self):
        usuario = Prompt.ask("Digite o nome do usuário")
        entrada = Prompt.ask("Digite a hora de entrada (YYYY-MM-DD HH:MM:SS)")
        saida = Prompt.ask("Digite a hora de saída (YYYY-MM-DD HH:MM:SS)")
        self.user_manager.registrar_horario(usuario, entrada, saida)
        self.console.print(f"Horário registrado para o usuário {usuario}.")
        logging.info(f"Horário registrado: Usuário {usuario}, Entrada {entrada}, Saída {saida}")

    def definir_meta_vendas(self):
        usuario = Prompt.ask("Digite o nome do usuário")
        meta_vendas = int(Prompt.ask("Digite a meta de vendas"))
        self.user_manager.definir_meta_vendas(usuario, meta_vendas)
        self.console.print(f"Meta de vendas definida para o usuário {usuario}.")
        logging.info(f"Meta de vendas definida: Usuário {usuario}, Meta {meta_vendas}")

    def ver_horarios(self):
        horarios = self.user_manager.obter_horarios()
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("ID", justify="center")
        table.add.column("Usuário", justify="center")
        table.add.column("Entrada", justify="center")
        table.add.column("Saída", justify="center")
        for horario in horarios:
            table.add.row(str(horario[0]), horario[1], horario[2], horario[3])
        self.console.print(table)

    def ver_metas(self):
        metas = self.user_manager.obter_metas()
        table = Table(show_header=True, header_style="bold magenta")
        table.add.column("ID", justify="center")
        table.add.column("Usuário", justify="center")
        table.add.column("Meta de Vendas", justify="center")
        for meta in metas:
            table.add.row(str(meta[0]), meta[1], str(meta[2]))
        self.console.print(table)

    def gerenciar_funcionarios(self):
        while True:
            self.console.print("[bold cyan]Gerenciamento de Funcionários[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add.column("Opção", justify="center")
            table.add.column("Descrição", justify="left")
            table.add.row("1", "Registrar horário")
            table.add.row("2", "Definir meta de vendas")
            table.add.row("3", "Ver horários")
            table.add.row("4", "Ver metas")
            table.add.row("5", "Ver atividades")
            table.add.row("0", "Voltar")
            self.console.print(table)
            escolha = Prompt.ask("Por favor, selecione uma opção")
            if escolha == "1":
                self.registrar_horario()
            elif escolha == "2":
                self.definir_meta_vendas()
            elif escolha == "3":
                self.ver_horarios()
            elif escolha == "4":
                self.ver_metas()
            elif escolha == "5":
                self.ver_atividades()
            elif escolha == "0":
                break
            else:
                self.console.print("[bold red]Opção inválida, por favor, tente novamente.[/bold red]")