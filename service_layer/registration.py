import base64
from uuid import uuid4
import uuid

import arrow
from django.contrib.auth.hashers import make_password

from accounts.services import grant_privilege
from dal.registration import create_new_subscriber, create_new_user, \
    create_new_user_subscriber, get_list_of_mini_uuids, \
    get_list_of_sb_mini_uuids, get_user_subscriber, get_user, \
    get_registered_subscriber, create_registration_verification_entry, \
    create_page_permissions, get_subscriber, get_yet_to_verify_subscriber
from utils.app_messages import EMAIL_NOT_REGISTERED, ACCOUNT_ACTIVE_ALREADY
from utils.email import send_templated_email


def get_unique_external_sid():
    mini_uuids      = list(get_list_of_mini_uuids())
    sb_mini_uuids   = list(get_list_of_sb_mini_uuids())
    external_sid    = uuid4()
    mini_uuid       = str(external_sid).split('-')[3]
    sb_external_sid = uuid4()
    sb_mini_uuid    = str(sb_external_sid).split('-')[3]

    if mini_uuid in mini_uuids and sb_mini_uuids:
        while(mini_uuid in mini_uuids and sb_mini_uuids):
            external_sid = uuid4()
            mini_uuid    = str(external_sid).split('-')[3]

    if sb_mini_uuid in mini_uuids and sb_mini_uuids:
        while(sb_mini_uuid in mini_uuids and sb_mini_uuids):
            sb_external_sid = uuid4()
            sb_mini_uuid    = str(sb_external_sid).split('-')[3]

    return external_sid, sb_external_sid

def constructing_verification_link(request, subscriber, password):
    activation_link = arrow.utcnow().timestamp
    salt            = str(uuid.uuid4())
    hashed_url      = make_password((str(subscriber.internal_sid)+str(salt)+str(activation_link)), hasher='md5')
    hashed_url      = hashed_url.split('$')[-1]
    url             = '/verifying_registration/' + hashed_url +'/'
    while get_registered_subscriber(url):
        salt            = str(uuid.uuid4())
        hashed_url      = make_password((str(subscriber.internal_sid)+str(salt)+str(activation_link)), hasher='md5')
        hashed_url      = hashed_url.split('$')[-1]
        url             = '/verifying_registration/' + hashed_url +'/'
    entry           = create_registration_verification_entry(subscriber, hashed_url, password)
    link            = request.build_absolute_uri(url)
    return link

def register_a_new_subscriber(request, form):
    external_sid = get_unique_external_sid(), # process this external_id to be unique
    site_url     = form.cleaned_data['site_url']
    email        = form.cleaned_data['email']
    password     = form.cleaned_data['password']
    phone        = u''
    if form.cleaned_data['phone']:
        phone       = form.cleaned_data['phone']

    subscriber_obj, subscriber_created = create_new_subscriber(external_sid,
                                                               site_url,
                                                               email,
                                                               phone)
    if subscriber_created:
        user_obj, user_created = create_new_user(email, password)

        if user_created:
            create_page_permissions(subscriber_obj)
            create_new_user_subscriber(user_obj, subscriber_obj)
            link = constructing_verification_link(request, subscriber_obj, password)
            grant_privilege(user_obj, 'admin')
            return send_templated_email(label="registration",
                                        to=user_obj.email,
                                        context={'user_name':user_obj.email,'link': link,})
        else:
            return 'Email already exists'

    else:
        return 'Subscriber already exists'

def verifying_registration_process(request, activation_link):
    verification    = get_registered_subscriber(activation_link)
    if verification:
        user_subscriber = get_user_subscriber(verification.sid)
        user            = get_user(user_subscriber.user.username)
        password        = base64.b64decode(verification.password)
        verification.delete()
        return user, True, password
    return None, False, None


def resend_the_link(subscriber, is_subscriber_present):
    return send_templated_email(label="registration",
                                to=subscriber.email,
                                context={'user_name':subscriber.email,'link': is_subscriber_present.activation_link,})

def resend_verification_link_process(request, form):
    email = form.cleaned_data['email']
    subscriber = get_subscriber(email)
    if subscriber:
        is_subscriber_present = get_yet_to_verify_subscriber(subscriber)
        if is_subscriber_present:
            return send_templated_email(label="registration",
                                        to=subscriber.email,
                                        context={'user_name':subscriber.email,'link': is_subscriber_present.activation_link,})
        else:
            return ACCOUNT_ACTIVE_ALREADY
    else:
        return EMAIL_NOT_REGISTERED
