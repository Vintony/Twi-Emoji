import time


def get_user_data_from_tweets(tweets):
    user_data = []
    for row in tweets:
        data = row['user']
        account_type = "undefined"
        tag = 'undefined'
        user_dict = {
            'user_id': data['id'],
            'screen_name': data['screen_name'],
            'account_type': account_type,
            'description': data['description'],
            'tag': tag,
            'location': data['location'],
            'followers_count': data['followers_count'],
            'follows_count': data['friends_count'],
            'lang': data['lang'],
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
                data['created_at'],
                '%a %b %d %H:%M:%S +0000 %Y')),
            'verified': data['verified'],
            'statuses_count': data['statuses_count']
        }
        user_data.append(user_dict)
    return user_data
