import time


# translate created_at info to mysql timestamp format
def time_translator(tweets):
    """
    :param tweets: tweet data dict
    :return: tweet data dict
    """
    for tweet in tweets:
        created_at_info = tweet['created_at']
        created_at_info = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at_info,
                                                                           '%a %b %d %H:%M:%S +0000 %Y'))
        tweet['created_at'] = created_at_info
