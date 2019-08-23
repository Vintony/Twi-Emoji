import pymysql
from ..UserConfig.databaseAuth import *


class UpdateSqlExecutor(object):
    def __init__(self):
        self.PORT = port
        self.USER = user
        self.PASSWD = passwd
        self.SCHEMA = schema
        self.db = self.connect()

    def connect(self):
        return pymysql.connect(port=self.PORT, user=self.USER, passwd=self.PASSWD, db=self.SCHEMA, charset="utf8mb4")

    def close(self):
        self.db.close()

    def update_user_by_id(self, update_id, user_id=None, screen_name=None, account_type=None, tag=None, location=None,
                          followers_count=None, follows_count=None, lang=None, created_at=None, verified=None,
                          statuses_count=None):
        cursor = self.db.cursor()
        update_query = "UPDATE users SET %s WHERE user_id = " + str(update_id)
        set_list = []
        value_list = []
        if user_id:
            set_list.append('user_id = %s')
            value_list.append(user_id)
        if screen_name:
            set_list.append('screen_name = %s')
            value_list.append(screen_name)
        if account_type:
            set_list.append('account_type = %s')
            value_list.append(account_type)
        if tag:
            set_list.append('tag = %s')
            value_list.append(tag)
        if location:
            set_list.append('location = %s')
            value_list.append(location)
        if followers_count:
            set_list.append('followers_count = %s')
            value_list.append(followers_count)
        if follows_count:
            set_list.append('follows_count = %s')
            value_list.append(follows_count)
        if lang:
            set_list.append('lang = %s')
            value_list.append(lang)
        if created_at:
            set_list.append('created_at = %s')
            value_list.append(created_at)
        if verified:
            set_list.append('verified = %s')
            value_list.append(verified)
        if statuses_count:
            set_list.append('statuses_count = %s')
            value_list.append(statuses_count)
        set_query = ', '.join(['%s'] * len(set_list))
        set_query = set_query % tuple(set_list)
        cursor.execute(update_query % set_query, tuple(value_list))
        self.db.commit()
        return cursor.rowcount

    def update_tweet_by_id(self, update_id, tweet_id=None, user_id=None, screen_name=None, tweet_type=None, full_text=None,
                           keyword=None, tag=None, created_at=None, geo=None, lang=None, retweet_count=None, favorite_count=None,
                           collected_by=None, emoji_flag=None, hashtag_flag=None, retweeted_flag=None):
        cursor = self.db.cursor()
        update_query = "UPDATE tweets SET %s WHERE tweet_id = " + str(update_id)
        set_list = []
        value_list = []
        if tweet_id:
            set_list.append('tweet_id = %s')
            value_list.append(tweet_id)
        if user_id:
            set_list.append('user_id = %s')
            value_list.append(user_id)
        if screen_name:
            set_list.append('screen_name = %s')
            value_list.append(screen_name)
        if tweet_type:
            set_list.append('tweet_type = %s')
            value_list.append(tweet_type)
        if full_text:
            set_list.append('full_text = %s')
            value_list.append(full_text)
        if keyword:
            set_list.append('keyword = %s')
            value_list.append(keyword)
        if tag:
            set_list.append('tag = %s')
            value_list.append(tag)
        if created_at:
            set_list.append('created_at = %s')
            value_list.append(created_at)
        if geo:
            set_list.append('geo = %s')
            value_list.append(geo)
        if lang:
            set_list.append('lang = %s')
            value_list.append(lang)
        if retweet_count:
            set_list.append('retweet_count = %s')
            value_list.append(retweet_count)
        if favorite_count:
            set_list.append('favorite_count = %s')
            value_list.append(favorite_count)
        if collected_by:
            set_list.append('collected_by = %s')
            value_list.append(collected_by)
        if emoji_flag:
            set_list.append('emoji_flag = %s')
            value_list.append(emoji_flag)
        if hashtag_flag:
            set_list.append('hashtag_flag = %s')
            value_list.append(hashtag_flag)
        if retweeted_flag:
            set_list.append('retweeted_flag = %s')
            value_list.append(retweeted_flag)

        set_query = ', '.join(['%s'] * len(set_list))
        set_query = set_query % tuple(set_list)
        cursor.execute(update_query % set_query, tuple(value_list))
        self.db.commit()
        return cursor.rowcount

# executor = UpdateSqlExecutor()
# executor.update_user_by_id(1, user_id=2, screen_name="test3", account_type="test35", tag="test45")
# executor.close()
