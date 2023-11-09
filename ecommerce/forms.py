from allauth.account.forms import SignupForm
from django import forms
from .models import ShipmentDetail


class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

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
        'mobile','telephone','method')
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
