from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            # 1. authenticate() 함수를 사용하여 사용자를 인증한다.
            # 이메일 기반 인증을 사용하려면 settings.py에 커스텀 백엔드 등록이 필수.
            self.user = authenticate(self.request, email=email, password=password)

            # 2. authenticate가 None을 반환하면 인증 실패
            if self.user is None:
                # 보안을 위해 이메일/비밀번호 오류 메시지를 일반화합니다.
                raise forms.ValidationError(
                    "이메일 또는 비밀번호가 올바르지 않습니다.",
                    code="invalid_login",
                )

            # 3. 계정 활성화 상태 확인
            if not self.user.is_active:
                raise forms.ValidationError(
                    "계정이 비활성화되어 있습니다.",
                    code="inactive",
                )
        else:
            # 이메일이나 비밀번호 중 하나라도 입력되지 않았을 경우
            raise forms.ValidationError(
                "이메일과 비밀번호를 모두 입력해주세요.",
                code="required",
            )

        return self.cleaned_data

    def get_user(self):
        return self.user
