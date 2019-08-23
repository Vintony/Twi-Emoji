from emoji import UNICODE_EMOJI


class CrawlerRuleDefiner(object):
    def __init__(self, required_keywords=None, optional_keywords=None, lang=None,
                 retweeted=None, has_hashtags=None, has_emojis=None,
                 has_user_mentions=None, has_urls=None, has_symbols=None,
                 quote_range=None, reply_range=None, retweet_range=None,
                 favorite_range=None):
        """
        CrawlerRuleDefiner: accept parameters to create rule and filter out the illegal tweets
        :param required_keywords: list of keyword(s) that Tweets must have all keywords
        :param optional_keywords: list of keyword(s) that Tweets must have at least one of keywords
        :param lang: language of the Tweets
        :param retweeted: allow retweeted Tweets or not:
                        True ---- only retweeted Tweets,
                        False --- no retweeted Tweets,
                        None ---- both retweeted and no retweeted Tweets
        :param has_hashtags: whether Tweets must contain hashtags or not
                        True ---- must contain at least one hashtag
                        False --- no hashtag
                        None ---- no limitation on hashtag
        :param has_emojis: whether Tweets must contain emojis or not
                        True ---- must contain at least one emoji
                        False --- no emoji (quite slow for loop)
                        None ---- no limitation on emoji
        :param has_user_mentions: whether Tweets must mention other users or not
                        True ---- must contain at least one user mention
                        False --- no user mention
                        None ---- no limitation on user mentions
        :param has_urls: whether Tweets must contain urls or not
                        True ---- must contain at least one url
                        False --- no url
                        None ---- no limitation on url
        :param has_symbols: whether Tweets contain symbols or not
                        True ---- must contain at least one symbol
                        False --- no symbol
                        None ---- no limitation on symbol
        :param quote_range: Tweets' quote_count range: None for no requirement or
                            [min, max] for quote_count between min and max
        :param reply_range: Tweets' reply_count range: None for no requirement or
                            [min, max] for reply_count between min and max
        :param retweet_range: Tweets' retweet_count range: None for no requirement or
                              [min, max] for retweet_count between min and max
        :param favorite_range: Tweets' favorite_count range: None for no requirement or
                               [min, max] for favorite_count between min and max
        """

        self.REQUIRED_KEYWORDS = required_keywords
        self.OPTIONAL_KEYWORDS = optional_keywords
        self.LANG = lang
        self.RETWEETED = retweeted
        self.HAS_HASHTAGS = has_hashtags
        self.HAS_EMOJIS = has_emojis
        self.HAS_USER_MENTIONS = has_user_mentions
        self.HAS_URLS = has_urls
        self.HAS_SYMBOLS = has_symbols
        self.QUOTE_RANGE = quote_range
        self.REPLY_RANGE = reply_range
        self.RETWEET_RANGE = retweet_range
        self.FAVORITE_RANGE = favorite_range

    def filter(self, tweets=None):
        """
        :param tweets: tweet.status.object
        :return: dict contains full data from tweet.status.object
        """
        legal_tweets = []
        for raw_row in tweets:
            row = raw_row._json
            legal_flag = True

            if legal_flag and self.REQUIRED_KEYWORDS:
                for keyword in self.REQUIRED_KEYWORDS:
                    if row['full_text'].count(keyword) < 1:
                        legal_flag = False
                        break

            if legal_flag and self.OPTIONAL_KEYWORDS:
                legal_flag = False
                for keyword in self.OPTIONAL_KEYWORDS:
                    if row['full_text'].count(keyword) >= 1:
                        legal_flag = True
                        break

            if legal_flag and self.LANG:
                if row['lang'] != self.LANG:
                    legal_flag = False

            if legal_flag and self.RETWEETED is not None:
                if self.RETWEETED and 'retweeted_status' not in row:
                    legal_flag = False

                if not self.RETWEETED and 'retweeted_status' in row:
                    legal_flag = False

            if legal_flag and self.HAS_HASHTAGS is not None:
                if self.HAS_HASHTAGS and not len(row['entities']['hashtags']):
                    legal_flag = False
                if not self.HAS_HASHTAGS and len(row['entities']['hashtags']):
                    legal_flag = False

            if legal_flag and self.HAS_EMOJIS is not None:
                if self.HAS_EMOJIS:
                    legal_flag = False
                    for emoji in UNICODE_EMOJI:
                        if row['full_text'].count(emoji) >= 1:
                            legal_flag = True
                            break

                if not self.HAS_EMOJIS:
                    for emoji in UNICODE_EMOJI:
                        if row['full_text'].count(emoji) >= 1:
                            legal_flag = False
                            break

            if legal_flag and self.HAS_USER_MENTIONS is not None:
                if self.HAS_USER_MENTIONS and not len(row['entities']['user_mentions']):
                    legal_flag = False
                if not self.HAS_USER_MENTIONS and len(row['entities']['user_mentions']):
                    legal_flag = False

            if legal_flag and self.HAS_URLS is not None:
                if self.HAS_URLS and not len(row['entities']['urls']):
                    legal_flag = False
                if self.HAS_URLS and len(row['entities']['urls']):
                    legal_flag = False

            if legal_flag and self.HAS_SYMBOLS is not None:
                if self.HAS_SYMBOLS and not len(row['entities']['urls']):
                    legal_flag = False
                if self.HAS_SYMBOLS and len(row['entities']['urls']):
                    legal_flag = False

            if legal_flag and self.QUOTE_RANGE is not None:
                if not self.QUOTE_RANGE[0] < row['quote_count'] < self.QUOTE_RANGE[1]:
                    legal_flag = False

            if legal_flag and self.REPLY_RANGE is not None:
                if not self.REPLY_RANGE[0] < row['reply_count'] < self.REPLY_RANGE[1]:
                    legal_flag = False

            if legal_flag and self.RETWEET_RANGE is not None:
                if not self.RETWEET_RANGE[0] < row['retweet_count'] < self.RETWEET_RANGE[1]:
                    legal_flag = False

            if legal_flag and self.FAVORITE_RANGE is not None:
                if not self.FAVORITE_RANGE[0] < row['favorite_count'] < self.RETWEET_RANGE[1]:
                    legal_flag = False

            if legal_flag:
                legal_tweets.append(row)
            else:
                pass

        return legal_tweets


# crawler_rule_alpha = CrawlerRuleDefiner(required_keywords=["football", "soccer"], optional_keywords=["manchester", "uk"])
# dict1 = {'full_text': 'football soccer uk'}
# dict2 = {'full_text': 'football soccer'}
# dict3 = {'full_text': 'football uk'}
# dict4 = {'full_text': 'football soccer uk manchester'}
#
# crawler_rule_alpha.filter(row=dict1)
# crawler_rule_alpha.filter(row=dict2)
# crawler_rule_alpha.filter(row=dict3)
# crawler_rule_alpha.filter(row=dict4)

# test1 = False
# test2 = None
#
# if test1 is None:
#     print("test1 is none")
#
# if test2 is None:
#     print("test2 is none")
#
# if test1 is False:
#     print("test1 is false")
#
# if test2 is False:
#     print("test2 is false")

# flag1 = True
# flag2 = False
# flag3 = None
#
# row1 = {'a': 'b', 'retweeted_status': '123'}
# row2 = {'a': 'b'}
#
#
# def test1(flag, row):
#     if flag is not None:
#         legal_flag = True
#         if flag and 'retweeted_status' not in row:
#             legal_flag = False
#
#         if not flag and 'retweeted_status' in row:
#             legal_flag = False
#         print(legal_flag)
#     else:
#         print("None")
#
#
# test1(flag1, row1)
# test1(flag2, row1)
# test1(flag2, row2)
# test1(flag3, row1)
