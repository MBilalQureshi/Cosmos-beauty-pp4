from allauth.account.forms import SignupForm
from django import forms
from .models import ShipmentDetail, ConfirmedOrderDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ShipmentDetailForm(forms.ModelForm):
    class Meta:
        model = ShipmentDetail
        fields = ('first_name','last_name','address_line_one', 'postal_code', 'city', 'country',
        'mobile','method',)
        # widget = {
        #     'first_name': forms.TextInput(),
        #     'last_name': forms.TextInput(),
        #     'address_line_one': forms.TextInput(),
        #     'postal_code': forms.NumberInput(),
        #     'city': forms.TextInput(),
        #     'country': forms.Textarea(),
        #     'mobile': forms.NumberInput(),
        #     'telephone': forms.NumberInput(),
        #     'method': forms.ChoiceField(),
        # }
    def __init__(self, *args, **kwargs):
        super(ShipmentDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            # Field('first_name', css_class='display-3', placeholder='Enter First Name', label='Custom Label',title='Custom Label 1',label_class='custom-label-class'),
            Field('first_name', css_class='fs-5',placeholder='Enter First Name', title='Enter First Name'),
            Field('last_name', css_class='fs-5', placeholder='Enter Last Name',title='Enter Last Name'),
            Field('address_line_one', css_class='fs-5', placeholder='Enter Address',title='Enter Address'),
            Field('postal_code', css_class='fs-5', placeholder='Enter Postal Code',title='Enter Postal Code'),
            Field('city', css_class='fs-5', placeholder='Enter City',title='Enter City'),
            Field('country', css_class='fs-5', placeholder='Enter Country',title='Enter Country'),
            Field('mobile', css_class='fs-5', placeholder='Enter Mobile Number',title='Enter Mobile Number'),
            Field('method', css_class='fs-5', placeholder='Enter Payment method',title='Enter Payment method'),
        )


class ConfirmedOrderDetailForm(forms.ModelForm):
    class Meta:
        model = ConfirmedOrderDetail
        fields = ('quantity',)
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': '1', 
                'max': '10',
                'type': 'number',
                'step': '1',
            }),
        }