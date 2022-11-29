from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.forms import formset_factory


class CatalogForm(forms.Form):
    # selected = forms.BooleanField(label="Show all fields", required=False)
    # name = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 1}), label="Name", required=False)
    # description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 1}), label="Description", required=False)
    # price = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 1}), label="Price", required=False)
    amount = forms.IntegerField(label='', initial=0, required=False)  # label="Amount of items",


CatalogTableFormSet = formset_factory(CatalogForm, extra=Item.objects.all().count())


class PaymentCurrency(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Payment currency",
                                      initial=1, empty_label=None, required=False)
