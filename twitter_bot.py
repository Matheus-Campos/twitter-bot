from os import sep
from os.path import dirname, realpath
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_script_directory():
    return dirname(realpath(__file__))


def get_tweets(chrome_webdriver_path, query):
    base_url = 'https://twitter.com/search?q='
    url = base_url + query

    browser = webdriver.Chrome(chrome_webdriver_path)
    browser.get(url)
    sleep(1.5)

    body = browser.find_element_by_tag_name('body')

    for i in range(5):
        body.send_keys(Keys.END)
        sleep(2)

    tweets = browser.find_elements_by_class_name('tweet')
    tweets_ids = ''

    for tweet in tweets:
        print('(' + tweet.text + ')')
        tweet_id = tweet.get_attribute('data-tweet-id')
        if (tweet is tweets[-1]):
            tweets_ids += tweet_id
        else:
            tweets_ids += tweet_id + ','

    browser.quit()
    return tweets_ids


def save_to_file(filename, ids):
    file = open(filename, 'w')
    file.write(ids)
    file.close()


if __name__ == '__main__':
    try:
        chrome_webdriver_path = get_script_directory() + '{0}webdriver{0}chromedriver'.format(sep)
        query = input('Digite o que você quer procurar: ')
        ids = get_tweets(chrome_webdriver_path, query.strip())
        save_to_file('tweets_ids.csv', ids)
    except KeyboardInterrupt:
        print('\nbye.')
        exit()
