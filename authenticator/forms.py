from django import forms
from django.contrib.auth.models import User
from authenticator.models import FrontAuth

class AuthenticatorForm(forms.Form):
    Uname = forms.CharField(max_length=264, label='', widget=forms.TextInput(attrs={'placeholder': "username.access", 'name': 'uname', 'id': 'uname'}))
    hashKey = forms.CharField(max_length=264, label='',widget=forms.PasswordInput(attrs={'placeholder': "Hash Key", 'name': 'hashKey', 'id': 'key'}))


class AddUserForm(forms.ModelForm):


    class Meta():
        model = User
        fields = ('username','password')

    def clean(self):
        clean_form= super().clean()
        username=clean_form['username'];
        if(len(username.split('.'))<2):
            raise forms.ValidationError("Username format wrong. username should be FirstName.SecondName")
