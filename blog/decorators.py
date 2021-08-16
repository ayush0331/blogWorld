from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def login_required(function):
    def wrapper_function(request,*args,**kwargs):
        if not request.user.is_authenticated:
            if request.is_ajax():
                return HttpResponseForbidden()
            else:
                return redirect("/")
        return function(request,*args,**kwargs)
    return wrapper_function
