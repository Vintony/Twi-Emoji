from django import forms


class ReportCreaterForm(forms.Form):
    tweet_type = forms.CharField(
        required=False,
        label="Enter the Tweet Types (Separated by \";\")",
        initial=None
    )
    account_type = forms.CharField(
        required=False,
        label="Enter the Account Types (Separated by \";\")",
        initial=None
    )
    tweet_tag = forms.CharField(
        required=False,
        label="Enter the Tweet Tags (Separated by \";\")",
        initial=None
    )
    account_tag = forms.CharField(
        required=False,
        label="Enter the Account Tags (Separated by \";\")",
        initial=None
    )
