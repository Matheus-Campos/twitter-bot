from os import sep
from os.path import dirname, realpath
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


ids = []


def get_script_directory():
    return dirname(realpath(__file__))


def refreshScroll(drive):
    body = drive.find_element_by_tag_name('body')
    for i in range(2):
        body.send_keys(Keys.END)
        sleep(2)
    return drive.find_elements_by_class_name('tweet')


def incrementData(data):
    listaData = data.split("-")
    print(listaData)
    dia = int(listaData[2])
    mes = listaData[1]
    ano = listaData[0]
    dia+=1
    dia = '%0*d' % (2, dia)
    return ano + "-" + mes + "-" + str(dia)


def searchPage(navegador,dtInical,dtFinal, query):

    dataInicial = dtInical
    dataFinal = dtFinal

    base_url = "https://twitter.com/search?l=pt&q=" + query + "%20since%3A" + dataInicial + "%20until%3A" + dataFinal + "&src=typd&lang=pt"
    navegador.get(base_url)
    sleep(1.5)


def get_tweets(chrome_webdriver_path, dtInicial, query):

    datainicial = dtInicial
    browser = webdriver.Chrome(chrome_webdriver_path)

    # MODIFICAR O LIMITE DO RANGE PARA O ULTIMO DIA DO MES EM QUESTAO!!!
    for i in range(31):
        datafinal = incrementData(datainicial)

        searchPage(browser, datainicial, datafinal, query)
        try:
            tweets = browser.find_elements_by_class_name('tweet')
            increment = 10

            while len(tweets) >= increment:
                print('scrolling down to load more tweets')
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)
                tweets = browser.find_elements_by_class_name('tweet')
                increment = increment + 10

            print('{} tweets found, {} total'.format(len(tweets), len(ids)))

            for tweet in tweets:
                try:
                    id = tweet.get_attribute('data-tweet-id')
                    print(id)
                    ids.append(id)
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)

        except NoSuchElementException:
            print('no tweets on this day')

        datainicial = datafinal


def save_to_file(filename, ids):
    texto = ""
    for i in ids:
        if texto == "":
            texto += str(i)
        else:
            texto += str(i) + ","

    file = open(filename, 'w')
    file.write(texto)
    file.close()


if __name__ == '__main__':
    try:
        chrome_webdriver_path = get_script_directory() + '{0}webdriver{0}chromedriver'.format(sep)
        query = input('Digite o que você quer procurar: ')

        # MODIFICAR A DATA INICIAL NO SEGUNDO ARGUMENTO PARA O DO MES EM QUESTÃO!!!
        get_tweets(chrome_webdriver_path, "2018-03-01", query)
        save_to_file('tweets_ids.csv', ids)
    except KeyboardInterrupt:
        print('\nbye.')
        exit()
