"""
1. TABLE user_ip_details :
    Create TABLE dbo.user_ip_details (
    id bigint IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,
    ip_address VARCHAR (50),
    country_name VARCHAR(50),
    city_name VARCHAR(50),
    isp VARCHAR(255),
    domain VARCHAR(255),
    CONSTRAINT uc_user_ip_details UNIQUE (ip_address)
);

2. TABLE user_analysis :
    Create TABLE dbo.user_analysis(
    id bigint IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,
    sid int ,
    user_id VARCHAR(50) ,
    dt datetime,
    ip_address bigint,
    total_requests bigint,
    CONSTRAINT uc_user_analysis UNIQUE (sid,user_id,dt,ip_address) ,
    FOREIGN KEY (sid) REFERENCES subscriber(internal_sid),
    FOREIGN KEY (ip_address) REFERENCES user_ip_details(id)
    );
"""

from django.db import models

from ip_analysis.models import Subscriber


class UserIpDetails(models.Model):
    ip_address      = models.CharField(max_length = 50, unique = True)
    country_name    = models.CharField(max_length = 50)
    city_name       = models.CharField(max_length = 50)
    isp             = models.CharField(max_length = 255)
    domain          = models.CharField(max_length = 255)

    class Meta:
        db_table = 'user_ip_details'

    def __unicode__(self):
        return "User IP Address : {}".format(self.ip_address)


class UserAnalysis(models.Model):
    sid             = models.ForeignKey(Subscriber, db_column = 'sid')
    user_id         = models.CharField(max_length = 50)
    dt              = models.DateTimeField()
    ip_address      = models.ForeignKey(UserIpDetails, db_column = 'ip_address')
    total_requests  = models.BigIntegerField()

    def get_no_of_distinct_ips(self, sid, user_id, dt_from, dt_to):
        no_of_distinct_ips = UserAnalysis.objects.filter(sid = sid, user_id = user_id, dt__range = [dt_from, dt_to]).values_list('ip_address').distinct()
        return no_of_distinct_ips

    class Meta:
        unique_together = ('sid','user_id','dt','ip_address',)
        db_table = 'user_analysis'

    def __unicode__(self):
        return "User ID : {}".format(self.user_id)
