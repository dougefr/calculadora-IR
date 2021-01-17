import csv
import datetime
from carteira import Carteira

operacoes = []
cal_mensal = {}
carteira = Carteira()

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
        posicao_carteira = carteira.comprar(op["ticket"], op["quantidade"], op["preco_medio"])
        print(f'[{mes_ano}] Comprando {op["ticket"]} no dia {op["data"]} com preço médio de R${op["preco_medio"]}.')
    else:
        lucro, posicao_carteira = carteira.vender(op["ticket"], op["quantidade"], op["preco_medio"])
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
            saldo_negativo = 0

    if saldo_negativo != 0:
        cal_mensal[mes_ano]["saldo_negativo"] = saldo_negativo

for mes_ano in cal_mensal:
    print(mes_ano, cal_mensal[mes_ano])