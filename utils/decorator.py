# -*- coding: utf-8 -*-

from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from ip_analysis.models import Subscriber
from user_analysis.models import SubscriberPageAuth, PagesList
from utils.account import get_subscriber_from_user


def load_model(model_name, pk, parameter):
    """Returns Model instance matching primary key

    :param model_name: Model class like User, Subscriber
    :param filters: dict containing all parameters to filter
                    like {'is_active': True, 'email': 'u@example.com'} or
                         {'pk': 1}
    :param parameter: string name variable which will be passed to the calling
                      function

    @load_model(User, pk=1, 'user')
    def index(request, user):
        pass

    """
    def inner(f):
        def wrapped_f(*args, **kwargs):
            result = {'parameter': get_object_or_404(model_name, pk=pk)}
            result.update(kwargs)
            return f(*args, **kwargs)
        return wrapped_f
    return inner


def access_to_page(extra_value):
    def inner(f):
        def wrapper(request, *args, **kwargs):
            subscriber = get_subscriber_from_user(request)
            sid = Subscriber.objects.get(internal_sid   = subscriber.internal_sid)
            page= PagesList.objects.get(page_name       = extra_value)
            auth_id = SubscriberPageAuth.objects.get(sid = sid, page_id = page)
            if auth_id.auth_id.id == 1:
                return f(request, *args, **kwargs)
            return HttpResponseRedirect('/')
        return wrapper
    return inner
