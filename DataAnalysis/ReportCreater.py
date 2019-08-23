from ..SqlExecutor.SelectSqlExecutor import *
# from SqlExecutor.SelectSqlExecutor import *


class ReportCreater(object):
    def __init__(self, tweet_type=None, account_type=None, tweet_tag=None, account_tag=None):
        self.TWEET_TYPE = tweet_type
        self.ACCOUNT_TYPE = account_type
        self.TWEET_TAG = tweet_tag
        self.ACCOUNT_TAG = account_tag

    def fetch_data(self):
        select_executor = SelectSqlExecutor()
        report_ids = []
        tweet_data = []
        if self.TWEET_TYPE is None and self.ACCOUNT_TYPE is None:
            for tweet in select_executor.select_all_tweets():
                tweet_data.append({
                    'tweet_id': tweet[0],
                    'user_id': tweet[1],
                    'screen_name': tweet[2],
                    'tweet_type': tweet[3],
                    'full_text': tweet[4],
                    'keyword': tweet[5],
                    'tag': tweet[6],
                    'created_at': str(tweet[7]),
                    'geo': tweet[8],
                    'lang': tweet[9],
                    'retweet_count': tweet[10],
                    'favorite_count': tweet[11],
                    'collected_by': tweet[12],
                    'emoji_flag': tweet[13],
                    'emoji_list': tweet[14],
                    'hashtag_flag': tweet[15],
                    'retweeted': tweet[16]
                })
                report_ids.append({
                    'tweet_id': tweet[0],
                    'user_id': tweet[1]
                })
            return report_ids, tweet_data

        if self.TWEET_TYPE is not None:
            for tweet in select_executor.select_tweets_by_type(self.TWEET_TYPE):
                tweet_data.append({
                    'tweet_id': tweet[0],
                    'user_id': tweet[1],
                    'screen_name': tweet[2],
                    'tweet_type': tweet[3],
                    'full_text': tweet[4],
                    'keyword': tweet[5],
                    'tag': tweet[6],
                    'created_at': str(tweet[7]),
                    'geo': tweet[8],
                    'lang': tweet[9],
                    'retweet_count': tweet[10],
                    'favorite_count': tweet[11],
                    'collected_by': tweet[12],
                    'emoji_flag': tweet[13],
                    'emoji_list': tweet[14],
                    'hashtag_flag': tweet[15],
                    'retweeted': tweet[16]
                })
                report_ids.append({
                    'tweet_id': tweet[0],
                    'user_id': tweet[1]
                })
            if self.ACCOUNT_TYPE is not None:
                user_id = []
                tweet_data_temp = []
                report_ids_temp = []
                for user_info in select_executor.select_users_by_type(self.ACCOUNT_TYPE):
                    user_id.append(user_info[0])
                for tweet in tweet_data:
                    if tweet['user_id'] in user_id:
                        tweet_data_temp.append(tweet)
                for ids in report_ids:
                    if ids['user_id'] in user_id:
                        report_ids_temp.append(ids)

                return report_ids_temp, tweet_data_temp
            else:
                return report_ids, tweet_data
        else:
            user_id = []
            for user_info in select_executor.select_users_by_type(self.ACCOUNT_TYPE):
                user_id.append([user_info[0]])
            for tweet in select_executor.select_tweets_by_user_id(user_id):
                tweet_data.append({
                    'tweet_id': tweet[0],
                    'user_id': tweet[1],
                    'screen_name': tweet[2],
                    'tweet_type': tweet[3],
                    'full_text': tweet[4],
                    'keyword': tweet[5],
                    'tag': tweet[6],
                    'created_at': str(tweet[7]),
                    'geo': tweet[8],
                    'lang': tweet[9],
                    'retweet_count': tweet[10],
                    'favorite_count': tweet[11],
                    'collected_by': tweet[12],
                    'emoji_flag': tweet[13],
                    'emoji_list': tweet[14],
                    'hashtag_flag': tweet[15],
                    'retweeted': tweet[16]
                })
                report_ids.append({
                    'tweet_id': tweet[0],
                    'user_id': tweet[1]
                })
            return report_ids, tweet_data

    def create_report(self):
        report_ids, tweet_data = self.fetch_data()
        tweets_count = len(tweet_data)
        tweets_emoji_count = 0
        tweets_emoji = []
        tweets_hashtag_count = 0
        tweets_hashtag = []
        for tweet in tweet_data:
            if tweet['emoji_flag'] == 1:
                tweets_emoji_count += 1
                tweets_emoji.append(tweet['tweet_id'])

            if tweet['hashtag_flag'] == 1:
                tweets_hashtag_count += 1
                tweets_hashtag.append(tweet['tweet_id'])

        report = {
            'tweets_count': tweets_count,
            'tweets_emoji_count': tweets_emoji_count,
            'tweets_hashtag_count': tweets_hashtag_count,
            'tweets_emoji': tweets_emoji,
            'tweets_hashtag': tweets_hashtag
        }
        return report


# report_creater = ReportCreater(tweet_type=["test", "test2"],
#                                account_type=["test", "test2"])
# report_ids1, tweet_data1 = report_creater.fetch_data()
# print(report_ids1)
# print(tweet_data1)




