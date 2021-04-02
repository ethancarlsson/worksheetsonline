from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Profile, OriginalWorksheet

def allowed_users(worksheet):
    '''Makes sure teachers side is only accessible by the teacher who owns the worksheet.'''
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = None
            if worksheet:
                user = OriginalWorksheet.objects.get(pk=kwargs['pk']).worksheet_owner
            else:
                user = Profile.objects.get(pk=kwargs['pk']).user
            if request.user == user:
                return view_func(request, *args, **kwargs)
            else:
                return render(request,'fill_the_blanks/no_access.html')
        return wrapper_func
    return decorator
