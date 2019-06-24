from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class user_registration_form(forms.Form):
    username = forms.CharField(label='Username',
                                max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
                                max_length=100,required=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                max_length=100,required=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # required is True by default, it makes HTML check if the user entered data in fields or not
    # before hitting submit, we can make it False like above
    # we can see it by looking at the forms page source from the browser

    # next def is to validate the email of the user
    def clean_email(self):
        email = self.cleaned_data['email']

        # to check if the email is already in the database or not
        qs = User.objects.filter(email=email) # qs is short of QuerySet
        if qs.exists():
            raise ValidationError('E-Mail Address Is Already Exists !!')
        return email # will continue normally if the email doesn't already exist in the database

    def clean(self):
        cleaned_data = super().clean() # to make this function runs first with the class itself
        p1 = cleaned_data.get('password1') # .get() return None if the field is empty
        p2 = cleaned_data.get('password2')
        print(p1)

        if p1 and p2: # to check Niether p1 nor p2 has returned a None value
            if p1 != p2:
                raise ValidationError('Password doesn\'t match')
