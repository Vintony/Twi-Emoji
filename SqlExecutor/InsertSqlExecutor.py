import pymysql

from ..UserConfig.databaseAuth import *


class InsertSqlExecutor(object):
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

    def insert_emoji(self, tweet_id, user_id, emoji_definition, usage_count):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'"
                       .format(emoji_definition.replace('\'', '\'\'')))
        if cursor.fetchone()[0] == 1:
            try:
                cursor.execute("""INSERT INTO `{0}` (tweet_id, user_id, usage_count) VALUES (%s, %s, %s)"""
                               .format(emoji_definition.replace('\'', '\'\'')),
                               (tweet_id, user_id, usage_count))
                self.db.commit()
                return 0
            except Exception as e:
                print(e)
        else:
            try:
                cursor.execute(
                    """
                CREATE TABLE `{0}` (`tweet_id` bigint(20) NOT NULL,
                `user_id` bigint(20) NOT NULL,`usage_count` int(11) DEFAULT '0',
                PRIMARY KEY (`tweet_id`,`user_id`)) 
                ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                    """.format(emoji_definition.replace('\'', '\'\'')))

                cursor.execute("""INSERT INTO `{0}` (tweet_id, user_id, usage_count) VALUES (%s, %s, %s)"""
                               .format(emoji_definition.replace('\'', '\'\'')),
                               (tweet_id, user_id, usage_count))
                self.db.commit()
                return 1
            except Exception as e:
                print(e)
                return 0

    def insert_tweets(self, data):
        cursor = self.db.cursor()
        rows_count = 0
        for row in data:
            insert_query = "INSERT INTO tweets(" \
                           "tweet_id, user_id, screen_name, tweet_type, full_text, " \
                           "keyword, tag, created_at, geo, lang, " \
                           "retweet_count, favorite_count, collected_by, " \
                           "emoji_flag, emoji_list, hashtag_flag, retweeted) values " \
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(insert_query, (
                    row['tweet_id'], row['user_id'], row['screen_name'], row['tweet_type'],
                    row['full_text'], row['keyword'], row['tag'], row['created_at'],
                    row['geo'], row['lang'], row['retweet_count'], row['favorite_count'],
                    row['collected_by'], row['emoji_flag'], row['emoji_list'], row['hashtag_flag'], row['retweeted']
                ))
                self.db.commit()
                rows_count += cursor.rowcount
            except Exception as e:
                print(e)
        return rows_count

    def insert_users(self, data):
        cursor = self.db.cursor()
        rows_count = 0
        for row in data:
            insert_query = "INSERT INTO users(" \
                           "user_id, screen_name, description, account_type," \
                           "tag, location, followers_count, follows_count," \
                           "lang, created_at, verified, statuses_count)" \
                           "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(insert_query, (
                    row['user_id'], row['screen_name'], row['description'], row['account_type'],
                    row['tag'], row['location'], row['followers_count'], row['follows_count'],
                    row['lang'], row['created_at'], row['verified'], row['statuses_count']
                ))
                self.db.commit()
                rows_count += cursor.rowcount
            except Exception as e:
                print(e)

        return rows_count
