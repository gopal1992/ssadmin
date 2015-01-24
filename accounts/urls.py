# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse

from .views import (user_login,
                    user_logout,
                    forgot_password,
                    custom_password_reset_done,
                    custom_password_reset_confirm,
                    custom_password_reset_complete,
                    user_management,
                    delete_user,
                    edit_user,
                    new_user,
                    update_timezone)


urlpatterns = patterns('',
    url(
        regex=r'login/$',
        view=user_login,
        name="accounts.login"
    ),
    url(
        regex=r'logout/$',
        view=user_logout,
        name="accounts.logout"
    ),
    url(
        regex=r'forgot_password/$',
        view=forgot_password,
        name="accounts.forgot_password"),

    url(
        regex=r'password_reset_done/$',
        view=custom_password_reset_done,
        name='accounts.password_reset_done'),

    url(
        regex=r'password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        view=custom_password_reset_confirm,
        name='accounts.password_reset_confirm'
    ),
    url(
        regex=r'password_reset_complete/$',
        view=custom_password_reset_complete,
        name='accounts.password_reset_complete'
    ),
    url(
        regex=r'user_management/$',
        view=user_management,
        name="accounts.user_management"
    ),
    url(
        regex=r'timezone/$',
        view=update_timezone,
        name="accounts.update_timezone"
    ),
    url(
        regex=r'user/new/$',
        view=new_user,
        name="accounts.new_user"
    ),
    url(
        regex=r'user/edit/$',
        view=edit_user,
        name="accounts.edit_user"
    ),
    url(
        regex=r'user/delete/$',
        view=delete_user,
        name="accounts.delete_user"
    ),

)
