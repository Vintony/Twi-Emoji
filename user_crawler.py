from .DataCrawler.CrawlerRuleDefiner import *
from .DataCrawler.UserCrawler import *
from .DataProcessor.ExtractUsers import *
from .DataProcessor.RawTweetsFormator import *


def user_crawling(user_para, rule_para=None):
    result = {}
    tweets_collected_count = 0
    tweets_inserted_count = 0
    users_created_count = 0
    emoji_table_count = 0
    emoji_stat = Counter({})
    crawled_users = []
    user_id = user_para['user_id']
    user_screen_name = user_para['screen_name']
    max_tweet = user_para['max_tweets']
    insert_executor = InsertSqlExecutor()

    if rule_para:
        if rule_para['rule_flag']:
            crawler_rule = CrawlerRuleDefiner(required_keywords=rule_para['required_keywords'],
                                              optional_keywords=rule_para['optional_keywords'],
                                              lang=rule_para['lang'],
                                              retweeted=rule_para['retweeted'],
                                              has_hashtags=rule_para['has_hashtags'],
                                              has_emojis=rule_para['has_emojis'],
                                              has_user_mentions=rule_para['has_user_mentions'],
                                              has_urls=rule_para['has_urls'],
                                              has_symbols=rule_para['has_symbols'],
                                              quote_range=rule_para['quote_range'],
                                              reply_range=rule_para['reply_range'],
                                              retweet_range=rule_para['retweet_range'],
                                              favorite_range=rule_para['favorite_range'])
        else:
            crawler_rule = CrawlerRuleDefiner()
    else:
        crawler_rule = CrawlerRuleDefiner()

    if user_id:
        for uid in user_id:
            try:
                crawler = UserCrawler(
                    user_id=int(uid),
                    screen_name=None,
                    max_tweets=max_tweet
                )
                crawler.crawling()
                tweets_collected_count += crawler.get_user_tweets_number()
                data = crawler_rule.filter(crawler.get_user_tweets())
                crawled_users.append(crawler.get_user_tweets()[0]._json['user']['screen_name'])
                users_created_count += insert_executor.insert_users(data=get_user_data_from_tweets(data))
                tweets_data, emoji_stat_temp, emoji_table_temp = raw_tweets_formator(
                    data,
                    tweet_type='test',
                    collected_by="user_id" + uid
                )
                emoji_stat += emoji_stat_temp
                emoji_table_count += emoji_table_temp
                tweets_inserted_count += insert_executor.insert_tweets(data=tweets_data)
            except Exception as e:
                print(e)
    if user_screen_name:
        for name in user_screen_name:
            if name not in crawled_users:
                try:
                    crawler = UserCrawler(
                        user_id=None,
                        screen_name=name,
                        max_tweets=max_tweet
                    )
                    crawler.crawling()
                    tweets_collected_count += crawler.get_user_tweets_number()
                    data = crawler_rule.filter(crawler.get_user_tweets())
                    users_created_count += insert_executor.insert_users(data=get_user_data_from_tweets(data))
                    tweets_data, emoji_stat_temp, emoji_table_temp = raw_tweets_formator(
                        data,
                        tweet_type='test',
                        collected_by="user_id" + name
                    )
                    emoji_stat += emoji_stat_temp
                    emoji_table_count += emoji_table_temp
                    tweets_inserted_count += insert_executor.insert_tweets(data=tweets_data)
                except Exception as e:
                    print(e)
            else:
                pass

    result['tweets_collected'] = tweets_collected_count
    result['users_created'] = users_created_count
    result['tweets_inserted'] = tweets_inserted_count
    result['emoji_stat'] = dict(emoji_stat)
    result['emoji_table_count'] = emoji_table_count
    insert_executor.close()

    return result



