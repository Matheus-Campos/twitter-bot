# -*- coding: utf-8 -*-
import csv
import sys
from mysql import connector


STATES = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS':  'Mato Grosso do Sul', 'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'}


def getState(place, data):
    """Analisa se place está no dicionário STATES"""
    for k, v in STATES.items():
        data['state'] = v if place.lower() == k.lower() or place.lower() == v.lower() else ''


def getLocal(local):
    """Retorna a quantidade de elementos numa lista de lugares
     e a própria lista."""
    if local.find(','):
        local = local.split(',')
        try:
            float(local[0])  # checa se a localização é uma coordenada
            return len(local), local
        except ValueError:
            pass
    elif local.find('-'):
        local = local.split('-')
    elif local.find('/'):
        local = local.split('/')
    else:
        # presume-se que a localização é nula
        return 0, []
    return len(local), local


def correctSentimentValue(sentiment):
    """Retorna o sentimento correto, evitando
        erros como o sentimento sair do alcance entre -1 e 1."""
    sentiment = float(sentiment)
    polarity = getSentimentPolarity(sentiment)
    if -1 <= sentiment <= 1:
        sentiment = str(sentiment)
    elif sentiment < 0:
        sentiment = '-0.' + str(abs(sentiment))
    else:
        sentiment = '0.' + str(sentiment)
    return sentiment, polarity


def getSentimentPolarity(sentiment):
    if sentiment > 0:
        return 'POSITIVO'
    elif sentiment < 0:
        return 'NEGATIVO'
    else:
        return 'NEUTRO'

def getConnection():
    return connector.Connect(host='127.0.0.1', database='fonte_sentimento_stf', user='root', password='')


def main(input_file, output):
    # Abre o arquivo de saída para escrita:
    with open('tweets_analise/' + input_file, 'r') as file_read, open(output, 'w') as file_write:

        # Define o leitor CSV do arquivo:
        reader = csv.reader(file_read, delimiter=';')
        # header = next(reader) # passa a primeira linha (cabealho)

        # Define o escritor CSV do arquivo:
        fieldnames = ['date', 'ano', 'mes', 'dia', 'city', 'state', 'country', 'user id', 'username', 'user nickname','tweet', 'sentiment', 'verified']
        writer = csv.DictWriter(file_write, fieldnames=fieldnames, delimiter='\t')  # inicia como DictWriter para permitir a escrita por dicionário
        writer.writeheader()  # escreve o cabeçalho no arquivo

        # Percorre as linhas do arquivo de entrada:
        for row in reader:
            # ignora as linhas bugadas (temporariamente)
            if len(row[11]) > 255:
                continue
            # separa os dados do CSV de leitura
            date, time = row[10].split(' ')
            number_location, place = getLocal(row[7])  # retorna o número de itens na lista de locais e a lista de locais
            place = [p.replace('Brazil', 'Brasil') for p in place] # substitui Brazil por Brasil
            user = [row[1], row[2], row[3]]
            tweet = row[11]
            verified = row[4]
            sentiment, polarity = correctSentimentValue(row[-1])
            ano, mes, dia = date.split('-')

            # coloca os dados organizados num dicionário
            data = {'date': date, 'ano': ano, 'mes': mes, 'dia': dia, 'state': '', 'country': 'Brazil', 'username': user[1], 'user id': user[0], 'user nickname': user[2], 'tweet': tweet, 'sentiment': sentiment, 'verified': verified}

            # quebra a localização do tweet
            if number_location == 0:
                data['state'] = ''
            elif number_location == 1:
                getState(place[-1], data)
            elif number_location >= 2:
                getState(place[-2], data)

            # escreve no arquivo de escrita
            writer.writerow(data)

            db_conn = getConnection()
            cursor = db_conn.cursor()

            insere_sentimento = ('INSERT INTO sentimento (id_sentimento, polaridade) VALUES (%s, %s)')
            sentimento = (sentiment, polarity)
            cursor.execute(insere_sentimento, params=sentimento)
            db_conn.commit()
            cursor.close()
            db_conn.close()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        try:
            main(sys.argv[1], sys.argv[2])
        except KeyboardInterrupt:
            exit(0)
    else:
        print('Usage: python3 lerplanilhas.py <arq_entrada> <arq_saida>')
        exit(1)
