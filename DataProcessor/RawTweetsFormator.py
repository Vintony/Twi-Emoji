from collections import Counter
import regex
from emoji import UNICODE_EMOJI
from ..DataProcessor.TweetCreated_AtTranslator import time_translator
from ..DataProcessor.TweetGeoInfoTranslator import geo_translator
from ..SqlExecutor.InsertSqlExecutor import *
from ..UserConfig.emojiRange import *


def raw_tweets_formator(tweets, **kwargs):
    # translate created_at to mysql timestamp format
    time_translator(tweets)
    # translate geo(latitude, longitude) to exact address
    geo_translator(tweets)
    # extract json from raw data
    tweets_data = []
    emoji_stat = Counter({})
    emoji_table_count = 0
    for row in tweets:
        # check if tweet contains hashtags
        if len(row['entities']['hashtags']):
            hashtag_flag = 1
        else:
            hashtag_flag = 0
        # check if tweet contains emoji
        # full_emoji_list is v12.0 unicode in example\emoji.json
        emoji_flag = 0
        if use_customized_emoji == 1:
            emoji_dict = CUSTOMIZED_EMOJI
        else:
            emoji_dict = UNICODE_EMOJI

        for emoji in emoji_dict:
            if 'full_text' in row:
                if row['full_text'].count(emoji) >= 1:
                    emoji_flag = 1
                    break
            else:
                if row['text'].count(emoji) >= 1:
                    emoji_flag = 1
                    break

        counter, temp_stat, temp_table_count = split_count(text=row['full_text'] if 'full_text' in row else row['text'],
                                                           emoji_dict=emoji_dict, tweet_id=row['id'],
                                                           user_id=row['user']['id'])
        emoji_stat += temp_stat
        emoji_table_count += temp_table_count
        emoji_list = ' '.join(emoji for emoji in counter)

        # check if tweet is retweeted
        retweeted_flag = 0
        if 'retweeted_status' in row:
            retweeted_flag = 1
        row_dict = {'tweet_id': row['id'],
                    'user_id': row['user']['id'],
                    'screen_name': row['user']['screen_name'],
                    'full_text': row['full_text'] if 'full_text' in row else row['text'],
                    'keyword': None,
                    'tag': None,
                    'created_at': row['created_at'],
                    'geo': row['geo'],
                    'lang': row['lang'],
                    'retweet_count': row['retweet_count'],
                    'favorite_count': row['favorite_count'],
                    'tweet_type': kwargs['tweet_type'],
                    'collected_by': kwargs['collected_by'],
                    'emoji_flag': emoji_flag,
                    'emoji_list': emoji_list,
                    'hashtag_flag': hashtag_flag,
                    'retweeted': retweeted_flag
                    }
        tweets_data.append(row_dict)

    return tweets_data, emoji_stat, emoji_table_count


def split_count(text, emoji_dict, tweet_id, user_id):
    emoji_list = []
    emoji_stat = Counter({})
    emoji_stat_display = Counter({})
    data = regex.findall(r'\X', text)
    flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text)
    insert_executor = InsertSqlExecutor()
    emoji_table_created = 0
    for word in data:
        if any(char in emoji_dict for char in word):
            emoji_list.append(word)
            # delete the emoji end with VARIATION SELECTOR
            if len(word) <= 2:
                word = word[:-1] if any(word.endswith(x) for x in ['️', "︎"]) else word
            emoji_stat += Counter({emoji_dict[word]: 1})
            emoji_stat_display += Counter({word + emoji_dict[word]: 1})

    for i in range(0, int(len(flags)/2)):
        flag = flags[2*i] + flags[2*i+1]
        emoji_stat += Counter({emoji_dict[flag]: 1})
        emoji_stat_display += Counter({flag + emoji_dict[flag]: 1})

    for key, value in dict(emoji_stat).items():
        temp = insert_executor.insert_emoji(tweet_id=tweet_id, user_id=user_id,
                                            emoji_definition=key, usage_count=value)
        emoji_table_created += temp if temp else 0

    return emoji_list + flags, emoji_stat_display, emoji_table_created
