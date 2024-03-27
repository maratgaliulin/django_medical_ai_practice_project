from django.http import HttpResponseForbidden

class MyHttpResponseForbidden(BaseException, HttpResponseForbidden):
    pass