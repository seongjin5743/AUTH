from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta():
        model = Article

        # 둘 중 하나를 쓰면 user를 제외할 수 있다.
        # fields = ('title', 'content')
        exclude = ('user', )