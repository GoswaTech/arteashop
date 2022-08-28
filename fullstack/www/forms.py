from django import forms

class LoginForm(forms.Form):
    password = forms.CharField(
            label = 'Your Password',
            max_length = 127,
            widget = forms.PasswordInput,
        )
