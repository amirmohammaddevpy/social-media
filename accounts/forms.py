from django import forms
from users.models import MyUser

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=255,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_confirm = forms.CharField(max_length=255,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = MyUser
        fields = ('first_name','last_name','username','email')
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(max_length=255,widget=forms.PasswordInput(attrs={'class':'form-control'}))