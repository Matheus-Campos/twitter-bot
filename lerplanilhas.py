# -*- coding: utf-8 -*-
import csv
import sys
import pycountry

STATES = [state.name for state in pycountry.subdivisions.get(country_code='BR')]
STATES.remove('Fernando de Noronha')  # remove a subdivisão Fernando de Noronha


def pegaLocal(local):
    """Retorna a quantidade de elementos numa lista de lugares
     e a própria lista."""
    if local.find(','):
        local = local.split(',')
        try:
            float(local[0])  # checa se a localização é uma coordenada
            return 2, local
        except ValueError:
            pass
    elif local.find('-'):
        local = local.split('-')
    elif local.find('/'):
        local = local.split('/')
    else:
        # presumi-se que a localização é nula
        return 0, []
    return len(local), local


def main(input_file, output):
    # Abre o arquivo de saída para escrita:
    with open(input_file, 'r') as file_read, open(output, 'w') as file_write:

        # Define o leitor CSV do arquivo:
        reader = csv.reader(file_read, delimiter=';')
        # header = next(reader) # passa a primeira linha (cabealho)

        # Define o escritor CSV do arquivo:
        fieldnames = ['date','ano','mes','dia','city', 'state', 'country', 'user id', 'username', 'user nickname','tweet', 'feeling']
        writer = csv.DictWriter(file_write, fieldnames=fieldnames, delimiter=';')  # inicia como DictWriter para permitir a escrita por dicionário
        writer.writeheader() # escreve o cabeçalho no arquivo

        # Percorre as linhas do arquivo de entrada:
        for row in reader:
            # separa os dados do CSV de leitura
            date, time = row[10].split(' ')
            number, place = pegaLocal(row[7])  # retorna o número de itens na lista de locais e a lista de locais
            place = [p.replace('Brazil', 'Brasil') for p in place] # substitui Brazil por Brasil
            user = [row[1], row[2], row[3]]
            tweet = row[11]
            feeling = (row[-1])
            dia, mes, ano = date.split('/')
            # coloca os dados organizados num dicionário
            data = {'date': date, 'ano': ano, 'mes': mes, 'dia': dia, 'username': user[1], 'user id': user[0], 'user nickname': user[2], 'tweet': tweet, 'feeling': feeling}

            # quebra a localização do tweet, organizando por país, estado e cidade
            if place[0] == 'Brasil':
                data['country'] = place[0]
            elif place[-1] == 'Brasil':
                data['country'] = place[-1]
                if len(place) == 2:
                    data['state'] = place[0]
                else:
                    data['city'] = place[0]
                    data['state'] = place[1]
            else:
                data['state'] = place[-1]
                if len(place) > 1:
                    data['city'] = place[0]

            # escreve no arquivo de escrita
            writer.writerow(data)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Usage: python3 lerplanilhas.py-OLD <arq_entrada> <arq_saida>')
        exit(1)
