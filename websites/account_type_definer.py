from .DataAnalysis.AccountTypeDefiner import *
from .SqlExecutor.SelectSqlExecutor import *


def accounts_type_definer(definer_para):
    result = {}
    type_definer = AccountTypeDefiner(
        type_name=definer_para['type_name'],
        required_keywords=definer_para['required_keywords'],
        optional_keywords=definer_para['optional_keywords'],
        lang=definer_para['lang'],
        max_age=definer_para['max_age'],
        min_age=definer_para['min_age'],
        follower_range=definer_para['follower_range'],
        follow_range=definer_para['follow_range'],
        status_range=definer_para['status_range'],
        verified=definer_para['verified']
    )
    user_id = []
    executor = SelectSqlExecutor()
    executor.connect()
    for ID in executor.select_all_users_id():
        user_id.append(ID[0])
    result['account_affected'] = type_definer.define_accounts_type(user_id)
    result['type_name'] = definer_para['type_name']
    return result
