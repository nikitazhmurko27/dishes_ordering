from django import forms
from django.forms import ModelForm
from .models import OrderIngredients
from django.core.exceptions import ValidationError
from datetime import datetime


order_choices = (('DESC', 'DESC'), ('ASC', 'ASC'))


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].widget.attrs.update({'class': 'disabled-select'})

    class Meta:
        model = OrderIngredients
        fields = ('ingredient', 'amount')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        min_amount = 1
        if amount < min_amount:
            raise ValidationError(f'The amount should not be less than {min_amount}')
        return amount


class DishFilterForm(forms.Form):
    search_str = forms.CharField(label='Search', max_length=128, required=False)
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    order_by = forms.ChoiceField(choices=order_choices, required=False)

    def clean_search_str(self):
        search_str = self.cleaned_data['search_str']
        max_len = 128
        if len(search_str) > max_len:
            raise ValidationError(f'The search string should not be more than {max_len}')
        return search_str

    def clean_date_to(self):
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']

        if date_from is None or date_to is None:
            return date_to

        if isinstance(date_from, str):
            date_from = datetime.strptime(date_from, '%d/%m/%y')
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to, '%d/%m/%y')

        if date_from > date_to:
            raise ValidationError(f'The "Date From" should not be more than "Date To"')
        return date_to
