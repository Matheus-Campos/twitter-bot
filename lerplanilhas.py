# -*- coding: utf-8 -*-
import csv
import sys
from mysql import connector


STATES = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS':  'Mato Grosso do Sul', 'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'}
STATES2 = {'AC': '1743', 'AL': '1744', 'AP': '1745', 'AM': '1746', 'BA': '1747', 'CE': '1748', 'DF': '1749', 'ES': '1750', 'GO': '1751', 'MA': '1752', 'MT': '1753', 'MS':  '1754', 'MG': '1755', 'PA': '1756', 'PB': '1757', 'PR': '1758', 'PE': '1759', 'PI': '1760', 'RJ': '1761', 'RN': '1762', 'RS': '1763', 'RO': '1764', 'RR': '1765', 'SC': '1766', 'SP': '1767', 'SE': '1768', 'TO': '1769', 'ND': '1770'}


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


def executeQuery(statement, values, local=None):
    db_conn = getConnection()
    cursor = db_conn.cursor()
    try:
        cursor.execute(statement, values)
    except:
        if local is not None:
            cursor.execute("SELECT id FROM local WHERE state = {}".format(values[1]))
            for row in cursor:
                print(row)
            cursor.close()
            db_conn.close()
            return int(id)
    id = cursor._last_insert_id
    db_conn.commit()
    cursor.close()
    db_conn.close()
    return id


def main(input_file, output):
    
    # Abre o arquivo de saída para escrita:
    with open('tweets_analise/' + input_file, 'r', encoding='UTF8') as file_read, open(output, 'w', encoding='UTF8') as file_write:
        # Define o leitor CSV do arquivo:
        reader = csv.reader(file_read, delimiter=';')
        
        # header = next(reader) # passa a primeira linha (cabealho)

        # Define o escritor CSV do arquivo:
        fieldnames = ['date', 'ano', 'mes', 'dia', 'city', 'state', 'country', 'user id', 'username', 'user nickname','text', 'sentiment', 'verified']
        writer = csv.DictWriter(file_write, fieldnames=fieldnames, delimiter='\t')  # inicia como DictWriter para permitir a escrita por dicionário
        writer.writeheader()  # escreve o cabeçalho no arquivo
        
        # Percorre as linhas do arquivo de entrada:
        print(reader)
        
        for row in reader:
            
            
            # ignora as linhas bugadas (temporariamente)
            if len(row[11]) > 255:
                continue
            # separa os dados do CSV de leitura
            date, time = row[10].split(' ')
            number_location, place = getLocal(row[7])  # retorna o número de itens na lista de locais e a lista de locais
            place = [p.replace('Brazil', 'Brasil') for p in place] # substitui Brazil por Brasil
            user = row[1:6]    
            user.extend(['pt'])
            text = row[11]
            sentiment, polarity = correctSentimentValue(row[-1]) # sentimento + polaridade
            ano, mes, dia = date.split('-')
            # retweeted = 1 if bool(row[-2]) == 'True' else 0  <----- não está sendo utilizado por causa do csv

            # coloca os dados organizados num dicionário
            data = {'date': date, 'ano': ano, 'mes': mes, 'dia': dia, 'state': '', 'country': 'Brasil', 'username': user[1], 'user id': user[0], 'user nickname': user[2], 'text': text, 'sentiment': sentiment, 'verified': row[4]}

            # quebra a localização do tweet
            if number_location == 0:
                data['state'] = ''
            elif number_location == 1:
                getState(place[-1], data)
            elif number_location >= 2:
                getState(place[-2], data)

            # cria uma lista de estados + siglas
            estados = list(STATES.values())
            estados.extend(list(STATES.keys()))
            estados.sort()
            
            for i in place :
                if i in estados:
                    if i=='Acre' or i=='AC' or i=='Rio Branco' : state = 'AC'
                    elif i=='Alagoas' or i=='AL' or i=='Maceió' or i =='Maceio' or i==' Maceió': state = 'AL'
                    elif i=='Amapá' or i=='AP' or i=='Macapá' : state = 'AP'
                    elif i=='Amazonas' or i=='AM' or i=='Manaus' or i==' Manaus': state = 'AM'
                    elif i=='Bahia' or i=='BA' or i == ' Bahia' : state = 'BA'
                    elif i=='Ceará' or i=='CE' or i=='Fortaleza' : state ='CE'
                    elif i=='Brasília' or i=='DF' or i=='Distrito Federal' or i=='Brasilia': state = 'DF'
                    elif i=='Espírito Santo' or i=='ES' or i=='Espirito Santo' : state = 'ES'
                    elif i=='Goiás' or i=='GO' or i=='Goias' : state = 'GO'
                    elif i=='Maranhão' or i=='Maranhao' or i=='MA' : state = 'MA'
                    elif i=='Mato Grosso' or i=='MT' or i==' Mato Grosso' or i=='Cuiabá': state = 'MT'
                    elif i=='Mato Grosso do Sul' or i=='MS' or i=='Campo Grande': state= 'MS'
                    elif i=='Minas Gerais' or i =='MG' or i=='minas' or i=='Belo Horizonte' : state= 'MG'
                    elif i=='Pará' or i=='PA' or i=='Belém' : state= 'PA'
                    elif i=='Paraíba' or i=='PB' or i=='Paraiba' or i=='João Pessoa': state='PB'
                    elif i=='Paraná' or i=='PR' or i=='Curitiba': state='PR'
                    elif i=='Pernambuco' or i=='PE' or i=='Recife' : state='PE'
                    elif i=='Piauí' or i=='PI' or i=='Teresina': state='PI'
                    elif i=='Rio de Janeiro' or i=='RJ' : state='RJ'
                    elif i=='Rio Grande do Norte' or i=='RN' or i=='Natal': state = 'RN'
                    elif i=='Rio Grande do Sul' or i=='Porto Alegre' or i=='RS' : state = 'RS'
                    elif i=='Rondônia' or i=='RO' or i=='Porto Velho': state = 'RO'
                    elif i=='Roraima' or i=='RR' or i =='Boa Vista': state = 'RR'
                    elif i=='Santa Catarina' or i=='SC' or i=='Florianópolis' : state ='SC'
                    elif i=='Sergipe' or i=='SE' or i=='Aracaju' : state ='SE'
                    elif i=='Tocantins' or i=='TO' or i=='Palmas' : state ='TO'
                    elif i=='São Paulo' or i=='SP' or i==' São Paulo' or i == 'São Paulo' or i=='Sao Paulo': state = 'SP'
                else: 
                    state='ND'

            idEstado = STATES2[state]
            # escreve no arquivo de escrita
            writer.writerow(data)

            ########################## INSERÇÕES NO BANCO DE DADOS #####################################

            sentiment = float(sentiment)
            if sentiment > 0:
                sentiment = 1
            elif sentiment < 0:
                sentiment = -1
            else:
                sentiment = 0

            insert_local = 'INSERT INTO local (pais, estado) VALUES (%s, %s)'
            local = (data['country'], 'Undefined')

            insert_user = 'INSERT INTO usuario (id_usuario, nome, apelido, verificado, qtd_seguidores, idioma, local_id_local) VALUES (%s,%s,%s,%s,%s,%s,%s)'

            insert_tweet = 'INSERT INTO tweet (id_tweet, usuario_id_usuario, data, texto, idioma,sentimento_id_sentimento,local_id_local) VALUES (%s, %s, %s, %s, %s,%s,%s)'
            tweet = (row[0], user[0], date, text, 'pt', sentiment, idEstado)

            insert_tweet_minister = 'INSERT INTO tweet_ministro VALUES (%s, %s)'
            id_minister = 11
            tweet_minister = (row[0], id_minister)


            try:
                print((state, idEstado))
                print("Insert Local")
                id_local = executeQuery(insert_local, local, True)
                print()

            except connector.IntegrityError as e:
                print('[LOCAL]', e.msg)

            user.extend([idEstado])

            boleano = user[3]
            if boleano == 'false':
                boleano = 0
            else:
                boleano = 1


            try:
                t1 = (user[0],user[1],user[2],boleano,user[4],user[5],user[6])
                print(t1)
                print("Insert User")
                executeQuery(insert_user, t1)
                #executeQuery(insert_user, tuple(user))
                print()
            except connector.IntegrityError as e:
                print('[USUARIO]', e.msg)
            
            
            #b = (id_local)
            #tweet = tweet + (b,)

            try:
                print(tweet)
                print("Insert Tweet")
                executeQuery(insert_tweet, tweet)
                print()
            except connector.IntegrityError as e:
                print('[TWEET]', e.msg)
                print()

            try:
                print(tweet_minister)
                print("Insert Tweet_ministro")
                executeQuery(insert_tweet_minister, tweet_minister)
                print()
            except connector.IntegrityError as e:
                print('[TWEET_MINISTER]', e.msg)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        try:
            main(sys.argv[1], sys.argv[2])
        except KeyboardInterrupt:
            exit(0)
    else:
        print('Usage: python3 lerplanilhas.py <arq_entrada> <arq_saida>')
        exit(1)
