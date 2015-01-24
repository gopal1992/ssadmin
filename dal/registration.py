import base64

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from ip_analysis.models import Subscriber, UserSubscriber, VerifyRegistration
from persistance.page_authorization import SubscriberPageAuth, PagesList, \
    PageAuthAction


def create_new_subscriber(external_sid, site_url, email, phone):
    new_external_sid        =   external_sid[0][0]
    new_sb_external_sid     =   external_sid[0][1]
    latest_internal_sid     =   get_list_latest_internal_sid_subscribers()
    mini_uuid               =   str(new_external_sid).split('-')[3]
    sb_mini_uuid            =   str(new_sb_external_sid).split('-')[3]
    obj, created            =   Subscriber.objects.get_or_create(internal_sid    = latest_internal_sid + 2,
                                                                 external_sid    = new_external_sid,
                                                                 mini_uuid       = mini_uuid,
                                                                 site_url        = site_url,
                                                                 email           = email,
                                                                 phone1          = phone,
                                                                 sb_external_sid = new_sb_external_sid,
                                                                 sb_internal_sid = latest_internal_sid + 3,
                                                                 sb_mini_uuid    = sb_mini_uuid)
    return obj, created

def create_new_user(email, password):
    try:
        obj, created    =   User.objects.get_or_create(email = email, username = email)
        if created:
            obj.set_password(password)
            obj.save()
        return obj, created
    except IntegrityError:
        obj = None
        created = False
        return obj, created

def create_new_user_subscriber(user, subscriber):
    return UserSubscriber.objects.create(user = user, subscriber = subscriber)

def get_list_of_mini_uuids():
    return Subscriber.objects.all().values_list('mini_uuid', flat = True)

def get_list_of_sb_mini_uuids():
    return Subscriber.objects.all().values_list('sb_mini_uuid', flat = True)

def get_list_latest_internal_sid_subscribers():
    return Subscriber.objects.all().values_list('internal_sid', flat = True).order_by('-internal_sid')[0]

def get_registered_subscriber(activation_link):
    try:
        verification = VerifyRegistration.objects.get(activation_link = activation_link)
        verification.is_activated   = True
        verification.save()
        return verification
    except ObjectDoesNotExist:
        return False

def create_registration_verification_entry(subscriber, activation_link, password):
    password = base64.b64encode(password)
    return VerifyRegistration.objects.create(sid = subscriber, activation_link = activation_link, password = password)

def get_yet_to_verify_subscriber(subscriber):
    try:
        return VerifyRegistration.objects.get(sid = subscriber)
    except ObjectDoesNotExist:
        return False

def get_user_subscriber(subscriber):
    return UserSubscriber.objects.get(subscriber = subscriber)

def get_user(user):
    return User.objects.get(username = user)

def get_subscriber(email):
    try:
        subscriber = Subscriber.objects.get(email = email)
        return subscriber
    except ObjectDoesNotExist:
        return False

def create_page_permissions(subscriber):
    user_access_page    =   SubscriberPageAuth.objects.create(sid = subscriber,
                                                              page_id   = PagesList.objects.get(id = 1),
                                                              auth_id   = PageAuthAction.objects.get(auth_action = 0))
    user_analysis_page  =   SubscriberPageAuth.objects.create(sid = subscriber,
                                                              page_id   = PagesList.objects.get(id = 2),
                                                              auth_id   = PageAuthAction.objects.get(auth_action = 0))
    ip_access_page      =   SubscriberPageAuth.objects.create(sid = subscriber,
                                                              page_id   = PagesList.objects.get(id = 3),
                                                              auth_id   = PageAuthAction.objects.get(auth_action = 1))
    ip_analysis_page    =   SubscriberPageAuth.objects.create(sid = subscriber,
                                                              page_id   = PagesList.objects.get(id = 4),
                                                              auth_id   = PageAuthAction.objects.get(auth_action = 1))
    return user_access_page, user_analysis_page, ip_access_page, ip_analysis_page
