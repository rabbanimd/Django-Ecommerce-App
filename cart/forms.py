from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

payment_option=(
    ('S','stripe'),
    ('P','paypal'),
    ('V' ,'Visa')
)
class checkout_form(forms.Form):

    ship_address=forms.CharField(widget=forms.TextInput(attrs={
        'placholder':'1234 Main St'
    }))
    ship_address2=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder':'h.no-79 Raj Mahal'
    })
                                 )
    ship_country=CountryField(blank_label='(select country)').formfield(
        required=False,widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    ship_zip=forms.CharField()
    ship_state=forms.CharField()
    ship_city=forms.CharField()
    bill_address = forms.CharField(widget=forms.TextInput(attrs={
        'placholder': '1234 Main St'
    }))
    bill_address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'h.no-79 Raj Mahal'
    })
                                    )
    bill_country = CountryField(blank_label='(select country)').formfield(
        required=False, widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        }))
    bill_zip = forms.CharField()
    same_billing_add=forms.BooleanField(required=False)
    save_info=forms.BooleanField(widget=forms.CheckboxInput())
    payment_op=forms.ChoiceField(widget=forms.RadioSelect,choices=payment_option)

    # set_default_shipping = forms.BooleanField(required=False)
    # use_default_shipping = forms.BooleanField(required=False)
    # set_default_billing = forms.BooleanField(required=False)
    # use_default_billing = forms.BooleanField(required=False)

class SearchForm(forms.Form):
    query=forms.CharField(max_length=100)
    catid=forms.IntegerField()