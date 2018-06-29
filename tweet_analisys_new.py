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
            print ("palavra vazia ignorada")
        return False
    # ignora qualquer palavra que comeca com http
    if palavra[:4] == "http":
        if debug:
            print ("link ignorado")
        return False
    # ignora qualquer palavra que tenha @ no inicio (referencia a outro usuario)
    if palavra[0] == "@":
        if debug:
            print ("nome de usuario removido")
        return False
    # ignora RT (retwit)
    if palavra == "RT":
        if debug:
            print ("removido tag RT")
        return False
    # ignora richtext
    if palavra[0] == "&":
        if debug:
            print ("removido tag richtext")
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

l_tweets = []
l_classes = []
with open('Modelo_base_barroso.csv','r',encoding="UTF8") as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        l_tweets.append(limpa_tweet(row[11]))
        l_classes.append(row[13])

print(l_tweets)
vectorizer = CountVectorizer(analyzer="word")
freq_tweets = vectorizer.fit_transform(l_tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets,l_classes)

#{{Sessão destinada a inserção dos tweets da base de dados}}
# testes2 = ['O militante Roberto Barroso está desrespeitando a constituição p/ tentar atrapalhar o gov. @MichelTemer e consequentemente, atrapalhar a recuperação do Brasil. Não bastaram as tentativas de golpe contra o Temer. O @SenadoFederal não reage, deveriam pedir o impeachment desse cara.']

freq_testes = vectorizer.transform(l_tweets)
modelo.predict(freq_testes)

#RESULTADO DA ANALISE
print(modelo.predict(freq_testes))

resultados = cross_val_predict(modelo, freq_tweets, l_classes, cv=10)
print(metrics.accuracy_score(l_classes, resultados))


sentimento =['positivo','negativo','neutro']
print (metrics.classification_report(l_classes,resultados,sentimento))

# --- Da erro por algum motivo ---
# print(pd.crosstab(l_classes, resultados, rownames=['Real'], colnames=['Predito'], margins=True))


# -- Utilizando Bigrams --
vectorizer2 = CountVectorizer(ngram_range=(1,2))
freq_tweets2 = vectorizer.fit_transform(l_tweets)
modelo2 = MultinomialNB()
modelo2.fit(freq_tweets2,l_classes)

resultados2 = cross_val_predict(modelo2, freq_tweets2, l_classes, cv=10)
print(metrics.accuracy_score(l_classes,resultados2))

print (metrics.classification_report(l_classes,resultados2,sentimento))