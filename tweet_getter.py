from tweepy import OAuthHandler, API


class TweetGetter:

    def __init__(self, consumer_token, consumer_secret, oauth_token, oauth_secret):
        try:
            auth = OAuthHandler(consumer_token, consumer_secret)
            auth.set_access_token(oauth_token, oauth_secret)
            self.__api = API(auth)
        except:
            print('invalid tokens')
            exit(1)

    def get_tweets(self, file):
        ids = file.read().split(',')
        for id in ids:
            try:
                tweet = self.__api.get_status(id, tweet_mode='extended')
                location_record = f'Location record: {tweet.user.location}'
                user = tweet.user
                user_record = f'User record: {user.id_str},{user.name},{user.screen_name},{user.verified},{user.followers_count},{user.lang}'
                tweet_record = f'Tweet record: {tweet.id_str},{user.id_str},{tweet.favorite_count},{tweet.retweet_count},{tweet.created_at},{tweet.full_text},{tweet.retweeted}'
            except:
                print('tweet does not exist anymore or tweepy was not able to get')
                continue
            print(location_record)
            print(user_record)
            print(tweet_record)




if __name__ == '__main__':
    # print('Not this file.')
    # exit(1)
    consumer_token = 'gRXyhvV52uR2GyiFpfSmDKhLQ'
    consumer_secret = 'RuwEWK6RPJ1NAVMbJOicKbUgw96m9fmiFbupmdarCWwrgkbmvX'
    oauth_token = '534684487-bk0tijVH74tD52cBzynMkx09e11C9A1lx55QFSZ1'
    oauth_secret = '2tRoUcnZApggTbpztead4BpC7JGDt9D72aLCzcv3jmqxI'
    tg = TweetGetter(consumer_token, consumer_secret, oauth_token, oauth_secret)
    file = open('tweets_ids/ids_barroso.csv')
    tg.get_tweets(file)
