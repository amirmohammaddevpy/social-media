from django import forms
from users.models import MyUser ,Contact

class EditProfile(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ("username","first_name","last_name","bio","avatar")
        
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class':'form-control'}),
        }