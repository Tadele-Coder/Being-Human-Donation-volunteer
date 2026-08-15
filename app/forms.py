from django import forms
from . models import Donor, Volunteer, Donation,DONATION_CHOICES, DonationArea


from django.contrib.auth.forms import (
UserCreationForm,
AuthenticationForm,
UsernameField,
PasswordChangeForm,
PasswordResetForm,
SetPasswordForm, 
)

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation

class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autofocus': True
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':'Enter Password'}))

    password2 = forms.CharField(label='Confirm Password(agin)', widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':'Enter Password Again'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets ={
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email ID'})
        }
class DonorSignupForm(forms.ModelForm):

    class Meta:
        model = Donor
        fields = [
            'contact',
            'userpic',
            'address'
        ]

        widgets = {
            'contact': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'userpic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }
class VolunteerSignupForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = [
            'contact',
            'userpic',
            'idpic',
            'aboutme',
            'address'
        ]

        widgets = {
            'contact': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'userpic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'idpic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'aboutme': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Old Password'
        })
    )

    new_password1 = forms.CharField(
        label='New Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'New Password'
        }),
        help_text=password_validation.password_validators_help_text_html()
    )

    new_password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
        
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={
        'autocomplete':'email', 'class':'form-control'
    }))
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password', strip=False, widget=forms.PasswordInput(attrs={
    'autocomplete':'new-password', 'class':'form-control'
    }))
class DonationNowForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = [
            'donationname',
            'donationpic',
            'collectionloc',
            'description'
        ]

        widgets = {

            'donationname': forms.Select(attrs={
                'class': 'form-select'
            }),

            'donationpic': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'collectionloc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Donation Collection Address'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Special Note'
            }),
        }

        labels = {
            'donationname': 'Donation Name',
            'donationpic': 'Donation Image',
            'collectionloc': 'Collection Address',
            'description': 'Description',
        }
class DonationAreaForm(forms.ModelForm):
    class Meta:
        model=DonationArea
        fields = ['areaname', 'description']
        widgets={
            'areaname':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Donation Area'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'})
            
        }
        labels={
            'areaname':'Donation Area Name',
            'description':'Description',
        }