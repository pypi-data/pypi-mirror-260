import inspect
from threading import local

from django.conf import settings

USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')

_thread_locals = local()


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, user_fun.__get__(user_fun, local))


def _set_current_user(user=None):
    _do_set_current_user(lambda self: user)



class SetCurrentUser:
    def __init__(this, request):
        this.request = request

    def __enter__(this):
        _do_set_current_user(lambda self: getattr(this.request, 'user', None))

    def __exit__(this, type, value, traceback):
        _do_set_current_user(lambda self: None)


class UserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with SetCurrentUser(request):
            response = self.get_response(request)
        return response


def get_current_user():
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    return current_user() if callable(current_user) else current_user
    


def gets_current_users(self):
    try:
        return( next(
        (
            frame_record[0].f_locals["request"]
            for frame_record in inspect.stack()
            if frame_record[3] == "dispatch"
        ),
        None).user)
    except Exception:
        return( next(
        (
            frame_record[0].f_locals["request"]
            for frame_record in inspect.stack()
            if frame_record[3] == "get_response"
        ),
        None).user)