# myapp/forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from .models import CustomUser, Video

# For registration page
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    
    plan = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=[
            ('premium', 'Premium - $39 / 3 Months with a 5 day free trial'),
            ('basic', 'Basic - $19 / 1 Month'),
            ('free', 'Free'),
        ],
        error_messages = {"required":"Please select an option, it's required"}
    )

# For login page
class CustomUserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-0', 
        'placeholder': 'Enter Email'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mb-0',
            'placeholder': 'Enter Password'
        }
    ))

# For upload page
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video_file')

# For upload page
class DecodeVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video_file', )
