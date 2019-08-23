from .DataAnalysis.ReportCreater import *


def report_creating(creater_para):
    report_creater = ReportCreater(
        tweet_type=creater_para['tweet_type'],
        account_type=creater_para['account_type'],
        tweet_tag=creater_para['tweet_tag'],
        account_tag=creater_para['account_tag']
    )
    return report_creater.create_report()
