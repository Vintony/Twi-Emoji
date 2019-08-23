from geopy.geocoders import Nominatim


# translate geo to detail address
def geo_translator(tweets):
    """
    :param tweets: tweet data dict
    :return: tweet data dict
    """
    for tweet in tweets:
        if tweet['geo']:
            geo_info = tweet['geo']['coordinates']
            geo_locator = Nominatim(user_agent="a")
            # geo_info[0] : latitude, geo_info[1] : longitude
            location = geo_locator.reverse(str(geo_info[0]) + ", " + str(geo_info[1]))
            tweet['geo'] = location.address
        else:
            pass
