
lista_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

def formata_para_brl(valor):
    try:
        valor = float(valor)
    except ValueError:
        return valor
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def brl_para_float(valor):
    try:
        valor = str(valor)
    except ValueError:
        return valor
    return float(valor.replace('R$', '').replace('.', '').replace(',', '.'))

def format_currency(value):
    return "R$ {:,.2f}".format(value).replace(',', 'v').replace('.', ',').replace('v', '.')


