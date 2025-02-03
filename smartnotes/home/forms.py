from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label = 'Password', 
        widget = forms.PasswordInput
    )

    password2 = forms.CharField(
        label = 'Repeat password', 
        widget = forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose another one."
            )
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already taken. Please login."
            )
        
        return email
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords Do Not Match.")
        
        return cd['password2']

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
