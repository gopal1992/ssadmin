import datetime

from django.contrib.auth.models import User
from django.core.cache import get_cache
from django.db import models

from utils.constants import ACCESS_STATUS_ALLOW, ACCESS_STATUS_MAP, RK_RULE_BASE, \
    RK_RULE_BROWSER_INTGRITY, RK_RULE_HTTP_REQUEST_INTEGRITY, RK_RULE_AGGREGATOR, \
    RK_RULE_BEHAVIOUR_INTEGRITY, RK_RULE_PAGE_PER_MINUTE_EXCEEDS, \
    RK_RULE_PAGE_PER_SESSION_EXCEEDS, RK_RULE_SESSION_LENGTH_EXCEEDS, \
    RK_WHITE_LIST, RK_RULE_LIMITING_CHECK_FAILED, \
    RK_IP_ACTION_BASE, RK_VERIFY_INT, RK_SID_MAP, RK_SID_MIN_MAP


ALLOW = ACCESS_STATUS_MAP[ACCESS_STATUS_ALLOW]


# Create your models here.
class ResponseCode(models.Model):
    #id. Since Django default has the same name. Not explicitly declared
    response = models.CharField(max_length=25)

    class Meta:
        db_table = "response_code"

    def __unicode__(self):
        return self.response


class Subscriber(models.Model):
    internal_sid    =   models.IntegerField(primary_key=True)
    external_sid    =   models.CharField(max_length=75, null=True, blank=True)

    name            =   models.CharField(max_length=256)
    address1        =   models.TextField(max_length=500)
    address2        =   models.TextField(max_length=500, null=True, blank=True, default = u'')
    phone1          =   models.CharField(max_length=25)
    phone2          =   models.CharField(max_length=25, null=True, blank=True, default = u'')
    email           =   models.EmailField(max_length=500)
    # 0 means deactivated else active
    status          =   models.IntegerField(default = 1)
    timezone        =   models.CharField(max_length=75, default='Asia/Kolkata')

    pagepermin      =   models.IntegerField(db_column="pagepermin", default = 0)
    pagepersess     =   models.IntegerField(db_column="pagepersess", default = 0)
    sesslength      =   models.IntegerField(db_column="sesslength", default = 0)

    r_browserIntgrity       =   models.ForeignKey(ResponseCode, db_column="r_browserIntgrity",     related_name='+', default=2)
    r_httpRequestIntegrity  =   models.ForeignKey(ResponseCode, db_column="r_httpRequestIntegrity",related_name='+', default=2)
    r_Aggregator            =   models.ForeignKey(ResponseCode, db_column="r_Aggregator",            related_name='+', default=1)
    r_behaviourIntegrity    =   models.ForeignKey(ResponseCode, db_column="r_behaviourIntegrity",   related_name='+', default=2)
    r_Pagepermin            =   models.ForeignKey(ResponseCode, db_column="r_Pagepermin",          related_name='+', default=2)
    r_pagepersess           =   models.ForeignKey(ResponseCode, db_column="r_pagepersess",         related_name='+', default=2)
    r_sesslength            =   models.ForeignKey(ResponseCode, db_column="r_sesslength",           related_name='+', default=2)

    mode                    =   models.IntegerField(default=1)
    site_url                =   models.URLField(max_length=250)
    mini_uuid               =   models.CharField(max_length=200)

    sb_internal_sid         =   models.IntegerField()
    sb_external_sid         =   models.CharField(max_length = 200, null = True, blank = True)
    sb_mini_uuid            =   models.CharField(max_length = 200)

    def save(self, *args, **kwargs):
        redis = get_cache('default').raw_client

        base_key = "{}:{}".format(RK_RULE_BASE, self.internal_sid)
        base_key_1 = "{}:{}".format(RK_RULE_BASE, self.sb_internal_sid)

        # Verify Integration
        redis.hset(base_key,    RK_VERIFY_INT, 0)
        redis.hset(base_key_1,  RK_VERIFY_INT, 1)

        redis.hset(RK_SID_MAP,      self.external_sid, self.internal_sid)
        redis.hset(RK_SID_MIN_MAP,  self.mini_uuid,    self.internal_sid)

        redis.hset(RK_SID_MAP,      self.sb_external_sid, self.sb_internal_sid)
        redis.hset(RK_SID_MIN_MAP,  self.sb_mini_uuid,    self.sb_internal_sid)

        # Bot Response Rules
        redis.hset(base_key, RK_RULE_BROWSER_INTGRITY,          self.r_browserIntgrity.id)
        redis.hset(base_key, RK_RULE_HTTP_REQUEST_INTEGRITY,    self.r_httpRequestIntegrity.id)
        redis.hset(base_key, RK_RULE_AGGREGATOR,                self.r_Aggregator.id)
        redis.hset(base_key, RK_RULE_BEHAVIOUR_INTEGRITY,       self.r_behaviourIntegrity.id)
        redis.hset(base_key, RK_RULE_LIMITING_CHECK_FAILED,     self.r_Pagepermin.id)

        # Rate Limiting Check Failed
        redis.hset(base_key, "{}{}".format(RK_RULE_LIMITING_CHECK_FAILED,
                                           RK_RULE_PAGE_PER_SESSION_EXCEEDS),
                             self.r_pagepersess.id)
        redis.hset(base_key, "{}{}".format(RK_RULE_LIMITING_CHECK_FAILED,
                                           RK_RULE_SESSION_LENGTH_EXCEEDS),
                             self.r_sesslength.id)

        # Rate Limiting Rules
        redis.hset(base_key, RK_RULE_PAGE_PER_MINUTE_EXCEEDS,   self.pagepermin)
        redis.hset(base_key, RK_RULE_PAGE_PER_SESSION_EXCEEDS,  self.pagepersess)
        redis.hset(base_key, RK_RULE_SESSION_LENGTH_EXCEEDS,    self.sesslength)

        super(Subscriber, self).save(*args, **kwargs)

    def delete(self, using=None):
        redis = get_cache('default').raw_client

        base_key = "{}:{}".format(RK_RULE_BASE, self.internal_sid)
        base_key_1 = "{}:{}".format(RK_RULE_BASE, self.sb_internal_sid)

        # Verify Integration
        redis.hdel(base_key,    RK_VERIFY_INT)
        redis.hdel(base_key_1,  RK_VERIFY_INT)

        redis.hdel(RK_SID_MAP,      self.external_sid)
        redis.hdel(RK_SID_MIN_MAP,  self.mini_uuid)

        redis.hdel(RK_SID_MAP,      self.sb_external_sid)
        redis.hdel(RK_SID_MIN_MAP,  self.sb_mini_uuid)

        # Bot Response Rules
        redis.hdel(base_key, RK_RULE_BROWSER_INTGRITY)
        redis.hdel(base_key, RK_RULE_HTTP_REQUEST_INTEGRITY)
        redis.hdel(base_key, RK_RULE_AGGREGATOR)
        redis.hdel(base_key, RK_RULE_BEHAVIOUR_INTEGRITY)

        # Rate Limiting Check Failed
        redis.hdel(base_key, "{}{}".format(RK_RULE_LIMITING_CHECK_FAILED,
                                           RK_RULE_PAGE_PER_MINUTE_EXCEEDS))
        redis.hdel(base_key, "{}{}".format(RK_RULE_LIMITING_CHECK_FAILED,
                                           RK_RULE_PAGE_PER_SESSION_EXCEEDS))
        redis.hdel(base_key, "{}{}".format(RK_RULE_LIMITING_CHECK_FAILED,
                                           RK_RULE_SESSION_LENGTH_EXCEEDS))

        # Rate Limiting Rules
        redis.hdel(base_key, RK_RULE_PAGE_PER_MINUTE_EXCEEDS)
        redis.hdel(base_key, RK_RULE_PAGE_PER_SESSION_EXCEEDS)
        redis.hdel(base_key, RK_RULE_SESSION_LENGTH_EXCEEDS)

        super(Subscriber, self).delete(using)

    class Meta:
        unique_together = ('site_url', 'email',)
        db_table = "subscriber"

    def __unicode__(self):
        return u"<{}: {}>".format(self.internal_sid, self.site_url)


class RulesSummary(models.Model):
    sid     =   models.ForeignKey(Subscriber, db_column="sid")
    dt      =   models.DateField()

    r_browserIntgrity       =   models.BigIntegerField()
    r_httpRequestIntegrity  =   models.BigIntegerField()
    r_Aggregator            =   models.BigIntegerField()
    r_behaviourIntegrity    =   models.BigIntegerField()
    r_Ratelimiting          =   models.BigIntegerField()

    genuineusers            =   models.BigIntegerField()

    # This will have total value of all 24 hours
    trustedbots             =   models.BigIntegerField()
    badbots                 =   models.BigIntegerField()

    monitor                 =   models.BigIntegerField()
    captcha                 =   models.BigIntegerField()
    block                   =   models.BigIntegerField()
    feedfakedata            =   models.BigIntegerField()

    all_js                  =   models.BigIntegerField()
    all_api                 =   models.BigIntegerField()

    genuineusers0 = models.BigIntegerField()
    trustedbots0 = models.BigIntegerField()
    badbots0 = models.BigIntegerField()
    all_js0 = models.BigIntegerField()
    all_api0 = models.BigIntegerField()

    genuineusers1 = models.BigIntegerField()
    trustedbots1 = models.BigIntegerField()
    badbots1 = models.BigIntegerField()
    all_js1 = models.BigIntegerField()
    all_api1 = models.BigIntegerField()

    genuineusers2 = models.BigIntegerField()
    trustedbots2 = models.BigIntegerField()
    badbots2 = models.BigIntegerField()
    all_js2 = models.BigIntegerField()
    all_api2 = models.BigIntegerField()

    genuineusers3 = models.BigIntegerField()
    trustedbots3 = models.BigIntegerField()
    badbots3 = models.BigIntegerField()
    all_js3 = models.BigIntegerField()
    all_api3 = models.BigIntegerField()

    genuineusers4 = models.BigIntegerField()
    trustedbots4 = models.BigIntegerField()
    badbots4 = models.BigIntegerField()
    all_js4 = models.BigIntegerField()
    all_api4 = models.BigIntegerField()

    genuineusers5 = models.BigIntegerField()
    trustedbots5 = models.BigIntegerField()
    badbots5 = models.BigIntegerField()
    all_js5 = models.BigIntegerField()
    all_api5 = models.BigIntegerField()

    genuineusers6 = models.BigIntegerField()
    trustedbots6 = models.BigIntegerField()
    badbots6 = models.BigIntegerField()
    all_js6 = models.BigIntegerField()
    all_api6 = models.BigIntegerField()

    genuineusers7 = models.BigIntegerField()
    trustedbots7 = models.BigIntegerField()
    badbots7 = models.BigIntegerField()
    all_js7 = models.BigIntegerField()
    all_api7 = models.BigIntegerField()

    genuineusers8 = models.BigIntegerField()
    trustedbots8 = models.BigIntegerField()
    badbots8 = models.BigIntegerField()
    all_js8 = models.BigIntegerField()
    all_api8 = models.BigIntegerField()

    genuineusers9 = models.BigIntegerField()
    trustedbots9 = models.BigIntegerField()
    badbots9 = models.BigIntegerField()
    all_js9 = models.BigIntegerField()
    all_api9 = models.BigIntegerField()

    genuineusers10 = models.BigIntegerField()
    trustedbots10 = models.BigIntegerField()
    badbots10 = models.BigIntegerField()
    all_js10 = models.BigIntegerField()
    all_api10 = models.BigIntegerField()

    genuineusers11 = models.BigIntegerField()
    trustedbots11 = models.BigIntegerField()
    badbots11 = models.BigIntegerField()
    all_js11 = models.BigIntegerField()
    all_api11 = models.BigIntegerField()

    genuineusers12 = models.BigIntegerField()
    trustedbots12 = models.BigIntegerField()
    badbots12 = models.BigIntegerField()
    all_js12 = models.BigIntegerField()
    all_api12 = models.BigIntegerField()

    genuineusers13 = models.BigIntegerField()
    trustedbots13 = models.BigIntegerField()
    badbots13 = models.BigIntegerField()
    all_js13 = models.BigIntegerField()
    all_api13 = models.BigIntegerField()

    genuineusers14 = models.BigIntegerField()
    trustedbots14 = models.BigIntegerField()
    badbots14 = models.BigIntegerField()
    all_js14 = models.BigIntegerField()
    all_api14 = models.BigIntegerField()

    genuineusers15 = models.BigIntegerField()
    trustedbots15 = models.BigIntegerField()
    badbots15 = models.BigIntegerField()
    all_js15 = models.BigIntegerField()
    all_api15 = models.BigIntegerField()

    genuineusers16 = models.BigIntegerField()
    trustedbots16 = models.BigIntegerField()
    badbots16 = models.BigIntegerField()
    all_js16 = models.BigIntegerField()
    all_api16 = models.BigIntegerField()

    genuineusers17 = models.BigIntegerField()
    trustedbots17 = models.BigIntegerField()
    badbots17 = models.BigIntegerField()
    all_js17 = models.BigIntegerField()
    all_api17 = models.BigIntegerField()

    genuineusers18 = models.BigIntegerField()
    trustedbots18 = models.BigIntegerField()
    badbots18 = models.BigIntegerField()
    all_js18 = models.BigIntegerField()
    all_api18 = models.BigIntegerField()

    genuineusers19 = models.BigIntegerField()
    trustedbots19 = models.BigIntegerField()
    badbots19 = models.BigIntegerField()
    all_js19 = models.BigIntegerField()
    all_api19 = models.BigIntegerField()

    genuineusers20 = models.BigIntegerField()
    trustedbots20 = models.BigIntegerField()
    badbots20 = models.BigIntegerField()
    all_js20 = models.BigIntegerField()
    all_api20 = models.BigIntegerField()

    genuineusers21 = models.BigIntegerField()
    trustedbots21 = models.BigIntegerField()
    badbots21 = models.BigIntegerField()
    all_js21 = models.BigIntegerField()
    all_api21 = models.BigIntegerField()

    genuineusers22 = models.BigIntegerField()
    trustedbots22 = models.BigIntegerField()
    badbots22 = models.BigIntegerField()
    all_js22 = models.BigIntegerField()
    all_api22 = models.BigIntegerField()

    genuineusers23 = models.BigIntegerField()
    trustedbots23 = models.BigIntegerField()
    badbots23 = models.BigIntegerField()
    all_js23 = models.BigIntegerField()
    all_api23 = models.BigIntegerField()

    class Meta:
        unique_together = ('sid', 'dt',)
        db_table = "rulessummary"

    def __unicode__(self):
        return u"Rules Summary, sid: {}".format(self.sid)


class IpDetails(models.Model):
    ip_address      =   models.CharField(max_length=75, db_column="ip_address", unique=True)
    country_name    =   models.CharField(max_length=255)
    city_name       =   models.CharField(max_length=255)
    isp             =   models.CharField(max_length=255)
    domain          =   models.CharField(max_length=255)

    class Meta:
        db_table = "ip_details"

    def __unicode__(self):
        return u"{}".format(self.ip_address)


class IpAccessType(models.Model):
    type    =   models.CharField(max_length = 50)

    class Meta:
        db_table = 'ip_access_type'

    def __unnicode__(self):
        return "Ip Access Type : {}".format(self.type)


class IpAddressAccessList(models.Model):
    sid             =   models.ForeignKey(Subscriber, db_column="sid")
    ipaddress       =   models.CharField(max_length = 75, db_column="ip_address", unique = True)
    type            =   models.ForeignKey(IpAccessType, db_column='type')
    change_dt       =   models.DateTimeField(default = datetime.datetime.utcnow())
    def save(self, *args, **kwargs):
        redis       = get_cache('default').raw_client
        key = RK_WHITE_LIST

        redis.sadd("{}:{}".format(key, self.sid.internal_sid), self.ipaddress)

        base_key  = "{}:{}".format(RK_IP_ACTION_BASE, self.sid.internal_sid)
        redis.hdel(base_key, self.ipaddress)

        super(IpAddressAccessList, self).save(*args, **kwargs)

    def delete(self, using=None):
        redis   = get_cache('default').raw_client
        key     = RK_WHITE_LIST

        redis.srem("{}:{}".format(key, self.sid.internal_sid), self.ipaddress)

        super(IpAddressAccessList, self).delete(using)

    class Meta:
        unique_together = ('sid', 'ipaddress',)
        db_table = "ip_address_access_list"

    def __unicode__(self):
        return u"{}: {}[{}]".format(self.sid, self.ipaddress, "WL")


class IpAnalysis(models.Model):
    sid             =   models.ForeignKey(Subscriber, db_column="sid")
    dt              =   models.DateTimeField()
    ipaddress       =   models.ForeignKey(IpDetails, db_column="ip_address")

    totalrequests           =   models.BigIntegerField(db_column="total_requests")
    browserIntgrity         =   models.BigIntegerField(db_column="browser_integrity")
    httpRequestIntegrity    =   models.BigIntegerField(db_column="http_request_integrity")
    Aggregator              =   models.BigIntegerField(db_column="aggregator")
    behaviourIntegrity      =   models.BigIntegerField(db_column="behavior_integrity")
    Ratelimiting            =   models.BigIntegerField(db_column="rate_limiting")

    genuinerequests         =   models.BigIntegerField(db_column="genuine_requests")

    class Meta:
        unique_together = ('sid', 'dt', 'ipaddress',)
        db_table = "ip_analysis"

    @classmethod
    def get_all_whitelisted_ips(cls, sid, end_date):
        whitelisted_ips = []
        whitelisted_ip_address_access_list = IpAddressAccessList.objects.filter(sid = sid,
                                                                                type = 1,
                                                                                change_dt__lt = end_date)
        for whitelisted_ip_address_access in whitelisted_ip_address_access_list:
            whitelisted_ips.append(whitelisted_ip_address_access.ipaddress)
        return whitelisted_ips


class IpStatus(models.Model):
    status = models.CharField(max_length = 50)

    class Meta:
        db_table = "ip_status"

    def __unicode__(self):
        return self.status


class IpActions(models.Model):
    sid         =   models.ForeignKey(Subscriber, db_column = 'sid')
    ip_address  =   models.ForeignKey(IpDetails, db_column = 'ip_address')
    expiry_date =   models.DateField()
    status      =   models.ForeignKey(IpStatus, db_column = 'status', default=0)
    action      =   models.ForeignKey(ResponseCode, db_column = 'action')

    class Meta:
        unique_together = ('sid', 'ip_address',)
        db_table = "ip_actions"

    def __unicode__(self):
        return u"IP Address: {}, Expiry Date: {}".format(self.ip_address, self.expiry_date)


class UserSubscriber(models.Model):
    user        =   models.OneToOneField(User)
    subscriber  =   models.ForeignKey(Subscriber)

    def __unicode__(self):
        return u"User: {}, Subscriber: {}".format(self.user, self.subscriber)

class VerifyRegistration(models.Model):
    sid             = models.ForeignKey(Subscriber, db_column = 'sid')
    activation_link = models.CharField(max_length = 250, db_column = 'activation_link')
    is_activated    = models.BooleanField(default = False)
    activation_dt   = models.DateTimeField()
    password        = models.CharField(max_length = 250)

    def save(self, *args, **kwargs):
        self.activation_dt = datetime.datetime.utcnow()
        super(VerifyRegistration, self).save(*args, **kwargs)

    class Meta:
        db_table = "verify_registration"

    def __unicode__(self):
        return u"Subscriber: {}, Activation Link: {}".format(self.sid, self.activation_link)
