from django import forms
from app.models import Question, User, Answer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class RegistrForm(UserCreationForm):
    photo = forms.ImageField(required=False)
    nickname = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nickname', 'photo']

class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

class SettingsForm(UserChangeForm):
    photo = forms.ImageField(required=False)
    nickname = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'photo', 'nickname']

    def clean_password(self):
        return self.clean_password

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
