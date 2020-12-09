from django import forms
from app.models import Question, User, Answer, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class RegistrForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

class SettingsForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        return self.clean_password

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
