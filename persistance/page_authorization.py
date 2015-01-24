from django.core.cache import get_cache
from django.db import models

from ip_analysis.models import Subscriber
from utils.constants import RK_RULE_BASE, RK_USER_ACCESS, RK_USER_ANALYSIS, \
    RK_IP_ACCESS, RK_IP_ANALYSIS


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

