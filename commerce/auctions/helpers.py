from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Helper functions

# Forms
class ListingForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=64,
        required=True,
        widget=forms.TextInput(attrs={
             'class':'form-control col-md-12'
        }))

    startingbid = forms.IntegerField(
        label="Starting Bid",
        required=True,
        widget=forms.TextInput(attrs={
            "class":"form-control"
        })
    )

    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={
            "rows":"10",
            "cols":"10",
            "class":"form-control form-control-lg",
            "style":"top:2rem"
        })
    )

    image = forms.URLField(
        required=False,
        label="Image",
        widget=forms.URLInput(attrs={
            "class":"form-control",
            'placeholder':"URL"
        })
    )

    category = forms.CharField(
        label="Category",
        required=False,
        widget=forms.TextInput(attrs={
             "class":"form-control"
        }
        )
    )

