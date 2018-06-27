from tweepy import OAuthHandler, API
import sys


class TweetGetter:

    def __init__(self, consumer_token, consumer_secret, oauth_token, oauth_secret):
        try:
            auth = OAuthHandler(consumer_token, consumer_secret)
            auth.set_access_token(oauth_token, oauth_secret)
            self.__api = API(auth, wait_on_rate_limit=True)
        except:
            print('invalid tokens')
            exit(1)

    def get_tweets(self, file, output):
        ids = file.read().split(',')
        records = []
        for id in ids:
            try:
                tweet = self.__api.get_status(id, tweet_mode='extended')
                user = tweet.user
                text = tweet.full_text.replace('\n', ' ')
                tweet_record = f'{tweet.id_str}\t{user.id_str}\t{user.name}\t{user.screen_name}\t{user.verified}\t{user.followers_count}\t{user.lang}\t{tweet.user.location}\t{tweet.favorite_count}\t{tweet.retweet_count}\t{tweet.created_at}\t{text}\t{tweet.retweeted}\n'
                records.append(tweet_record)
                print(f'{len(records)} tweets in records')
            except KeyboardInterrupt:
                self.__save_to_csvfile('output_'+output+'.csv', records)
                exit()
            except Exception as e:
                print(e)
                print('tweet does not exist anymore or tweepy was not able to get')
                continue
        else:
            self.__save_to_csvfile('output_'+output+'.csv', records)

    def __save_to_csvfile(self, filename, content):
        if filename[-4:] != '.csv':
            return
        file = open(filename, 'w')
        file.writelines(content)
        file.close()


if __name__ == '__main__':
    # print('Not this file.')
    # exit(1)
    consumer_token = 'gRXyhvV52uR2GyiFpfSmDKhLQ'
    consumer_secret = 'RuwEWK6RPJ1NAVMbJOicKbUgw96m9fmiFbupmdarCWwrgkbmvX'
    oauth_token = '534684487-bk0tijVH74tD52cBzynMkx09e11C9A1lx55QFSZ1'
    oauth_secret = '2tRoUcnZApggTbpztead4BpC7JGDt9D72aLCzcv3jmqxI'
    tg = TweetGetter(consumer_token, consumer_secret, oauth_token, oauth_secret)
    file = open('tweets_ids/'+sys.argv[1])
    output = sys.argv[2]
    tg.get_tweets(file, output)
