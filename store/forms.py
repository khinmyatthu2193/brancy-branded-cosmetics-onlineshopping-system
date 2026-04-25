from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    # Add firstname and lastname fields
    firstname = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    lastname = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    
    # Fields for password and password confirmation
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'firstname', 'lastname', 'password']  # Include the new fields

    # Custom validation to check if password and confirm password match
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match")

        return password_confirm

    # Save the user with a hashed password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

###########################K M T for Login Logout#######################
class UpdateForm(UserChangeForm):
    # Add firstname and lastname fields
    firstname = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    lastname = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    
    # Fields for password and password confirmation
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'firstname', 'lastname', 'password']  # Include the new fields

    # Custom validation to check if password and confirm password match
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match")

        return password_confirm

    # Save the user with a hashed password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

##############################################################

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
