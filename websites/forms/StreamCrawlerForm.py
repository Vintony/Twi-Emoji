from django import forms


class StreamCrawlerForm(forms.Form):
    language = forms.CharField(
        required=False,
        label="Language",
        initial=None
    )
    retweeted = forms.ChoiceField(
        required=False,
        label="Retweeted",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')],
        widget=forms.Select,
        initial=None
    )
    track_words = forms.CharField(
        required=True,
        label="Tracked Keywords (Separated by \";\")",
        initial=None
    )
    max_tweets = forms.IntegerField(
        required=False,
        label="Enter Max Tweets",
        initial=None
    )
