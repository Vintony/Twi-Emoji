from ..UserConfig import apiAuth
# from UserConfig import apiAuth
import tweepy


class UserCrawler(object):
    def __init__(self, user_id=None, screen_name=None, max_tweets=400):
        self.api = apiAuth.api
        self.user_id = user_id
        self.screen_name = screen_name
        self.max_tweets = max_tweets
        self.user_tweets = []

    def crawling(self):
        try:
            if self.max_tweets < 200:
                new_tweets = self.api.user_timeline(user_id=self.user_id, screen_name=self.screen_name, count=self.max_tweets, tweet_mode='extended')
                self.max_tweets = 0
            else:
                new_tweets = self.api.user_timeline(user_id=self.user_id, screen_name=self.screen_name, count=200, tweet_mode='extended')
                self.max_tweets -= 200
            self.user_tweets.extend(new_tweets)
            oldest = self.user_tweets[-1].id - 1

            while len(new_tweets) > 0 and self.max_tweets > 0:
                if self.max_tweets < 200:
                    new_tweets = self.api.user_timeline(user_id=self.user_id, screen_name=self.screen_name,
                                                        count=self.max_tweets, tweet_mode='extended', max_id=str(oldest))
                    self.max_tweets = 0
                else:
                    new_tweets = self.api.user_timeline(user_id=self.user_id, screen_name=self.screen_name, count=200,
                                                        tweet_mode='extended', max_id=str(oldest))
                    self.max_tweets -= 200
                self.user_tweets.extend(new_tweets)
                oldest = self.user_tweets[-1].id - 1
            print("...%s tweets downloaded so far for: %s" % (len(self.user_tweets), self.screen_name))
        except tweepy.TweepError as e:
            print(e)

    def get_user_tweets(self):
        return self.user_tweets

    def get_user_tweets_number(self):
        return len(self.user_tweets)


# if __name__ == '__main__':
#     user_crawler = UserCrawler(user_id=15969831, screen_name=None, max_tweets=5)
#     user_crawler.crawling()
#     print(user_crawler.get_user_tweets()[0]._json['user']['id'])
