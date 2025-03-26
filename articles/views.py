from django.shortcuts import render, redirect
from .forms import ArticleForm

def index(request):
    return render(request, 'index.html')

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