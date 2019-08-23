from django import forms
from .RangedField import *


class AccountsTypeDefinerForm(forms.Form):
    type_name = forms.CharField(
        required=True,
        label="Type Name",
        initial=None
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
    max_age = forms.IntegerField(
        required=False,
        label="Max Account Age (Days)",
        initial=None
    )
    min_age = forms.IntegerField(
        required=False,
        label="Min Account Age (Days)",
        initial=None
    )
    follower_range = RangeField(forms.IntegerField, required=False)
    follow_range = RangeField(forms.IntegerField, required=False)
    status_range = RangeField(forms.IntegerField, required=False)
    verified = forms.ChoiceField(
        required=False,
        label="Verified Account",
        choices=[(True, 'True'), (False, 'False'), (None, 'Ignore')]
    )

