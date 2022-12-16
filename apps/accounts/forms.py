from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User

__all__ = [
    'UserCreationForm',
    'UserChangeForm',
    'UserRegisterForm',
    'LoginForm',
    'UserProfileForm',
]

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href='../password'>Change Password</a>")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name',
                'password', 'last_login')
    
class UserRegisterForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email exist')
        return email

class UserRegisterForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mx-auto w-100','placeholder':'Full Name'}),label='')
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control','placeholder':'Email'}),label='')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mx-auto w-100','placeholder':'Password'}),label='')
    password_r = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mx-auto w-100','placeholder':'Repat Password'}),label='')
    meet = forms.ChoiceField(choices=User.FIND_CHOICE,required=False,widget=forms.Select(attrs={'class': 'form-control mx-auto w-100','placeholder':'How Meet'}),label='How Toy Meet ?')
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class='btn btn-primary w-100'))
    helper.form_method = 'POST'

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email exist')
        return email
    
    def clean_password_r(self):
        password = self.cleaned_data.get('password')
        reapet_password = self.cleaned_data.get('password_r')
        if password and reapet_password:
            if password == reapet_password:
                if len(password) >= 6:
                    return reapet_password
                else:
                    raise ValidationError('Password Is Short')
            else:
                raise ValidationError('Password Not Mach')

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control mx-auto','placeholder':'Your Email'}),label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mx-auto','placeholder':'Your Password'}),label='Password')
    captcha = ReCaptchaField(widget=ReCaptchaV3)

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].disabled = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mx-auto w-100'

    class Meta:
        model = User
        fields = ('full_name','phone_number','email')