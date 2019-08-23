from django import forms
from .RangedField import *


class CrawlerRuleDefinerForm(forms.Form):
    rule_flag = forms.ChoiceField(
        required=False,
        label="Enable Crawler Rule",
        choices=[(True, 'Enable'), (False, 'Disable')],
        widget=forms.Select,
        initial=False
    )
    required_keywords = forms.CharField(
        required=False,
        label="Required Keywords (Separated by \";\")",
        initial=None
    )
    optional_keywords = forms.CharField(
        required=False,
        label="Optional Keywords (Separated by \";\")",
        initial=None
    )
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
    has_hashtags = forms.ChoiceField(
        required=False,
        label="Has Hashtags",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')],
        widget=forms.Select,
        initial=None
    )
    has_emojis = forms.ChoiceField(
        required=False,
        label="Has Emojis",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')],
        widget=forms.Select,
        initial=None
    )
    has_mentioned_users = forms.ChoiceField(
        required=False,
        label="Has Mentioned Users",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')],
        widget=forms.Select,
        initial=None
    )
    has_urls = forms.ChoiceField(
        required=False,
        label="Has Urls",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')],
        widget=forms.Select,
        initial=None
    )
    has_symbols = forms.ChoiceField(
        required=False,
        label="Has Symbols",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')],
        widget=forms.Select,
        initial=None
    )
    quote_range = RangeField(forms.IntegerField, required=False)
    reply_range = RangeField(forms.IntegerField, required=False)
    retweet_range = RangeField(forms.IntegerField, required=False)
    favorite_range = RangeField(forms.IntegerField, required=False)



