#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import sys
from mysql import connector


STATES = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS':  'Mato Grosso do Sul', 'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'}
STATES_IDS = {'AC': '1', 'AL': '2', 'AP': '3', 'AM': '4', 'BA': '5', 'CE': '6', 'DF': '7', 'ES': '8', 'GO': '9', 'MA': '10', 'MT': '11', 'MS': '12', 'MG': '13', 'PA': '14', 'PB': '15', 'PR': '16', 'PE': '17', 'PI': '18', 'RJ': '19', 'RN': '20', 'RS': '21', 'RO': '22', 'RR': '23', 'SC': '24', 'SP': '25', 'SE': '26', 'TO': '27', 'ND': '28'}


def getLocal(local):
    """Retorna a própria lista dividida."""
    if local.find(','):
        local = local.split(',')
    elif local.find('-'):
        local = local.split('-')
    elif local.find('/'):
        local = local.split('/')
    return local


def getSentiment(sentiment):
    sentiment = float(sentiment)
    if sentiment > 0:
        return 1
    elif sentiment < 0:
        return -1
    else:
        return 0


def getConnection():
    return connector.Connect(host='127.0.0.1', database='fonte_sentimento_stf', user='root', password='')


def main(input_file):
    # Abre o arquivo de saída para escrita:
    with open('tweets_analise/' + input_file, 'r', encoding='UTF8') as file_read:
        # Define o leitor CSV do arquivo:
        reader = csv.reader(file_read, delimiter=';')
        curr_record = 0
        
        # Percorre as linhas do arquivo de entrada:
        for row in reader:
            # ignora as linhas bugadas (temporariamente)
            if len(row[11]) > 255:
                continue
            
            ############################ COLETA DE DADOS DO ARQUIVO ###############################

            date, time = row[10].split(' ')
            place = getLocal(row[7])  # retorna o número de itens na lista de locais e a lista de locais
            place = [p.replace('Brazil', 'Brasil') for p in place]  # substitui Brazil por Brasil

            # cria uma lista de estados + siglas
            estados = list(STATES.values())
            estados.extend(list(STATES.keys()))
            estados.sort()

            # checa se alguma palavra da localização se encaixa em algum estado brasileiro
            for i in place:
                if i in estados:
                    if i == 'Acre' or i == 'AC' or i == 'Rio Branco':
                        state = 'AC'
                        break
                    elif i == 'Alagoas' or i == 'AL' or i == 'Maceió' or i == 'Maceio' or i == ' Maceió':
                        state = 'AL'
                        break
                    elif i == 'Amapá' or i == 'AP' or i == 'Macapá':
                        state = 'AP'
                        break
                    elif i == 'Amazonas' or i == 'AM' or i == 'Manaus' or i == ' Manaus':
                        state = 'AM'
                        break
                    elif i == 'Bahia' or i == 'BA' or i == ' Bahia':
                        state = 'BA'
                        break
                    elif i == 'Ceará' or i == 'CE' or i == 'Fortaleza':
                        state = 'CE'
                        break
                    elif i == 'Brasília' or i == 'DF' or i == 'Distrito Federal' or i == 'Brasilia':
                        state = 'DF'
                        break
                    elif i == 'Espírito Santo' or i == 'ES' or i == 'Espirito Santo':
                        state = 'ES'
                        break
                    elif i == 'Goiás' or i == 'GO' or i == 'Goias':
                        state = 'GO'
                        break
                    elif i == 'Maranhão' or i == 'Maranhao' or i == 'MA':
                        state = 'MA'
                        break
                    elif i == 'Mato Grosso' or i == 'MT' or i == ' Mato Grosso' or i == 'Cuiabá':
                        state = 'MT'
                        break
                    elif i == 'Mato Grosso do Sul' or i == 'MS' or i == 'Campo Grande':
                        state = 'MS'
                        break
                    elif i == 'Minas Gerais' or i == 'MG' or i == 'minas' or i == 'Belo Horizonte':
                        state = 'MG'
                        break
                    elif i == 'Pará' or i == 'PA' or i == 'Belém':
                        state = 'PA'
                        break
                    elif i == 'Paraíba' or i == 'PB' or i == 'Paraiba' or i == 'João Pessoa':
                        state = 'PB'
                        break
                    elif i == 'Paraná' or i == 'PR' or i == 'Curitiba':
                        state = 'PR'
                        break
                    elif i == 'Pernambuco' or i == 'PE' or i == 'Recife':
                        state = 'PE'
                        break
                    elif i == 'Piauí' or i == 'PI' or i == 'Teresina':
                        state = 'PI'
                        break
                    elif i == 'Rio de Janeiro' or i == 'RJ':
                        state = 'RJ'
                        break
                    elif i == 'Rio Grande do Norte' or i == 'RN' or i == 'Natal':
                        state = 'RN'
                        break
                    elif i == 'Rio Grande do Sul' or i == 'Porto Alegre' or i == 'RS':
                        state = 'RS'
                        break
                    elif i == 'Rondônia' or i == 'RO' or i == 'Porto Velho':
                        state = 'RO'
                        break
                    elif i == 'Roraima' or i == 'RR' or i == 'Boa Vista':
                        state = 'RR'
                        break
                    elif i == 'Santa Catarina' or i == 'SC' or i == 'Florianópolis':
                        state = 'SC'
                        break
                    elif i == 'Sergipe' or i == 'SE' or i == 'Aracaju':
                        state = 'SE'
                        break
                    elif i == 'Tocantins' or i == 'TO' or i == 'Palmas':
                        state = 'TO'
                        break
                    elif i == 'São Paulo' or i == 'SP' or i == 'Sao Paulo':
                        state = 'SP'
                        break
            else:
                state = 'ND'
            id_state = STATES_IDS[state]

            user = row[1:6]    
            user.extend(['pt', id_state])
            text = row[11]
            sentiment = getSentiment(row[-1])

            curr_record += 1
            print('Record #%d'%(curr_record))

            ########################## INSERÇÕES NO BANCO DE DADOS #####################################

            insert_user = 'INSERT INTO usuario (id_usuario, nome, apelido, verificado, qtd_seguidores, idioma, local_id_local) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            # 0 para falso e 1 para verdadeiro
            user[3] = 0 if user[3] == 'False' else 1
            user = tuple(user)

            insert_tweet = 'INSERT INTO tweet (id_tweet, usuario_id_usuario, data, texto, idioma, local_id_local) VALUES (%s, %s, %s, %s, %s, %s)'
            tweet = (row[0], user[0], date, text, 'pt', id_state)

            insert_tweet_minister = 'INSERT INTO tweet_ministro VALUES (%s, %s, %s)'
            id_minister = 11
            tweet_minister = (row[0], id_minister, sentiment)

            insert_tweet_subject = 'INSERT INTO tweet_assunto VALUES (%s, %s, %s)'
            id_subject = 1
            tweet_subject = (row[0], id_subject, sentiment)

            # abre a conexão com o banco de dados
            db_conn = getConnection()
            cursor = db_conn.cursor()

            try:
                print("[INFO] Inserting into 'usuario' > {}".format(str(user)))
                cursor.execute(insert_user, user)
                print('[SUCCESS] OK!')
            except connector.IntegrityError as e:
                print('[ERROR]', e.msg)

            try:
                print("[INFO] Inserting into 'tweet' > {}".format(str(tweet)))
                cursor.execute(insert_tweet, tweet)
                print('[SUCCESS] OK!')
            except connector.IntegrityError as e:
                print('[ERROR]', e.msg)
                print()

            try:
                print("[INFO] Inserting into 'tweet_ministro' > {}".format(str(tweet_minister)))
                cursor.execute(insert_tweet_minister, tweet_minister)
                print('[SUCCESS] OK!')
            except connector.IntegrityError as e:
                print('[ERROR]', e.msg)

            # try:
            #     print("[INFO] Inserting into 'tweet_assunto' > {}".format(str(tweet_subject)))
            #     cursor.execute(insert_tweet_subject, tweet_subject)
            #     print('[SUCCESS] OK!')
            # except connector.IntegrityError as e:
            #     print('[ERROR]', e.msg)

            # fecha a conexão com o banco de dados
            db_conn.commit()
            cursor.close()
            db_conn.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            main(sys.argv[1])
        except KeyboardInterrupt:
            exit(0)
    else:
        print('Usage: python3 database_insertion.py <arq_entrada>')
        exit(1)
