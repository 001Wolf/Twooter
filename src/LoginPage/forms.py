from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':'Email ID', 'class':'form_input'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form_input'}), label="")