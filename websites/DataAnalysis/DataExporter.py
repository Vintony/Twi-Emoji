import io
import json
from ..SqlExecutor.SelectSqlExecutor import *
import codecs


class DataExporter(object):
    def __init__(self, tweet_type=None, tweet_tag=None, account_type=None, account_tag=None):
        self.TWEET_TYPE = tweet_type
        self.TWEET_TAG = tweet_tag
        self.ACCOUNT_TYPE = account_type
        self.ACCOUNT_TAG = account_tag

    def fetch_data(self):
        select_executor = SelectSqlExecutor()
        tweet_data = []
        if self.TWEET_TYPE is None and self.ACCOUNT_TYPE is None:
            for tweet in select_executor.select_all_tweets():
                tweet_data.append({
                    'full_text': tweet[4],
                    'emoji_list': tweet[14],
                })

            return tweet_data

        if self.TWEET_TYPE is not None:
            for tweet in select_executor.select_tweets_by_type(self.TWEET_TYPE):
                tweet_data.append({
                    'full_text': tweet[4],
                    'emoji_list': tweet[14],
                })

            if self.ACCOUNT_TYPE is not None:
                user_id = []
                tweet_data_temp = []
                for user_info in select_executor.select_users_by_type(self.ACCOUNT_TYPE):
                    user_id.append(user_info[0])
                for tweet in tweet_data:
                    if tweet['user_id'] in user_id:
                        tweet_data_temp.append(tweet)

                return tweet_data_temp
            else:
                return tweet_data
        else:
            user_id = []
            for user_info in select_executor.select_users_by_type(self.ACCOUNT_TYPE):
                user_id.append([user_info[0]])
            for tweet in select_executor.select_tweets_by_user_id(user_id):
                tweet_data.append({
                    'full_text': tweet[4],
                    'emoji_list': tweet[14],
                })

            return tweet_data

    def create_json(self):
        sample = {
            "name": "chinese-tweets",
            "data": self.fetch_data()
        }

        with io.open(str(len(self.fetch_data())) + '_zh_tweets.json', 'w', encoding='utf-8') as fp:
            json.dump(sample, fp, indent=2, ensure_ascii=False)

        # with codecs.open(str(len(self.fetch_data())) + '_zh_tweets.json', 'a+', 'utf-8') as fp:
        #     fp.write(json.dump(sample, fp, indent=2, ensure_ascii=False))
        #     fp.close()

# with open('result.json', 'w') as fp:
#     sample = {
#         "name": "english-tweets",
#         "data": [
#             {"text": "manchester is good!❤", "emoji_list": "❤"},
#             {"text": "manchester is great!❤❤❤❤", "emoji_list": "❤❤❤"},
#             {"text": "🔴LIVE NOW !! Manchester City vs West Ham United LIVE STREAM NOW TV |  #mancity #MCIWHU #COYI #PLAsiaTrophy link :: https://t.co/wrGgSy8Zcx https://t.co/dFKDxRwHUL", "emoji_list": "🔴"}
#         ]
#     }
#     json.dump(sample, fp, indent=2)

