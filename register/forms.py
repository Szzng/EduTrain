from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser
from course.models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'nickname', 'interest']

    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()
    interest = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )



    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):  # 저장하는 부분 오버라이딩
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            # for saving M2M Field
            user.interest.clear()
            user.interest.add(*self.cleaned_data['interest'])
            self.save_m2m()

        return user


class UserUpdateForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].disabled = True


class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

        labels = {
            'email': '',
            'password': '',
        }

        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'email',

                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'password',
                }
            )
        }

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = MyUser.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호를 바르게 입력하세요."))

        except MyUser.DoesNotExist:
            self.add_error("email", forms.ValidationError("email을 바르게 입력하세요."))

