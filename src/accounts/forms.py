from django import forms
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from .models import CustomUser
from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['nickname'].widget.attrs['class'] = 'font-weight-bold form-control jz-profile-form'
        self.fields['nickname'].widget.attrs['disabled'] = ''

        self.fields['description'].widget.attrs['class'] = 'form-control jz-profile-form'
        self.fields['description'].widget.attrs['disabled'] = ''
        self.fields['description'].widget.attrs['placeholder'] = 'まだ自己紹介がありません'

    class Meta:
        model = CustomUser
        fields = ('nickname','description')
        help_texts = {
            'nickname': None
        }


class CustomSignupForm(SignupForm):
    nickname = forms.CharField(
        max_length=150,
        label='ニックネーム')
    id_regex = RegexValidator(
        regex=r'^[0-9a-zA-Z_]{5,15}$',
        message=('半角英数字または_(アンダースコア)のみ使用可能です。')
    )
    username = forms.CharField(
        validators=[MinLengthValidator(5), id_regex],
        max_length=15,
        label='アカウントID')

    class Meta:
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["email"]

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        user.username = self.cleaned_data['username']
        user.save()
        return user


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        login_widget = forms.TextInput(
            attrs={"placeholder": "アカウントID", "autocomplete": "username"}
        )
        id_regex = RegexValidator(
            regex=r'^[0-9a-zA-Z_]{5,15}$',
            message=('半角英数字または_(アンダースコア)のみ使用可能です。')
        )
        self.fields["login"] = forms.CharField(
            label="アカウントID",
            widget=login_widget,
            validators=[MinLengthValidator(5), id_regex],
            max_length=15,
        )