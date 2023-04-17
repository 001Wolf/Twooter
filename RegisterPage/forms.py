from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class':'form_input'}), label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email Id', 'class':'form_input'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'form_input'}), label="")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class':'form_input'}), label="")