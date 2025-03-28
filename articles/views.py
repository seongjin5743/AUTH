from django.shortcuts import render, redirect  # 템플릿 렌더링 및 리다이렉트를 위한 함수
from .forms import ArticleForm, CommentForm  # 게시글 및 댓글 폼 가져오기
from .models import Article, Comment  # 게시글 및 댓글 모델 가져오기
from django.contrib.auth.decorators import login_required  # 로그인 여부를 확인하는 데코레이터

def home(request):
    return redirect('/articles/')  # 기본 URL로 접속 시 게시글 목록 페이지로 리다이렉트

# 게시글 Read
def index(request):
    articles = Article.objects.all()  # 모든 게시글을 가져옴
    context = {
        'articles': articles,  # 템플릿에 전달할 게시글 목록
    }
    return render(request, 'index.html', context)  # 게시글 목록 템플릿 렌더링

# 게시글 상세 페이지
def detail(request, id):
    article = Article.objects.get(id=id)  # id에 해당하는 게시글을 가져옴
    form = CommentForm()  # 댓글 작성 폼 생성
    context = {
        'article': article,  # 템플릿에 전달할 게시글 객체
        'form': form,  # 템플릿에 전달할 댓글 작성 폼
    }
    return render(request, 'detail.html', context)  # 게시글 상세 템플릿 렌더링

# 게시글 Create
@login_required  # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
def create(request):
    if request.method == 'POST':  # POST 요청일 경우, 폼 데이터를 처리
        form = ArticleForm(request.POST)  # ArticleForm에 POST 데이터를 전달
        if form.is_valid():  # 폼 데이터가 유효한지 검증
            article = form.save(commit=False)  # 저장은 잠시 보류하고 객체만 반환
            article.user = request.user  # 현재 로그인한 사용자를 작성자로 설정
            article.save()  # 게시글 저장
            return redirect('articles:index')  # 저장 후 메인 페이지로 리다이렉트
    else:  # GET 요청일 경우, 빈 폼을 생성
        form = ArticleForm()

    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'create.html', context)  # 게시글 작성 템플릿 렌더링

# 게시글 Delete
@login_required  # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
def delete(request, id):
    article = Article.objects.get(id=id)  # id에 해당하는 게시글을 가져옴
    if request.user == article.user:  # 현재 로그인한 사용자가 작성자인지 확인
        article.delete()  # 게시글 삭제
    return redirect('articles:index')  # 삭제 후 메인 페이지로 리다이렉트

# 게시글 Update
@login_required  # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
def update(request, id):
    article = Article.objects.get(id=id)  # id에 해당하는 게시글을 가져옴

    if request.user != article.user:  # 현재 로그인한 사용자가 작성자가 아니면
        return redirect('articles:index')  # 메인 페이지로 리다이렉트

    if request.method == 'POST':  # POST 요청일 경우, 폼 데이터를 처리
        form = ArticleForm(request.POST, instance=article)  # 기존 게시글 데이터를 폼에 전달
        if form.is_valid():  # 폼 데이터가 유효한지 검증
            form.save()  # 게시글 수정 저장
            return redirect('articles:detail', id=id)  # 수정 후 상세 페이지로 리다이렉트
    else:  # GET 요청일 경우, 기존 게시글 데이터를 폼에 전달
        form = ArticleForm(instance=article)
    context = {
        'form': form,  # 템플릿에 전달할 폼 객체
    }
    return render(request, 'update.html', context)  # 게시글 수정 템플릿 렌더링

# 댓글 Create
@login_required  # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
def comment_create(request, article_id):
    form = CommentForm(request.POST)  # 댓글 작성 폼에 POST 데이터를 전달

    if form.is_valid():  # 폼 데이터가 유효한지 검증
        comment = form.save(commit=False)  # 저장은 잠시 보류하고 객체만 반환

        # 객체 저장하는 경우
        # comment.user = request.user  # 현재 로그인한 사용자를 댓글 작성자로 설정
        # article = Article.objects.get(id=id)  # 댓글이 달릴 게시글 가져오기
        # comment.article = article  # 댓글에 게시글 설정

        # id 값을 저장하는 경우
        comment.user_id = request.user.id  # 현재 로그인한 사용자의 id를 댓글 작성자로 설정
        comment.article_id = article_id  # 댓글이 달릴 게시글의 id 설정
        comment.save()  # 댓글 저장
        return redirect('articles:detail', id=article_id)  # 댓글 작성 후 상세 페이지로 리다이렉트

# 댓글 Delete
@login_required  # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)  # id에 해당하는 댓글을 가져옴
    if request.user == comment.user:  # 현재 로그인한 사용자가 댓글 작성자인지 확인
        comment.delete()  # 댓글 삭제
    return redirect('articles:detail', id=article_id)  # 삭제 후 상세 페이지로 리다이렉트