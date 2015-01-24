# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from accounts.services import generate_random_password
from utils.email import send_templated_email


def send_new_user_email(request, user):
    password = generate_random_password()
    user.set_password(password)
    user.save()
    url = reverse('ip_analysis.view_traffic_analysis')
    context = {
        'username': user.username,
        'password': password,
        'email': user.email,
        'dashboard_url': request.build_absolute_uri(url),
    }
    return send_templated_email(
        label="new_user",
        to=user.email,
        context=context
    )
