from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # settings.py에 AUTH_USER_MODEL = '앱이름.User'를 추가해준다.
    pass