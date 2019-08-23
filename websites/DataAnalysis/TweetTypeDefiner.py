from datetime import datetime

from ..SqlExecutor.SelectSqlExecutor import *
from ..SqlExecutor.UpdateSqlExecutor import *


class TweetTypeDefiner(object):
    def __init__(self, type_name, required_keywords=None, optional_keywords=None, required_tags=None,
                 optional_tags=None, max_age=None, min_age=None, geo=None, lang=None, retweet_range=None, favorite_range=None,
                 collected_by=None, has_emoji=None, has_hashtag=None, retweeted=None):
        """
        TweetTypeDefiner: accept parameters to indicate Tweet's type
        :param type_name: TweetType Name
        :param required_keywords: list of keywords that Tweet's full_text must have all keywords
        :param optional_keywords: list of keywords that Tweet's full_text must have at least one of keywords
        :param required_tags: list of tags that Tweet's tag must have all tags
        :param optional_tags: list of tags that Tweet's tag must have at least one of tags
        :param max_age: max age of the Tweet (calculate by system_time - created_at)
        :param min_age: min age of the Tweet
        :param geo: geo of the Tweet
        :param lang: language of the Tweet
        :param retweet_range: Tweet's retweet_count range: None for no requirement or
                            [min, max] for retweet_count between min and max
        :param favorite_range: Tweet's favorite_count range: None for no requirement or
                            [min, max] for favorite_count between min and max
        :param collected_by: collected_by of the Tweet
        :param has_emoji: whether Tweet must contain emojis or not
                        True ---- must contain at least one emoji
                        False --- no emoji (quite slow for loop)
                        None ---- no limitation on emoji
        :param has_hashtag: whether Tweet must contain hashtag or not
                        True ---- must contain at least one hashtag
                        False --- no hashtag
                        None ---- no limitation on hashtag
        :param retweeted: whether Tweet is retweeted or not
                        True ---- retweeted Tweet
                        False --- non-retweeted Tweet
                        None ---- no limitation on retweeted
        """
        self.REQUIRED_KEYWORDS = required_keywords
        self.OPTIONAL_KEYWORDS = optional_keywords
        self.REQUIRED_TAGS = required_tags
        self.OPTIONAL_TAGS = optional_tags
        self.MAX_AGE = max_age
        self.MIN_AGE = min_age
        self.GEO = geo
        self.LANG = lang
        self.RETWEET_RANGE = retweet_range
        self.FAVORITE_RANGE = favorite_range
        self.COLLECTED_BY = collected_by
        self.HAS_EMOJI = has_emoji
        self.HAS_HASHTAG = has_hashtag
        self.RETWEETED = retweeted
        self.type_name = type_name
        self.select_executor = SelectSqlExecutor()
        self.update_executor = UpdateSqlExecutor()

    def define_tweets_type(self, list_of_ids=None):
        if list_of_ids:
            tweets = self.select_executor.select_tweets_by_tweet_id(list_of_ids)
            for TWEET in tweets:
                legal_flag = True
                tweet_id = TWEET[0]
                user_id = TWEET[1]
                screen_name = TWEET[2]
                tweet_type = TWEET[3]
                full_text = TWEET[4]
                keyword = TWEET[5]
                tag = TWEET[6]
                created_at = TWEET[7]
                geo = TWEET[8]
                lang = TWEET[9]
                retweet_count = TWEET[10]
                favorite_count = TWEET[11]
                collected_by = TWEET[12]
                emoji_flag= TWEET[13]
                hashtag_flag = TWEET[14]
                retweeted = TWEET[15]

                if legal_flag and self.REQUIRED_KEYWORDS is not None:
                    for keyword in self.REQUIRED_KEYWORDS:
                        if full_text.count(keyword) < 1:
                            legal_flag = False
                            break

                if legal_flag and self.OPTIONAL_KEYWORDS is not None:
                    legal_flag = False
                    for keyword in self.OPTIONAL_KEYWORDS:
                        if full_text.count(keyword) >= 1:
                            legal_flag = True
                            break

                if legal_flag and self.REQUIRED_TAGS is not None:
                    for t in self.REQUIRED_TAGS:
                        if tag.count(t) < 1:
                            legal_flag = False
                            break

                if legal_flag and self.OPTIONAL_TAGS is not None:
                    legal_flag = False
                    for t in self.OPTIONAL_TAGS:
                        if tag.count(t) >= 1:
                            legal_flag = True
                            break

                if created_at:
                    age = ((datetime.now() - datetime.strptime(created_at,
                                                               '%Y-%m-%d %H:%M:%S')).days)
                    if legal_flag and self.MAX_AGE is not None:
                        if age > self.MAX_AGE:
                            legal_flag = False

                    if legal_flag and self.MIN_AGE is not None:
                        if age < self.MIN_AGE:
                            legal_flag = False

                else:
                    if self.MAX_AGE is not None or self.MIN_AGE is not None:
                        legal_flag = False

                if legal_flag and self.GEO is not None:
                    if geo != self.GEO:
                        legal_flag = False

                if legal_flag and self.LANG is not None:
                    if lang != self.LANG:
                        legal_flag = False

                if legal_flag and self.RETWEET_RANGE is not None:
                    if not (self.RETWEET_RANGE[0] < retweet_count < self.RETWEET_RANGE[1]):
                        legal_flag = False

                if legal_flag and self.FAVORITE_RANGE is not None:
                    if not (self.FAVORITE_RANGE[0] < favorite_count < self.FAVORITE_RANGE[1]):
                        legal_flag = False

                if legal_flag and self.COLLECTED_BY is not None:
                    if collected_by != self.COLLECTED_BY:
                        legal_flag = False

                if legal_flag and self.HAS_EMOJI is not None:
                    if self.HAS_EMOJI and not emoji_flag:
                        legal_flag = False
                    if not self.HAS_EMOJI and emoji_flag:
                        legal_flag = False

                if legal_flag and self.HAS_HASHTAG is not None:
                    if self.HAS_HASHTAG and not hashtag_flag:
                        legal_flag = False
                    if not self.HAS_HASHTAG and hashtag_flag:
                        legal_flag = False

                if legal_flag and self.RETWEETED is not None:
                    if self.RETWEETED and not retweeted:
                        legal_flag = False
                    if not self.RETWEETED and retweeted:
                        legal_flag = False

                if legal_flag:
                    print("update tweet " + str(tweet_id) + " " + self.type_name)
                    self.update_executor.update_tweet_by_id(update_id=tweet_id, tweet_type=self.type_name)
                else:
                    pass

    def close(self):
        self.select_executor.close()
        self.update_executor.close()

