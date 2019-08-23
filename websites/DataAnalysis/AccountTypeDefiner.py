from datetime import datetime

from ..SqlExecutor.SelectSqlExecutor import *
from ..SqlExecutor.UpdateSqlExecutor import *


class AccountTypeDefiner(object):
    def __init__(self, type_name, required_keywords=None, optional_keywords=None, lang=None, max_age=None, min_age=None,
                 follower_range=None, follow_range=None, status_range=None, verified=None):
        """
        AccountTypeDefiner: accept parameters to indicate account's type
        :param type_name: AccountType Name
        :param required_keywords: list of keyword(s) that Account(Tweeter)'s description must have all keywords
        :param optional_keywords: list of keyword(s) that Account(Tweeter)'s description must have at least one of keywords
        :param lang: language of the Account
        :param max_age: max age of the Account (calculate by system_time - created_at)
        :param min_age: min age of the Account
        :param follower_range: Account's followers range: None for no requirement or
                              [min, max] for followers between min and max
        :param follow_range: Account's followings range: None for no requirement or
                                [min. max] for following between min and max
        :param status_range: Account's statuses range: None for no requirements or
                                [min, max] for statuses between min and max
        :param verified: Account is verified or not
                        True ----- only verified account
                        False ---- only unverified account
                        None ----- no requirement
        """
        self.REQUIRED_KEYWORDS = required_keywords
        self.OPTIONAL_KEYWORDS = optional_keywords
        self.LANG = lang
        self.MAX_AGE = max_age
        self.MIN_AGE = min_age
        self.FOLLOWER_RANGE = follower_range
        self.FOLLOW_RANGE = follow_range
        self.STATUS_RANGE = status_range
        self.VERIFIED = verified
        self.type_name = type_name
        self.select_executor = SelectSqlExecutor()
        self.update_executor = UpdateSqlExecutor()

    def define_accounts_type(self, list_of_ids=None):
        if list_of_ids:
            users = self.select_executor.select_users_by_id(list_of_ids)
            count = 0
            for USER in users:
                legal_flag = True
                user_id = USER[0]
                screen_name = USER[1]
                description = USER[2]
                account_type = USER[3]
                tag = USER[4]
                location = USER[5]
                followers_count = USER[6]
                follows_count = USER[7]
                lang = USER[8]
                created_at = USER[9]
                verified = USER[10]
                statuses_count = USER[11]

                if legal_flag and self.REQUIRED_KEYWORDS is not None:
                    for keyword in self.REQUIRED_KEYWORDS:
                        if description.count(keyword) < 1:
                            legal_flag = False
                            break

                if legal_flag and self.OPTIONAL_KEYWORDS is not None:
                    legal_flag = False
                    for keyword in self.OPTIONAL_KEYWORDS:
                        if description.count(keyword) >= 1:
                            legal_flag = True
                            break

                if legal_flag and self.LANG is not None:
                    if lang != self.LANG:
                        legal_flag = False

                if created_at:
                    age = ((datetime.now() - datetime.strptime(str(created_at),
                                                               '%Y-%m-%d %H:%M:%S')).days)
                    if legal_flag and self.MAX_AGE is not None:
                        if age > self.MAX_AGE:
                            legal_flag = False

                    if legal_flag and self.MIN_AGE is not None:
                        if age < self.MIN_AGE:
                            legal_flag = False
                else:
                    if self.MAX_AGE is not None or self.MIN_AGE is not None:
                        legal_flag = False

                if legal_flag and self.FOLLOWER_RANGE is not None:
                    if not (self.FOLLOWER_RANGE[0] < followers_count < self.FOLLOWER_RANGE[1]):
                        legal_flag = False

                if legal_flag and self.FOLLOW_RANGE is not None:
                    if not (self.FOLLOW_RANGE[0] < follows_count < self.FOLLOW_RANGE[1]):
                        legal_flag = False

                if legal_flag and self.STATUS_RANGE is not None:
                    if not (self.STATUS_RANGE[0] < statuses_count < self.STATUS_RANGE[1]):
                        legal_flag = False

                if legal_flag and self.VERIFIED is not None:
                    if self.VERIFIED and not verified:
                        legal_flag = False
                    if not self.VERIFIED and verified:
                        legal_flag = False

                if legal_flag:
                    # print("update user " + str(user_id) + " " + self.type_name)
                    count += self.update_executor.update_user_by_id(update_id=user_id, account_type=self.type_name)
                else:
                    pass
            return count

    def close(self):
        self.select_executor.close()
        self.update_executor.close()


# typeDefiner = AccountTypeDefiner("correct", ["Manchester", "Football"], ["player", "man", "woman"], "en")
# typeDefiner.define_accounts_type([1, 2, 3, 4])
