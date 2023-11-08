from allauth.account.forms import SignupForm
from django import forms
from .models import Address


class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_line_one', 'postal_code', 'city', 'country',
        'telephone', 'mobile')