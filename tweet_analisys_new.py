import nltk
import re
import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

debug = False


def filtraPalavra(palavra):
    # ignora palavras vazias
    if palavra == "":
        if debug:
            print("palavra vazia ignorada")
        return False
    # ignora qualquer palavra que comeca com http
    if palavra[:4] == "http":
        if debug:
            print("link ignorado")
        return False
    # ignora qualquer palavra que tenha @ no inicio (referencia a outro usuario)
    if palavra[0] == "@":
        if debug:
            print("nome de usuario removido")
        return False
    # ignora RT (retwit)
    if palavra == "RT":
        if debug:
            print("removido tag RT")
        return False
    # ignora richtext
    if palavra[0] == "&":
        if debug:
            print("removido tag richtext")
        return False
    # ignora hashtag
    if palavra[0] == "#":
        if debug:
            print("removido hashtag")
        return False
    return True


# dataset = pd.read_csv('Tweets_Mg.csv',encoding='utf-8')
def limpa_tweet(tweet):
    # quebra em lista de palavras
    lista_palavras = tweet.split(" ")
    # filtra algumas palavras que podem atrapalhar a analise de sentimento
    lista_palavras = filter(filtraPalavra, lista_palavras)
    # remonta texto com lista de palavras
    return " ".join(lista_palavras)


def analisa_sentimento(arq_name):
    linhas = []
    tweets = []
    with open('output_' + arq_name + '.csv', 'r', encoding="UTF8") as arq:
        reader = csv.reader(arq, delimiter='\t')
        for row in reader:
            try:
                tweets.append(limpa_tweet(row[11]))
                linhas.append(row[0:13])
            except:
                continue
    # print(len(tweets))
    # print(len(linhas))
    freq_tweets = vectorizer.transform(tweets)
    analise = modelo.predict(freq_tweets)
    analise = analise.tolist()
    # print(linhas)
    for pos, linha in enumerate(linhas):
        linhas[pos].append(analise[pos])
    with open('output_' + arq_name + '_analisys.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')

        for row in linhas:
            writer.writerow(row)
    return


## -------- TREINO DO ALGORITMO ATRAVES DO MACHINE LEARNING --- NAO ALTERAR -----
l_tweets = []
l_classes = []

with open('Modelo_base_barroso.csv', 'r', encoding="UTF8") as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        l_tweets.append(limpa_tweet(row[11]))
        l_classes.append(row[13])

vectorizer = CountVectorizer(analyzer="word")
freq_tweets = vectorizer.fit_transform(l_tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets, l_classes)

freq_testes = vectorizer.transform(l_tweets)

# RESULTADO DA ANALISE
# resultados = cross_val_predict(modelo, freq_tweets, l_classes, cv=10)


arquivos = [ 'barroso', 'carmen_lucia', 'celso', 'fachin', 'fux', 'gilmar', 'marco_aurelio', 'moraes', 'ricardo', 'stf',
            'toffoli', 'weber']

for i in arquivos:
    # print(i)
    analisa_sentimento(i)
