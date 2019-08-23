from ..UserConfig import apiAuth
import tweepy


class SearchCrawler(object):
    def __init__(self, query=None, lang=None, max_tweets=None, tweet_mode=None, crawler_mode=None):
        self.api = apiAuth.api
        self.query = query
        self.lang = lang
        self.max_tweets = max_tweets
        self.tweet_mode = tweet_mode
        self.searched_tweets = []
        self.mode = crawler_mode

    def crawling(self):
        last_id = -1
        while len(self.get_searched_tweets()) < self.max_tweets:
            count = self.max_tweets - len(self.get_searched_tweets())
            try:
                new_tweets = self.api.search(q=self.query, lang=self.lang, count=count, max_id=str(last_id - 1),
                                             tweet_mode=self.tweet_mode)
                if not new_tweets:
                    break
                self.get_searched_tweets().extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                print(e)
                break

    def get_searched_tweets(self):
        return self.searched_tweets

    def get_searched_tweets_number(self):
        return len(self.searched_tweets)
