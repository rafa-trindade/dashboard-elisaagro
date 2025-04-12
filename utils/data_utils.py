mapa_meses = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

meses_mapa = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
}

def anos_disponiveis(df):
    return sorted(df['data'].dt.year.unique())

def atualiza_meses_disponiveis(ano, df):
    meses_numeros = df[df['data'].dt.year == ano]['data'].dt.month.unique()
    meses_nomes = [mapa_meses[num] for num in sorted(meses_numeros)]
    return meses_nomes
