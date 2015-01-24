import datetime
from random import randrange, randint
import random

from django.contrib.auth.models import User
import factory

from ip_analysis.models import ResponseCode, Subscriber, RulesSummary, IpDetails, \
    IpAddressAccessList, IpAnalysis, UserSubscriber


COUNTRY_LIST = ['India', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'China', \
                'South Africa', 'Russia', 'Brazil']

CHOICE  =   ['True', 'False']

TIMEZONES = [("Pacific/Midway", "(GMT-11:00) Midway"),
             ("Pacific/Niue", "(GMT-11:00) Niue"),
             ("Pacific/Pago_Pago", "(GMT-11:00) Pago Pago"),
             ("Pacific/Honolulu", "(GMT-10:00) Hawaii Time"),
             ("Pacific/Rarotonga", "(GMT-10:00) Rarotonga"),
             ("Pacific/Tahiti", "(GMT-10:00) Tahiti"),
             ("Pacific/Marquesas", "(GMT-09:30) Marquesas"),]



class ResponseCodeFactory(factory.Factory):

    class Meta:
        model = ResponseCode

    response = factory.Sequence(lambda n: "%04d" %n)



class SubscriberFactory(factory.Factory):

    class Meta:
        model = Subscriber

    internal_sid = factory.Sequence(int)
    name         = factory.Sequence(lambda n: "name%s" %n)
    address1     = factory.Sequence(lambda n: "Flat No.%s" %n)
    phone1       = factory.Sequence(lambda n: "8888888%03d" %n)
    email        = factory.LazyAttribute(lambda n: "%s@example.com" % n.name)
    status       = randrange(2)
    timezone     = random.choice(TIMEZONES)
    pagepermin   = factory.Sequence(lambda n: "1%s0" %n)
    pagepersess  = factory.Sequence(lambda n: "2%s0" %n)
    sesslength   = factory.Sequence(lambda n: "3%s0" %n)

    r_Pagepermin    = factory.SubFactory(ResponseCodeFactory)
    r_pagepersess   = factory.SubFactory(ResponseCodeFactory)
    r_sesslength    = factory.SubFactory(ResponseCodeFactory)

    r_browserIntgrity       = factory.SubFactory(ResponseCodeFactory)
    r_httpRequestIntegrity  = factory.SubFactory(ResponseCodeFactory)
    r_Aggregator            = factory.SubFactory(ResponseCodeFactory)
    r_behaviourIntegrity    = factory.SubFactory(ResponseCodeFactory)

    mode        = randrange(2)

class RulesSummaryFactory(factory.Factory):

    class Meta:
        model = RulesSummary

    sid         = factory.SubFactory(SubscriberFactory)
    dt          = factory.Sequence(lambda n: datetime.date.today() - datetime.timedelta(days=randrange(1,182)))

    r_browserIntgrity       = randrange(5)
    r_httpRequestIntegrity  = randrange(5)
    r_Aggregator            = randrange(5)
    r_behaviourIntegrity    = randrange(5)

    genuineusers    = randrange(100000)
    trustedbots     = randrange(100000)
    badbots         = randrange(10000)

    monitor         = randrange(100000)
    captcha         = randrange(100000)
    block           = randrange(100000)
    feedfakedata    = randrange(100000)

    all_js  = randrange(10000)
    all_api = randrange(10000)

#     genuineusers   = randrange(100000)
#     trustedbots    = randrange(100000)
#     badbots        = randrange(100000)
#     all_js         = randrange(10000)
#     all_api        = randrange(10000)


class IpDetailsFactory(factory.Factory):

    class Meta:
        model = IpDetails

    ip_address      = factory.Sequence(lambda n: "{}.{}.{}.{}" .format(randint(1, 256), randint(1, 256), randint(1, 256), randint(1, 256)))
    country_name    = random.choice(COUNTRY_LIST)
    city_name       = factory.Sequence(lambda n: "city%s" %n)
    isp             = factory.Sequence(lambda n: "ISP%s" %n)
    domain          = factory.Sequence(lambda n: "domain%s" %n)


class IpAddressAccessListFactory(factory.Factory):

    class Meta:
        model = IpAddressAccessList

    sid = factory.SubFactory(SubscriberFactory)
    ipaddress   = factory.SubFactory(IpDetailsFactory)
    accessstatus= random.choice(CHOICE)


class IpAnalysisFactory(factory.Factory):

    class Meta:
        model = IpAnalysis

    sid = factory.SubFactory(SubscriberFactory)
    dt  = factory.Sequence(lambda n: datetime.date.today() - datetime.timedelta(days=randrange(0,32)))
    ipaddress   = factory.SubFactory(IpDetailsFactory)

    totalrequests           = randrange(100000)
    browserIntgrity         = randrange(100000)
    httpRequestIntegrity    = randrange(100000)
    Aggregator              = randrange(100000)
    behaviourIntegrity      = randrange(100000)
    Ratelimiting            = randrange(100000)
    genuinerequests         = randrange(100000)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username','email','password')

    username        = factory.Sequence(lambda n : "username{}@example.com".format(n))
    email           = factory.Sequence(lambda n : "username{}@example.com".format(n))
    password        = 'password'


class UserSubscriberFactory(factory.Factory):

    class Meta:
        model = UserSubscriber

#     user        = factory.SubFactory(UserFactory)
    subscriber  = factory.SubFactory(SubscriberFactory)