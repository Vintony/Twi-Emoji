from django.http import HttpResponse
from django.shortcuts import render

from .account_type_definer import *
from .data_exporter import *
from .forms.AccountsTypeDefinerForm import *
from .forms.CrawlerRuleDefinerForm import *
from .forms.DataExportForm import *
from .forms.ReportCreaterForm import *
from .forms.SearchCrawlerForm import *
from .forms.StreamCrawlerForm import *
from .forms.UserCrawlerForm import *
from .report_creater import *
from .search_crawler import *
from .stream_crawling import *
from .user_crawler import *


def index(request):
    return render(request, 'base/index.html')


def flag_translator(flag_string):
    if flag_string == "True":
        return True
    elif flag_string == "False":
        return False


def search_crawler_page(request):
    if request.method == 'POST':
        search_crawler_form = SearchCrawlerForm(data=request.POST)
        crawler_rule_definer_form = CrawlerRuleDefinerForm(data=request.POST)
        if search_crawler_form.is_valid():
            crawler_para = {
                'query': search_crawler_form.cleaned_data["search_query"],
                'lang': search_crawler_form.cleaned_data["language"]
                if search_crawler_form.cleaned_data.get("language") else None,
                'max_tweets': search_crawler_form.cleaned_data["max_tweets"],
                'tweet_mode': search_crawler_form.cleaned_data["tweet_mode"]
            }
            if crawler_rule_definer_form.is_valid() and flag_translator(crawler_rule_definer_form.cleaned_data["rule_flag"]):
                rule_para = {
                    'rule_flag': True,
                    'required_keywords': crawler_rule_definer_form.cleaned_data["required_keywords"].split(";")
                    if crawler_rule_definer_form.cleaned_data.get("required_keywords") else None,
                    'optional_keywords': crawler_rule_definer_form.cleaned_data["optional_keywords"].split(";")
                    if crawler_rule_definer_form.cleaned_data.get("optional_keywords") else None,
                    'lang': crawler_rule_definer_form.cleaned_data["language"]
                    if crawler_rule_definer_form.cleaned_data.get("language") else None,
                    'retweeted': flag_translator(crawler_rule_definer_form.cleaned_data["retweeted"])
                    if crawler_rule_definer_form.cleaned_data.get("retweeted") else None,
                    'has_hashtags': flag_translator(crawler_rule_definer_form.cleaned_data["has_hashtags"])
                    if crawler_rule_definer_form.cleaned_data.get("has_hashtags") else None,
                    'has_emojis': flag_translator(crawler_rule_definer_form.cleaned_data["has_emojis"])
                    if crawler_rule_definer_form.cleaned_data.get("has_emojis") else None,
                    'has_user_mentions': flag_translator(crawler_rule_definer_form.cleaned_data["has_mentioned_users"])
                    if crawler_rule_definer_form.cleaned_data.get("has_mentioned_users") else None,
                    'has_urls': flag_translator(crawler_rule_definer_form.cleaned_data["has_urls"])
                    if crawler_rule_definer_form.cleaned_data.get("has_urls") else None,
                    'has_symbols': flag_translator(crawler_rule_definer_form.cleaned_data["has_symbols"])
                    if crawler_rule_definer_form.cleaned_data.get("has_symbols") else None,
                    'quote_range': crawler_rule_definer_form.cleaned_data["tweet_quoted_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_quoted_range") else None,
                    'reply_range': crawler_rule_definer_form.cleaned_data["tweet_replied_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_replied_range") else None,
                    'retweet_range': crawler_rule_definer_form.cleaned_data["tweet_retweet_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_retweet_range") else None,
                    'favorite_range': crawler_rule_definer_form.cleaned_data["tweet_favorite_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_favorite_range") else None,
                }
                result = search_crawling(search_para=crawler_para, rule_para=rule_para)
                return render(request, 'base/crawler_result_page.html', result)

            else:
                result = search_crawling(search_para=crawler_para)
                return render(request, 'base/crawler_result_page.html', result)
        else:
            search_crawler_form = SearchCrawlerForm()
            crawler_rule_definer_form = CrawlerRuleDefinerForm()
            return render(request, 'base/search_crawler_page.html', {'SearchCrawlerForm': search_crawler_form,
                                                                     'CrawlerRuleDefinerForm': crawler_rule_definer_form})
    else:
        search_crawler_form = SearchCrawlerForm()
        crawler_rule_definer_form = CrawlerRuleDefinerForm()
        return render(request, 'base/search_crawler_page.html', {'SearchCrawlerForm': search_crawler_form,
                                                                 'CrawlerRuleDefinerForm': crawler_rule_definer_form})


def user_crawler_page(request):
    if request.method == "POST":
        user_crawler_form = UserCrawlerForm(data=request.POST)
        crawler_rule_definer_form = CrawlerRuleDefinerForm(data=request.POST)
        if user_crawler_form.is_valid():
            crawler_para = {
                'user_id': user_crawler_form.cleaned_data["user_id"].split(";")
                if user_crawler_form.cleaned_data.get("user_id") else None,
                'screen_name': user_crawler_form.cleaned_data["screen_name"].split(";")
                if user_crawler_form.cleaned_data.get("screen_name") else None,
                'max_tweets': user_crawler_form.cleaned_data["max_tweets"]
            }
            if crawler_rule_definer_form.is_valid() and flag_translator(crawler_rule_definer_form.cleaned_data["rule_flag"]):
                rule_para = {
                    'rule_flag': True,
                    'required_keywords': crawler_rule_definer_form.cleaned_data["required_keywords"].split(";")
                    if crawler_rule_definer_form.cleaned_data.get("required_keywords") else None,
                    'optional_keywords': crawler_rule_definer_form.cleaned_data["optional_keywords"].split(";")
                    if crawler_rule_definer_form.cleaned_data.get("optional_keywords") else None,
                    'lang': crawler_rule_definer_form.cleaned_data["language"]
                    if crawler_rule_definer_form.cleaned_data.get("language") else None,
                    'retweeted': flag_translator(crawler_rule_definer_form.cleaned_data["retweeted"])
                    if crawler_rule_definer_form.cleaned_data.get("retweeted") else None,
                    'has_hashtags': flag_translator(crawler_rule_definer_form.cleaned_data["has_hashtags"])
                    if crawler_rule_definer_form.cleaned_data.get("has_hashtags") else None,
                    'has_emojis': flag_translator(crawler_rule_definer_form.cleaned_data["has_emojis"])
                    if crawler_rule_definer_form.cleaned_data.get("has_emojis") else None,
                    'has_user_mentions': flag_translator(crawler_rule_definer_form.cleaned_data["has_mentioned_users"])
                    if crawler_rule_definer_form.cleaned_data.get("has_mentioned_users") else None,
                    'has_urls': flag_translator(crawler_rule_definer_form.cleaned_data["has_urls"])
                    if crawler_rule_definer_form.cleaned_data.get("has_urls") else None,
                    'has_symbols': flag_translator(crawler_rule_definer_form.cleaned_data["has_symbols"])
                    if crawler_rule_definer_form.cleaned_data.get("has_symbols") else None,
                    'quote_range': crawler_rule_definer_form.cleaned_data["tweet_quoted_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_quoted_range") else None,
                    'reply_range': crawler_rule_definer_form.cleaned_data["tweet_replied_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_replied_range") else None,
                    'retweet_range': crawler_rule_definer_form.cleaned_data["tweet_retweet_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_retweet_range") else None,
                    'favorite_range': crawler_rule_definer_form.cleaned_data["tweet_favorite_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_favorite_range") else None,
                }
                result = user_crawling(user_para=crawler_para, rule_para=rule_para)
                return render(request, 'base/crawler_result_page.html', result)

            else:
                result = user_crawling(user_para=crawler_para)
                return render(request, 'base/crawler_result_page.html', result)
        else:
            user_crawler_form = UserCrawlerForm()
            crawler_rule_definer_form = CrawlerRuleDefinerForm()
            return render(request, 'base/user_crawler_page.html', {'UserCrawlerForm': user_crawler_form,
                                                                   'CrawlerRuleDefinerForm': crawler_rule_definer_form})
    else:
        user_crawler_form = UserCrawlerForm()
        crawler_rule_definer_form = CrawlerRuleDefinerForm()
        return render(request, 'base/user_crawler_page.html', {'UserCrawlerForm': user_crawler_form,
                                                               'CrawlerRuleDefinerForm': crawler_rule_definer_form})


def stream_crawler_page(request):
    if request.method == 'POST':
        stream_crawler_form = StreamCrawlerForm(data=request.POST)
        crawler_rule_definer_form = CrawlerRuleDefinerForm(data=request.POST)
        if stream_crawler_form.is_valid():
            crawler_para = {
                'lang': stream_crawler_form.cleaned_data["language"],
                'retweeted': flag_translator(stream_crawler_form.cleaned_data["retweeted"])
                if stream_crawler_form.cleaned_data.get("retweeted") else None,
                'track_words': stream_crawler_form.cleaned_data["track_words"].split(";")
                if stream_crawler_form.cleaned_data.get("track_words") else None,
                'max_tweets': stream_crawler_form.cleaned_data["max_tweets"]
                if stream_crawler_form.cleaned_data.get("max_tweets") else None
            }
            if crawler_rule_definer_form.is_valid() and flag_translator(crawler_rule_definer_form.cleaned_data["rule_flag"]):
                rule_para = {
                    'rule_flag': True,
                    'required_keywords': crawler_rule_definer_form.cleaned_data["required_keywords"].split(";")
                    if crawler_rule_definer_form.cleaned_data.get("required_keywords") else None,
                    'optional_keywords': crawler_rule_definer_form.cleaned_data["optional_keywords"].split(";")
                    if crawler_rule_definer_form.cleaned_data.get("optional_keywords") else None,
                    'lang': crawler_rule_definer_form.cleaned_data["language"]
                    if crawler_rule_definer_form.cleaned_data.get("language") else None,
                    'retweeted': flag_translator(crawler_rule_definer_form.cleaned_data["retweeted"])
                    if crawler_rule_definer_form.cleaned_data.get("retweeted") else None,
                    'has_hashtags': flag_translator(crawler_rule_definer_form.cleaned_data["has_hashtags"])
                    if crawler_rule_definer_form.cleaned_data.get("has_hashtags") else None,
                    'has_emojis': flag_translator(crawler_rule_definer_form.cleaned_data["has_emojis"])
                    if crawler_rule_definer_form.cleaned_data.get("has_emojis") else None,
                    'has_user_mentions': flag_translator(crawler_rule_definer_form.cleaned_data["has_mentioned_users"])
                    if crawler_rule_definer_form.cleaned_data.get("has_mentioned_users") else None,
                    'has_urls': flag_translator(crawler_rule_definer_form.cleaned_data["has_urls"])
                    if crawler_rule_definer_form.cleaned_data.get("has_urls") else None,
                    'has_symbols': flag_translator(crawler_rule_definer_form.cleaned_data["has_symbols"])
                    if crawler_rule_definer_form.cleaned_data.get("has_symbols") else None,
                    'quote_range': crawler_rule_definer_form.cleaned_data["tweet_quoted_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_quoted_range") else None,
                    'reply_range': crawler_rule_definer_form.cleaned_data["tweet_replied_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_replied_range") else None,
                    'retweet_range': crawler_rule_definer_form.cleaned_data["tweet_retweet_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_retweet_range") else None,
                    'favorite_range': crawler_rule_definer_form.cleaned_data["tweet_favorite_range"]
                    if crawler_rule_definer_form.cleaned_data.get("tweet_favorite_range") else None,
                }
                result = stream_crawling(stream_para=crawler_para, rule_para=rule_para)
                return render(request, 'base/crawler_result_page.html', result)

            else:
                result = stream_crawling(stream_para=crawler_para)
                return render(request, 'base/crawler_result_page.html', result)
        else:
            stream_crawler_form = StreamCrawlerForm()
            crawler_rule_definer_form = CrawlerRuleDefinerForm()
            return render(request, 'base/stream_crawler_page.html', {'StreamCrawlerForm': stream_crawler_form,
                                                                     'CrawlerRuleDefinerForm': crawler_rule_definer_form})
    else:
        stream_crawler_form = StreamCrawlerForm()
        crawler_rule_definer_form = CrawlerRuleDefinerForm()
        return render(request, 'base/stream_crawler_page.html', {'StreamCrawlerForm': stream_crawler_form,
                                                                 'CrawlerRuleDefinerForm': crawler_rule_definer_form})


def report_page(request):
    if request.method == 'POST':
        report_creater_form = ReportCreaterForm(data=request.POST)
        if report_creater_form.is_valid():
            creater_para = {
                'tweet_type': report_creater_form.cleaned_data['tweet_type']
                if report_creater_form.cleaned_data.get("tweet_type") else None,
                'account_type': report_creater_form.cleaned_data['account_type']
                if report_creater_form.cleaned_data.get("account_type") else None,
                'tweet_tag': report_creater_form.cleaned_data['tweet_tag']
                if report_creater_form.cleaned_data.get("tweet_tag") else None,
                'account_tag': report_creater_form.cleaned_data['account_tag']
                if report_creater_form.cleaned_data.get("account_tag") else None
            }
            result = report_creating(creater_para)
            return render(request, 'base/report_result_page.html', result)
        else:
            report_creater_form = ReportCreaterForm()
            return render(request, 'base/report_creater_page.html', {'ReportCreaterForm': report_creater_form})
    else:
        report_creater_form = ReportCreaterForm()
        return render(request, 'base/report_creater_page.html', {'ReportCreaterForm': report_creater_form})


def accounts_type_definer_page(request):
    if request.method == 'POST':
        accounts_type_definer_form = AccountsTypeDefinerForm(data=request.POST)
        if accounts_type_definer_form.is_valid():
            definer_para = {
                'type_name': accounts_type_definer_form.cleaned_data['type_name'],
                'required_keywords': accounts_type_definer_form.cleaned_data['required_keywords'].split(";")
                if accounts_type_definer_form.cleaned_data.get("required_keywords") else None,
                'optional_keywords': accounts_type_definer_form.cleaned_data['optional_keywords'].split(";")
                if accounts_type_definer_form.cleaned_data.get("optional_keywords") else None,
                'lang': accounts_type_definer_form.cleaned_data['language']
                if accounts_type_definer_form.cleaned_data.get("language") else None,
                'max_age': accounts_type_definer_form.cleaned_data['max_age']
                if accounts_type_definer_form.cleaned_data.get("max_age") else None,
                'min_age': accounts_type_definer_form.cleaned_data['min_age']
                if accounts_type_definer_form.cleaned_data.get("min_age") else None,
                'follower_range': accounts_type_definer_form.cleaned_data['follower_range']
                if accounts_type_definer_form.cleaned_data.get("follower_range") else None,
                'follow_range': accounts_type_definer_form.cleaned_data['follow_range']
                if accounts_type_definer_form.cleaned_data.get("follow_range") else None,
                'status_range': accounts_type_definer_form.cleaned_data['status_range']
                if accounts_type_definer_form.cleaned_data.get("status_range") else None,
                'verified': flag_translator(accounts_type_definer_form.cleaned_data['verified'])
                if accounts_type_definer_form.cleaned_data.get("verified") else None
            }
            result = accounts_type_definer(definer_para=definer_para)
            return render(request, 'base/definer_result_page.html', result)

        else:
            accounts_type_definer_form = AccountsTypeDefinerForm()
            return render(request, 'base/accounts_type_definer_page.html',
                          {'AccountsTypeDefinerForm': accounts_type_definer_form})

    else:
        accounts_type_definer_form = AccountsTypeDefinerForm()
        return render(request, 'base/accounts_type_definer_page.html', {'AccountsTypeDefinerForm': accounts_type_definer_form})


def data_export_page(request):
    if request.method == "POST":
        data_export_form = DataExportForm(data=request.POST)
        if data_export_form.is_valid():
            export_para = {
                'tweet_type': data_export_form.cleaned_data['tweet_type']
                if data_export_form.cleaned_data.get("tweet_type") else None,
                'account_type': data_export_form.cleaned_data['account_type']
                if data_export_form.cleaned_data.get("account_type") else None,
                'tweet_tag': data_export_form.cleaned_data['tweet_tag']
                if data_export_form.cleaned_data.get("tweet_tag") else None,
                'account_tag': data_export_form.cleaned_data['account_tag']
                if data_export_form.cleaned_data.get("account_tag") else None
            }
            data_exporting(export_para)
            return index(request)
        pass
    else:
        data_export_form = DataExportForm()
        return render(request, 'base/data_export_page.html', {'DataExportForm': data_export_form})
