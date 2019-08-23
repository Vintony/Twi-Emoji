from ..UserConfig import apiAuth
# from UserConfig import apiAuth
import tweepy


class StreamCrawler(object):
    def __init__(self, lang=None, retweeted=None, track_words=None, max_tweets=None):
        self.api = apiAuth.api
        self.lang = lang
        self.retweeted = retweeted
        self.TRACK_WORDS = track_words
        self.max_tweets = max_tweets
        self.listener = self.StreamListener(api=tweepy.API(wait_on_rate_limit=True),
                                            lang=self.lang,
                                            retweeted=self.retweeted,
                                            max_tweets=self.max_tweets)
        self.streamer = tweepy.Stream(auth=apiAuth.api.auth, listener=self.listener)

    def disconnect(self):
        self.listener.disconnect()

    def crawling(self):
        try:
            self.streamer.filter(track=self.TRACK_WORDS, is_async=False)

        except Exception as e:
            print(e)

    def get_streaming_tweets(self):
        return self.listener.get_streaming_tweets()

    def get_streaming_tweets_count(self):
        return self.listener.get_streaming_tweets_count()

    class StreamListener(tweepy.StreamListener):
        def __init__(self, api=None, lang=None, retweeted=False, max_tweets=None):
            self.api = api
            self.lang = lang
            self.retweeted = retweeted
            self.max_tweets = max_tweets
            self.count = 0
            self.streaming_tweets = []
            self.trigger = True

        def disconnect(self):
            self.trigger = False

        def on_connect(self):
            print("StreamCrawler are now connected to the streaming API.")

        def on_error(self, status_code):
            print("An Error has occurred: " + repr(status_code))
            return False

        def on_status(self, status):
            data = status._json
            if (data['lang'] == self.lang if self.lang else True) & \
                    (~ ((self.retweeted ^ ('retweeted_status' in data)) if self.retweeted is not None else False) & ~(data['truncated'])):
                self.count += 1
                self.streaming_tweets.append(status)
            if self.max_tweets:
                if self.count == self.max_tweets:
                    return False
            if not self.trigger:
                return False

        def get_streaming_tweets(self):
            return self.streaming_tweets

        def get_streaming_tweets_count(self):
            return len(self.streaming_tweets)


# stream_crawler = StreamCrawler(lang=None, retweeted=False, track_words=["a"], max_tweets=100)
# stream_crawler.crawling()
# print("-------")
# while stream_crawler.get_streaming_tweets_count() < 10:
#     if stream_crawler.get_streaming_tweets_count() >= 5:
#         stream_crawler.disconnect()
#         print(stream_crawler.get_streaming_tweets())
#         print(stream_crawler.get_streaming_tweets_count())
#         break

