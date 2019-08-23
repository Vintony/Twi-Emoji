from django import forms


class SearchCrawlerForm(forms.Form):
    search_query = forms.CharField(
        required=True,
        label="Enter Search Query ",
        error_messages={'required': "Enter the query"})
    language = forms.CharField(
        required=False,
        label="Enter Language ")
    max_tweets = forms.IntegerField(
        required=True,
        label="Enter Max Tweets ",
        error_messages={'required': "Enter the max number of Tweets"})
    tweet_mode = forms.CharField(
        required=True,
        label="Enter Tweet Mode ",
        initial='extended')
