from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article
from django.contrib.auth.decorators import login_required

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'index.html', context)

@login_required # 로그인 안 한 상태로 만드려면 accounts의 login으로 갈 수 있게 한다.
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()

    context = {
        'form': form,
    }
    return render(request, 'create.html', context)