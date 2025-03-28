from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required  # 로그인 여부를 확인

def home(request):
    return redirect('/articles/')

# 메인 페이지 (게시글 목록) 뷰
def index(request):
    articles = Article.objects.all()  # 모든 게시글을 가져옴
    context = {
        'articles': articles,  # 템플릿에 전달할 게시글 목록
    }
    return render(request, 'index.html', context)  # 게시글 목록 템플릿 렌더링

def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'detail.html', context)

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

@login_required
def delete(request, id):
    article = Article.objects.get(id=id)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')

@login_required
def update(request, id):
    article = Article.objects.get(id=id)

    if request.user != article.user:
        return redirect('articles:index')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', id=id)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form,
    }
    
    return render(request, 'update.html', context)


@login_required
def comment_create(request, article_id):
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)

        # 객체 저장하는 경우
        # comment.user = request.user
        # article = Article.objects.get(id=id)
        # comment.article = article

        # id 값을 저장하는 경우
        comment.user_id = request.user.id
        comment.article_id = article_id
        comment.save()
        return redirect('articles:detail', id=article_id)

@login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', id=article_id)