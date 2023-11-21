from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.hashers import check_password
from .models import User

class EmailModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None,**kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None