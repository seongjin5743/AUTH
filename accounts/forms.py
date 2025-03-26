from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# 사용자 정의 회원가입 폼
class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User  # User 모델을 기반으로 폼 생성
        # fields = '__all__'
        fields = ('username', )  # username 필드만 포함

# 사용자 정의 로그인 폼
class CustomAuthenticationForm(AuthenticationForm):
    pass  # 기본 AuthenticationForm을 그대로 사용