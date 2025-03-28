from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # 사용자 정의 폼 가져오기
from django.contrib.auth import login as auth_login  # 로그인 함수
from django.contrib.auth import logout as auth_logout  # 로그아웃 함수
from .models import User  # User 모델 가져오기

# 회원가입 뷰
def signup(request):
    if request.method == 'POST':  # POST 요청일 경우, 회원가입 폼 데이터를 처리
        form = CustomUserCreationForm(request.POST)  # 사용자 정의 회원가입 폼 생성
        if form.is_valid():  # 폼 데이터가 유효한지 검증
            form.save()  # 유효하다면 사용자 저장
            return redirect('accounts:login')  # 회원가입 후 로그인 페이지로 리다이렉트
    else:  # GET 요청일 경우, 빈 폼을 생성
        form = CustomUserCreationForm()

    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'signup.html', context)  # 회원가입 템플릿 렌더링

# 로그인 뷰
def login(request):
    if request.method == 'POST':  # POST 요청일 경우, 로그인 폼 데이터를 처리
        form = CustomAuthenticationForm(request, request.POST)  # 사용자 정의 로그인 폼 생성
        if form.is_valid():  # 폼 데이터가 유효한지 검증
            auth_login(request, form.get_user())  # 유효하다면 사용자 로그인 처리

            # /accounts/login
            # /accounts/login/?next=/articles/create
            next_url = request.GET.get('next')  # GET 파라미터로 전달된 'next' 값 가져오기

            # next가 없을 때는 None or 'articles:index'
            # next가 있을 때는 'articles/create' or 'articles:index'
            return redirect(next_url or 'articles:index')  # 'next'가 없으면 기본값으로 이동
    else:  # GET 요청일 경우, 빈 폼을 생성
        form = CustomAuthenticationForm(request.POST)

    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'login.html', context)  # 로그인 템플릿 렌더링

# 로그아웃 뷰
def logout(request):
    auth_logout(request)  # 사용자 로그아웃 처리
    return redirect('articles:index')  # 로그아웃 후 메인 페이지로 리다이렉트

# 프로필 뷰
def profile(request, username):
    user_profile = User.objects.get(username=username)  # username에 해당하는 사용자 정보 가져오기
    context = {
        'user_profile': user_profile,  # 템플릿에 전달할 사용자 정보
    }
    return render(request, 'profile.html', context)  # 프로필 템플릿 렌더링