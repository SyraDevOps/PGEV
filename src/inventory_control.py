from rich.console import Console
from rich.table import Table

class InventoryControl:
    def __init__(self):
        self.console = Console()
        self.inventory = {}

    def add_product(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id] += quantity
        else:
            self.inventory[product_id] = quantity

    def remove_product(self, product_id, quantity):
        if product_id in self.inventory:
            if self.inventory[product_id] >= quantity:
                self.inventory[product_id] -= quantity
                if self.inventory[product_id] == 0:
                    del self.inventory[product_id]
            else:
                raise ValueError("Estoque insuficiente para remover.")
        else:
            raise ValueError("Produto não encontrado no inventário.")

    def update_quantity(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id] = quantity
        else:
            raise ValueError("Produto não encontrado no inventário.")

    def check_stock(self, product_id):
        stock = self.inventory.get(product_id, 0)
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID do Produto", justify="center")
        table.add_column("Quantidade em Estoque", justify="center")
        table.add_row(str(product_id), str(stock))
        self.console.print(table)
        return stock

    def notify_low_stock(self, threshold):
        low_stock_items = {product_id: qty for product_id, qty in self.inventory.items() if qty < threshold}
        return low_stock_items