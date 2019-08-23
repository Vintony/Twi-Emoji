from .DataAnalysis.DataExporter import *


def data_exporting(export_para):
    data_exporter = DataExporter(
        tweet_type=export_para['tweet_type'],
        tweet_tag=export_para['tweet_tag'],
        account_type=export_para['account_type'],
        account_tag=export_para['account_tag']
    )
    data_exporter.create_json()
