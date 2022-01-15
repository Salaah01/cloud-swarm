from django import forms


class PaymentForm(forms.Form):
    name = forms.CharField(max_length=255)
    address_line_1 = forms.CharField(max_length=255)
    address_line_2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
