from django import forms


class UserCrawlerForm(forms.Form):
    user_id = forms.CharField(
        required=False,
        label="Enter User Id (Separated by \";\")"
    )
    screen_name = forms.CharField(
        required=False,
        label="Enter Screen Name (Separated by \";\")"
    )
    max_tweets = forms.IntegerField(
        required=True,
        label="Enter Max Tweets"
    )

