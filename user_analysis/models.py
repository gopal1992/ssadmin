from django.core.cache import get_cache
from django.db import models

from ip_analysis.models import Subscriber
from utils.constants import RK_USER_ACCESS_BASE, RK_RULE_BASE, RK_USER_ACCESS, \
    RK_IP_ACCESS, RK_IP_ANALYSIS, RK_USER_ANALYSIS


class PagesList(models.Model):
    page_name   =   models.CharField(max_length = 50)

    class Meta:
        db_table = "pages_list"

    def __unicode__(self):
        return self.page_name

class PageAuthAction(models.Model):
    auth_action   =   models.CharField(max_length = 50)

    class Meta:
        db_table = 'page_auth_action'

    def __unicode__(self):
        return self.auth_action


class SubscriberPageAuth(models.Model):
    sid         = models.ForeignKey(Subscriber,     db_column = 'sid')
    page_id     = models.ForeignKey(PagesList,      db_column = 'page_id')
    auth_id     = models.ForeignKey(PageAuthAction, db_column = 'auth_id')

    def save(self, *args, **kwargs):
        redis = get_cache('default').raw_client
        base_key = "{}:{}".format(RK_RULE_BASE,     self.sid.internal_sid)

        if self.page_id.id == 1:
            redis.hset(base_key, RK_USER_ACCESS,    self.auth_id)
        if self.page_id.id == 2:
            redis.hset(base_key, RK_USER_ANALYSIS,  self.auth_id)
        if self.page_id.id == 3:
            redis.hset(base_key, RK_IP_ACCESS,      self.auth_id)
        if self.page_id.id == 4:
            redis.hset(base_key, RK_IP_ANALYSIS,    self.auth_id)

        super(SubscriberPageAuth, self).save(*args, **kwargs)

    class Meta:
        db_table = 'subscriber_page_auth'

    def __unicode__(self):
        return "Subscriber : {}, page : {} -> action : {}".format(self.sid, self.page_id, self.auth_id)


class UserAccessStatus(models.Model):
    status  = models.CharField(max_length = 50)

    class Meta:
        db_table = 'user_access_status'

    def __unicode__(self):
        return "Status : {}".format(self.status)


class UserAccessType(models.Model):
    type  = models.CharField(max_length = 50)

    class Meta:
        db_table = 'user_access_type'

    def __unicode__(self):
        return "Type : {}".format(self.type)


class UserAccessList(models.Model):
    user_id     = models.CharField(max_length = 50)
    sid         = models.ForeignKey(Subscriber,         db_column = 'sid')
    type        = models.ForeignKey(UserAccessType,     db_column = 'type')
    status      = models.ForeignKey(UserAccessStatus,   db_column = 'status')
    change_dt   = models.DateTimeField()

    class Meta:
        unique_together = ('sid', 'user_id',)
        db_table = 'user_access_list'

    def save(self, *args, **kwargs):
        redis = get_cache('default').raw_client
        base_key = "{}:{}".format(RK_USER_ACCESS_BASE, self.sid.internal_sid)

        redis.hdel(base_key, self.user_id)

        super(UserAccessList, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Subscriber : {}, User ID : {}".format(self.sid, self.user_id)

