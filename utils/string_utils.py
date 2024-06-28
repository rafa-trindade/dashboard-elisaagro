
lista_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

# Formata um número para o formato de moeda brasileira (R$)
def formata_para_brl(valor):
    try:
        valor = float(valor)
    except ValueError:
        return valor
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

#Converte um valor formatado em string como moeda brasileira para float
def brl_para_float(valor):
    try:
        valor = str(valor)
    except ValueError:
        return valor
    return float(valor.replace('R$', '').replace('.', '').replace(',', '.'))

# Função de formatação de moeda
def format_currency(value):
    return "R$ {:,.2f}".format(value).replace(',', 'v').replace('.', ',').replace('v', '.')


