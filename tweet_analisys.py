from textblob import TextBlob as tb
import sys

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

def processaTweet(tweet):
    # quebra em lista de palavras
    lista_palavras = tweet.split(" ")
    # filtra algumas palavras que podem atrapalhar a analise de sentimento
    lista_palavras=filter(filtraPalavra,lista_palavras)

    #remonta texto com lista de palavras
    txt = " ".join(lista_palavras)

    if len(txt) > 2:
        tweetblob = tb(txt)
        if debug:
            print ("Linguagem detectada:")
        lang = tweetblob.detect_language()
        if debug:
            print (lang)
        if lang != "en":
            if debug:
                print ("antes da traducao:")
                print (tweetblob.string)
            # tenta traduzir para uma var temporaria
            try:
                tweetblob2 = tb(tweetblob.translate(to='en').string)
            except:
                if debug:
                    print ("Houve um erro durante a traducao, usando texto original...")
                # no caso da traducao falhar passamos o mesmo texto original mesmo (provavelmente a analise de sentimento vai dar 0)
                # nao é ideal mas melhor que nao tratar a excecao
                tweetblob2 = tweetblob
            # apos o try acima tweetblob2 possui o texto que iremos processar
            tweetblob = tweetblob2
            if debug:
                print ("texto traducao:")
                print (tweetblob.string)
                print ("analise sentimento")
                print (tweetblob.sentiment)
            return (tweetblob.sentiment.polarity, tweetblob.string, lang)
        else:
            if debug:
                print ("analise sentimento")
                print (tweetblob.sentiment)
            return (tweetblob.sentiment.polarity, tweetblob.string, lang)
    else:
        # resolve bug da lista de palavra que ficava vazia e nao gerava um return
        return (0.0, "", "")


if __name__ == '__main__':
    arquivos = ["output/output_barroso.csv"]
    file = open("output/output_barroso.csv", encoding="iso-8859-1")
    cabecalho = file.readline()
    linhas = file.readlines()

    for i, j in enumerate(linhas):
        linhas[i] = j.split("\t")
        pol, proc_txt, lang = processaTweet(linhas[i][11])
        linhas[i].append(str(pol))
        linhas[i] = ",".join(linhas[i])

    print(linhas)

    out = open("output/output_barroso_analisys.csv", "w", encoding="iso-8859-1")
    # out.writeline(cabecalho)
    out.writelines(linhas)
    out.close()

