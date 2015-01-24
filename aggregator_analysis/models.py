from django.db import models

from ip_analysis.models import Subscriber, ResponseCode, IpStatus


class AggregatorDetails(models.Model):
    ip_address      =   models.CharField(max_length=50, unique=True)
    country_name    =   models.CharField(max_length=50)
    city_name       =   models.CharField(max_length=50)
    isp             =   models.CharField(max_length=255)
    aggregator_name =   models.CharField(max_length=255)

    class Meta:
        db_table    =   'aggregator_details'

    def __unicode__(self):
        return "IP Address : {}".format(self.ip_address)

class AggregatorAnalysis(models.Model):
    sid             =   models.ForeignKey(Subscriber, db_column = 'sid')
    dt              =   models.DateTimeField()
    ip_address      =   models.ForeignKey(AggregatorDetails, db_column = 'ip_address')
    total_requests  =   models.BigIntegerField()

    class Meta:
        unique_together =   ('sid', 'dt', 'ip_address')
        db_table        =   'aggregator_analysis'

    def __unicode__(self):
        return "Subscriber : {}, IP Address : {}".format(self.sid, self.ip_address)

class AggregatorActions(models.Model):
    sid         =   models.ForeignKey(Subscriber, db_column = 'sid')
    ip_address  =   models.ForeignKey(AggregatorDetails, db_column = 'ip_address')
    expiry_date =   models.DateField()
    status      =   models.ForeignKey(IpStatus, db_column = 'status')
    action      =   models.ForeignKey(ResponseCode, db_column = 'action')

    class Meta:
        db_table = 'aggregator_actions'
        unique_together = ('sid', 'ip_address',)

    def __unicode__(self):
        return "Subscriber : {}, IP Address : {} --> Action : {}".format(self.sid, self.ip_address, self.action)