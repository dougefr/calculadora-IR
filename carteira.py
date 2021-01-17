class Carteira:
    carteira = {}

    def comprar(self, ticket, quantidade, preco_medio):
        if ticket not in self.carteira:
            self.carteira[ticket] = {"quantidade": 0, "preco_medio": 0}

        estado_antes = self.carteira[ticket]
        valor_total_antes = estado_antes["preco_medio"] * estado_antes["quantidade"]
        quantidade_depois = estado_antes["quantidade"] + quantidade
        preco_medio_depois = (valor_total_antes + (quantidade * preco_medio)) / quantidade_depois
        self.carteira[ticket] = {"quantidade": quantidade_depois, "preco_medio": preco_medio_depois}

        return self.carteira[ticket]

    def vender(self, ticket, quantidade, preco_medio):
        self.carteira[ticket]["quantidade"] -= quantidade
        lucro = (quantidade * preco_medio) - (quantidade * self.carteira[ticket]["preco_medio"])

        if self.carteira[ticket]["quantidade"] == 0:
            self.carteira[ticket]["preco_medio"] = 0

        return lucro, self.carteira[ticket]