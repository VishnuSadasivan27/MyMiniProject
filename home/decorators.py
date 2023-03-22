
from .models import Registration
from django.shortcuts import redirect


def user_login_required(function):
    def wrapper(request, login_url='Login', *args, **kwargs):
        if not 'email' in request.session:
            return redirect(login_url)
        else:
            return function(request, *args, **kwargs)

    return wrapper
