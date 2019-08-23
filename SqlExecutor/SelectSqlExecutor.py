import pymysql
from ..UserConfig.databaseAuth import *
# from UserConfig.databaseAuth import *


class SelectSqlExecutor(object):
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

    def select_all_users(self):
        cursor = self.db.cursor()
        select_query = "SELECT * FROM users"
        cursor.execute(select_query)
        result = cursor.fetchall()
        return result

    def select_all_users_id(self):
        cursor = self.db.cursor()
        select_query = "SELECT user_id FROM users"
        cursor.execute(select_query)
        result = cursor.fetchall()
        return result

    def select_users_by_id(self, list_of_ids):
        cursor = self.db.cursor()
        format_strings = ','.join(['%s'] * len(list_of_ids))
        select_query = "SELECT * FROM users WHERE user_id IN (%s)"
        cursor.execute(select_query % format_strings, tuple(list_of_ids))
        result = cursor.fetchall()
        return result

    def select_all_tweets(self):
        cursor = self.db.cursor()
        select_query = "SELECT * FROM tweets"
        cursor.execute(select_query)
        result = cursor.fetchall()
        return result

    def select_tweets_by_tweet_id(self, list_of_ids):
        cursor = self.db.cursor()
        format_strings = ','.join(['%s'] * len(list_of_ids))
        select_query = "SELECT * FROM tweets WHERE tweet_id IN (%s)"
        cursor.execute(select_query % format_strings, tuple(list_of_ids))
        result = cursor.fetchall()
        return result

    def select_tweets_by_user_id(self, list_of_ids):
        cursor = self.db.cursor()
        format_strings = ','.join(['%s'] * len(list_of_ids))
        select_query = "SELECT * FROM tweets WHERE user_id IN (%s)"
        cursor.execute(select_query % format_strings, tuple(list_of_ids))
        result = cursor.fetchall()
        return result

    def select_tweets_by_type(self, list_of_types):
        cursor = self.db.cursor()
        format_strings = ','.join(['%s'] * len(list_of_types))
        select_query = "SELECT * FROM tweets WHERE tweet_type IN (%s)"
        cursor.execute(select_query % format_strings, tuple(list_of_types))
        result = cursor.fetchall()
        return result

    def select_users_by_type(self, list_of_types):
        cursor = self.db.cursor()
        format_strings = ','.join(['%s'] * len(list_of_types))
        select_query = "SELECT * FROM users WHERE account_type IN (%s)"
        cursor.execute(select_query % format_strings, tuple(list_of_types))
        result = cursor.fetchall()
        return result

    # def select_tweets_by_tag(self, list_of_tags):
    #     cursor = self.db.cursor()
    #     format_strings = ','.join(['%s'] * len(list_of_tags))
    #     select_query = "SELECT * FROM tweets WHERE tweet_tag IN (%s)"
    #     cursor.execute(select_query % format_strings, tuple(list_of_tags))
    #     result = cursor.fetchall()
    #     return result

# executor = SelectSqlExecutor()
# executor.connect()
# for ID in executor.select_all_users_id():
#     print(ID[0])
# result = executor.select_users_by_id([1, 2])
# for user in result:
#     print(user[0])


# executor = SelectSqlExecutor()
# for tweet in executor.select_tweets_by_type(["test", "test2", "test3"]):
#     print({
#         'tweet_id': tweet[0],
#         'user_id': tweet[1]
#     })
