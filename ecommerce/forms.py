from allauth.account.forms import SignupForm
from django import forms
from .models import ShipmentDetail, ConfirmedOrderDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class CustomSignupForm(SignupForm):
    """
    First and last name in All auth signup form are added
    """
    first_name = forms.CharField(
        max_length=16,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
        )
    last_name = forms.CharField(
        max_length=16, label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
        )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ShipmentDetailForm(forms.ModelForm):
    """
    This Form handles the Shipment detail modal.
    Fields in shipment details are styled, placeholders and titles
    are also added.
    """
    class Meta:
      model = ShipmentDetail
      fields = ('first_name', 'last_name', 'address_line_one',
            'postal_code', 'city', 'country', 'mobile', 'method')
       
    def __init__(self, *args, **kwargs):
        super(ShipmentDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('first_name', css_class='fs-5',
                  placeholder='Enter First Name', title='Enter First Name'),
            Field('last_name', css_class='fs-5',
                  placeholder='Enter Last Name', title='Enter Last Name'),
            Field('address_line_one', css_class='fs-5',
                  placeholder='Enter Address', title='Enter Address'),
            Field('postal_code', css_class='fs-5',
                  placeholder='Enter Postal Code', title='Enter Postal Code'),
            Field('city', css_class='fs-5',
                  placeholder='Enter City', title='Enter City'),
            Field('country', css_class='fs-5',
                  placeholder='Enter Country', title='Enter Country'),
            Field('mobile', css_class='fs-5',
                  placeholder='Enter Mobile Number',
                  title='Enter Mobile Number'),
            Field('method', css_class='fs-5',
                  placeholder='Enter Payment method',
                  title='Enter Payment method'),
        )


class ConfirmedOrderDetailForm(forms.ModelForm):
    """
    This Form handles the quantity in confirm
    order details model
    """
    class Meta:
        model = ConfirmedOrderDetail
        fields = ('quantity',)