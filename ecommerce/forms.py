from allauth.account.forms import SignupForm
from django import forms
from .models import ShipmentDetail, ConfirmedOrderDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

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
        'mobile','telephone','method',)
        widgets = {
            'mobile': forms.NumberInput(attrs={
                'type': 'number',
            }),'telephone': forms.NumberInput(attrs={
                'type': 'number',
            }),'mobile': forms.NumberInput(attrs={
                'type': 'number',
            }),
        }
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
    # def __init__(self, *args, **kwargs):
    #     super(ShipmentDetailForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.layout = Layout(
    #         # Field('first_name', css_class='display-3', placeholder='Enter First Name', label='Custom Label',title='Custom Label 1',label_class='custom-label-class'),
    #         Field('first_name', css_class='', title='Custom Label 1', css_label_class='fs-1 fw-bold'),
    #         Field('last_name', css_class='custom-class2', ),
    #         Field('address_line_one', css_class='custom-class1',),
    #         Field('postal_code', css_class='custom-class2', ),
    #         Field('city', css_class='custom-class1', ),
    #         Field('country', css_class='custom-class2', ),
    #         Field('mobile', css_class='custom-class1', ),
    #         Field('telephone', css_class='custom-class2',),
    #         Field('method', css_class='custom-class2', ),
    #         # Add more fields as needed
    #     )


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