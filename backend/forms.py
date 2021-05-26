from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'required':'true'}))
    username = forms.CharField(max_length = 20,label="Username",widget=forms.TextInput(attrs={'placeholder': 'Username','required':'true'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email','required':'true'}))
    class Meta():
        model = User
        fields = ('username','email','password',)
        widgets = {
            'username': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Email'}),
            'password': forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':'Password'}),
        }