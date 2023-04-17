from django import forms

class EditProfile(forms.Form):
    profile_pic = forms.ImageField(required=False)
    bio = forms.CharField(max_length=300, required=False)