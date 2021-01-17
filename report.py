import csv
import datetime

operacoes = []
cal_mensal = {}
carteira = {}

def comprar(ticket, quantidade, preco_medio):
    if ticket not in carteira:
        carteira[ticket] = {"quantidade": 0, "preco_medio": 0}

    estado_antes = carteira[ticket]
    valor_total_antes = estado_antes["preco_medio"] * estado_antes["quantidade"]
    quantidade_depois = estado_antes["quantidade"] + quantidade
    preco_medio_depois = (valor_total_antes + (quantidade * preco_medio)) / quantidade_depois
    carteira[ticket] = {"quantidade": quantidade_depois, "preco_medio": preco_medio_depois}

    return carteira[ticket]

def vender(ticket, quantidade, preco_medio):
    carteira[ticket]["quantidade"] -= quantidade
    lucro = (quantidade * preco_medio) - (quantidade * carteira[ticket]["preco_medio"])

    if carteira[ticket]["quantidade"] == 0:
        carteira[ticket]["preco_medio"] = 0

    return lucro, carteira[ticket]

with open("dataminer.csv", newline="") as csvfile:
    operacoes_reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
    for linha in operacoes_reader:
        operacoes.append({
            "ticket": linha[0],
            "operacao": linha[1],
            "data": datetime.datetime.strptime(linha[2], "%d/%m/%Y").date(),
            "preco_medio": float(linha[3].replace("R$", "").replace(",", ".")),
            "quantidade": int(linha[4])
        })

operacoes.sort(key=lambda op: op["data"])

for op in operacoes:
    posicao_carteira = {}
    mes_ano = op["data"].strftime("%m/%Y")
    if mes_ano not in cal_mensal:
        cal_mensal[mes_ano] = {"lucro": 0}

    if op["operacao"] == "COMPRA":
        posicao_carteira = comprar(op["ticket"], op["quantidade"], op["preco_medio"])
        print(f'[{mes_ano}] Comprando {op["ticket"]} no dia {op["data"]} com preço médio de R${op["preco_medio"]}.')
    else:
        lucro, posicao_carteira = vender(op["ticket"], op["quantidade"], op["preco_medio"])
        cal_mensal[mes_ano]["lucro"] += lucro
        print(f'[{mes_ano}] Vendendo {op["ticket"]} no dia {op["data"]} com preço médio de R${op["preco_medio"]} e lucro de R${lucro}')

    print(f'[{mes_ano}] Carteira possui {posicao_carteira["quantidade"]} cotas de {op["ticket"]} comprados ao preço médio de {posicao_carteira["preco_medio"]}')
    print("--------------")


# Calcula o IR
saldo_negativo = 0
for mes_ano in cal_mensal:
    if cal_mensal[mes_ano]["lucro"] < 0:
        saldo_negativo -= cal_mensal[mes_ano]["lucro"]
    else:
        saldo_atual = (cal_mensal[mes_ano]["lucro"] - saldo_negativo)

        if saldo_atual < 0:
            saldo_negativo -= cal_mensal[mes_ano]["lucro"]
        else:
            cal_mensal[mes_ano]["ir"] = saldo_atual * 0.2

    if saldo_negativo != 0:
        cal_mensal[mes_ano]["saldo_negativo"] = saldo_negativo

for mes_ano in cal_mensal:
    print(mes_ano, cal_mensal[mes_ano])