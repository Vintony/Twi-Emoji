from .DataCrawler.StreamCrawler import *
from .DataCrawler.CrawlerRuleDefiner import *
from .DataProcessor.ExtractUsers import *
from .DataProcessor.RawTweetsFormator import *


def stream_crawling(stream_para, rule_para=None):
    result = {}

    crawler = StreamCrawler(
        lang=stream_para['lang'],
        retweeted=stream_para['retweeted'],
        track_words=stream_para['track_words'],
        max_tweets=stream_para['max_tweets']
    )
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

    while True:
        crawler.crawling()
        if crawler.get_streaming_tweets_count() >= stream_para['max_tweets']:
            break
        result['tweets_collected'] = crawler.get_streaming_tweets_count()

    data = crawler_rule.filter(crawler.get_streaming_tweets())
    insert_executor = InsertSqlExecutor()
    result['users_created'] = insert_executor.insert_users(data=get_user_data_from_tweets(data))
    tweets_data, emoji_stat, emoji_table = raw_tweets_formator(data,
                                                               tweet_type='test',
                                                               collected_by=stream_para['track_words'])
    result['tweets_inserted'] = insert_executor.insert_tweets(data=tweets_data)
    result['emoji_table_count'] = emoji_table
    print(dict(emoji_stat))
    result['emoji_stat'] = dict(emoji_stat)
    insert_executor.close()
    return result
