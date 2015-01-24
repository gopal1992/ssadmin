from django.db import models

from ip_analysis.models import Subscriber, IpDetails, IpStatus, ResponseCode


# Create your models here.
class OldRulesSummary(models.Model):
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


class NewRulesSummary(models.Model):
    sid                     =   models.ForeignKey(Subscriber, db_column="sid")
    dt                      =   models.DateTimeField()
    r_browser_integrity       =   models.BigIntegerField()
    r_http_request_integrity  =   models.BigIntegerField()
    r_aggregator            =   models.BigIntegerField()
    r_behaviour_integrity    =   models.BigIntegerField()
    r_rate_limiting          =   models.BigIntegerField()
    monitor                 =   models.BigIntegerField(db_column = 'allow')
    captcha                 =   models.BigIntegerField()
    block                   =   models.BigIntegerField()
    feed_fake_data            =   models.BigIntegerField()
    genuine_users            =   models.BigIntegerField()
    trusted_bots             =   models.BigIntegerField()
    bad_bots                 =   models.BigIntegerField()
    all_js                  =   models.BigIntegerField()
    all_api                 =   models.BigIntegerField()

    class Meta:
        unique_together = ('sid', 'dt',)
        db_table = "rules_summary"

    def __unicode__(self):
        return u"Rules Summary, sid: {}".format(self.sid)

class OldIpDetails(models.Model):
    ipaddress       =   models.CharField(max_length=75, db_column="ipaddress", unique=True)
    country_name    =   models.CharField(max_length=255)
    city_name       =   models.CharField(max_length=255)
    isp             =   models.CharField(max_length=255)
    domain          =   models.CharField(max_length=255)

    class Meta:
        db_table = "ipdetails"

    def __unicode__(self):
        return u"{}".format(self.ip_address)

class NewIpDetails(models.Model):
    ip_address      =   models.CharField(max_length=75, db_column="ip_address", unique=True)
    country_name    =   models.CharField(max_length=255)
    city_name       =   models.CharField(max_length=255)
    isp             =   models.CharField(max_length=255)
    domain          =   models.CharField(max_length=255)

    class Meta:
        db_table = "ip_details"

    def __unicode__(self):
        return u"{}".format(self.ip_address)

class OldIpAnalysis(models.Model):
    sid                     =   models.ForeignKey(Subscriber, db_column="sid")
    dt                      =   models.DateField()
    ipaddress               =   models.ForeignKey(OldIpDetails, db_column="ipaddress")
    totalrequests           =   models.BigIntegerField()
    browserIntgrity         =   models.BigIntegerField()
    httpRequestIntegrity    =   models.BigIntegerField()
    Aggregator              =   models.BigIntegerField()
    behaviourIntegrity      =   models.BigIntegerField()
    Ratelimiting            =   models.BigIntegerField()
    genuinerequests         =   models.BigIntegerField()

    def __unicode__(self):
        return u"Ip Analysis sid: {} {} {}".format(self.sid, self.dt, self.ipaddress)

    class Meta:
        unique_together = ('sid', 'dt', 'ipaddress',)
        db_table = "ipanalysis"

class NewIpAnalysis(models.Model):
    sid                     =   models.ForeignKey(Subscriber, db_column="sid")
    dt                      =   models.DateTimeField()
    ip_address              =   models.ForeignKey(IpDetails, db_column="ip_address")
    total_requests          =   models.BigIntegerField()
    browser_integrity       =   models.BigIntegerField()
    http_request_integrity  =   models.BigIntegerField()
    aggregator              =   models.BigIntegerField()
    behavior_integrity      =   models.BigIntegerField()
    rate_limiting           =   models.BigIntegerField()
    genuine_requests        =   models.BigIntegerField()

    class Meta:
        unique_together = ('sid', 'dt', 'ip_address',)
        db_table = "ip_analysis"

class NewIpActions(models.Model):
    sid         =   models.ForeignKey(Subscriber, db_column = 'sid')
    ip_address  =   models.ForeignKey(NewIpDetails, db_column = 'ip_address')
    expiry_date =   models.DateField()
    status      =   models.ForeignKey(IpStatus, db_column = 'status')
    action      =   models.ForeignKey(ResponseCode, db_column = 'action')

    class Meta:
        unique_together = ('sid', 'ip_address',)
        db_table = "ip_actions"