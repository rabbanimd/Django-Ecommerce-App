from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Address
payment_option=(
    ('S','stripe'),
    ('P','paypal'),
    ('V' ,'Visa')
)
class checkout_form(forms.Form):
    fields =['full_name','address','address2','country','city','state','zip']
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'usha'}))
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'usha'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'usha'}))
    country=CountryField(blank_label='(select country)').formfield(
        required=False,widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    state=forms.CharField(required=False)
    city=forms.CharField(required=False)
    zip = forms.IntegerField(required=False)
    # save_info=forms.BooleanField(widget=forms.CheckboxInput())
    payment_op=forms.ChoiceField(widget=forms.RadioSelect,choices=payment_option)
    # set_default_shipping = forms.BooleanField(required=False)
    # use_default_shipping = forms.BooleanField(required=False)
    # set_default_billing = forms.BooleanField(required=False)
    # use_default_billing = forms.BooleanField(required=False)

class SearchForm(forms.Form):
    query=forms.CharField(max_length=100)
    catid=forms.IntegerField()
