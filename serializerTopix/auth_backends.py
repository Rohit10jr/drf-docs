# Login With Email Instead of Username

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, userid=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=userid)
            # user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
