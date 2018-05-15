#!/usr/bin/env python3

import sys
from os import sep
from os.path import dirname, realpath
from time import sleep
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

ids = []


def get_script_directory():
    return dirname(realpath(__file__))


def searchPage(navegador, dtInical, dtFinal, query):
    dataInicial = dtInical
    dataFinal = dtFinal
    base_url = "https://twitter.com/search?l=pt&q=" + query + "%20since%3A" + str(dataInicial) + "%20until%3A" + str(dataFinal) + "&src=typd&lang=pt"
    navegador.get(base_url)
    sleep(1.5)


def get_tweets(chrome_webdriver_path, initial_date, query):
    datainicial = initial_date
    browser = webdriver.Chrome(chrome_webdriver_path)

    # MODIFICAR O LIMITE DO RANGE PARA O NÚMERO DE DIAS DE COLETA DE TWEETS
    for i in range(76):
        datafinal = datainicial + timedelta(days=1)
        print('[INFO] gettings tweets from ' + datafinal)
        searchPage(browser, datainicial, datafinal, query)
        try:
            body = browser.find_element_by_tag_name('body')
            tweets = body.find_elements_by_class_name('tweet')
            increment = 10
            while len(tweets) >= increment:
                print('[INFO] scrolling down to load more tweets')
                body.send_keys(Keys.END)
                sleep(2)
                tweets = browser.find_elements_by_class_name('tweet')
                increment = increment + 10
            print('[SUCCESS] {} tweets found, {} total'.format(len(tweets), len(ids)))
            for tweet in tweets:
                try:
                    id = tweet.get_attribute('data-tweet-id')
                    print(id)
                    ids.append(id)
                except StaleElementReferenceException:
                    print('[ERROR] lost element reference', tweet)
        except NoSuchElementException:
            print('[ERROR] no tweets on this day')
        datainicial = datafinal


def save_to_file(filename, ids):
    print('saving in ' + filename)
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
    if len(sys.argv) < 3:
        print('Usage: python3 <query> <output_file>')
        sys.exit(1)
    try:
        chrome_webdriver_path = get_script_directory() + '{0}webdriver{0}chromedriver'.format(sep) 
        query = sys.argv[1]
        output_file = sys.argv[2]
        initial_date = date(2018, 3, 1)
        get_tweets(chrome_webdriver_path, initial_date, query)
    except KeyboardInterrupt or Exception:
        pass
    finally:
        try:
            save_to_file(output_file, ids)
        except:
            print('[FATAL] could not save ids')
        print('\nbye.')
        exit()
