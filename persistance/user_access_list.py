from django.core.cache import get_cache
from django.db import models

from ip_analysis.models import Subscriber
from utils.constants import RK_USER_ACCESS_BASE


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

