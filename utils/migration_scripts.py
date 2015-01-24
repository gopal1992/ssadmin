from datetime import timedelta
import datetime

from django.db.utils import IntegrityError

from data_migration.models import OldRulesSummary, NewRulesSummary, \
    OldIpAnalysis, NewIpAnalysis, OldIpDetails, NewIpDetails, NewIpActions
from ip_analysis.models import Subscriber, IpDetails, ResponseCode, IpStatus
from utils.datetime_utils import convert_date_to_datetime_with_delta, \
    convert_date_to_datetime


def rules_summary_migration():
    print datetime.datetime.now()
    with open('rules_summary.txt', 'w') as fd:
        for old_rules_summary in OldRulesSummary.objects.filter(dt__lte='2014-09-07'):
            if old_rules_summary.r_browserIntgrity > 23:
                r_browserIntgrity = old_rules_summary.r_browserIntgrity
                r_browserIntgrity_delta = r_browserIntgrity % 24
                r_browserIntgrity -= r_browserIntgrity_delta
                r_browserIntgrity /= 24
            else:
                browserIntgrity = True
                r_browserIntgrity = old_rules_summary.r_browserIntgrity

            if old_rules_summary.r_httpRequestIntegrity > 23:
                r_httpRequestIntegrity = old_rules_summary.r_httpRequestIntegrity
                r_httpRequestIntegrity_delta = r_httpRequestIntegrity % 24
                r_httpRequestIntegrity -= r_httpRequestIntegrity_delta
                r_httpRequestIntegrity /= 24
            else:
                httpRequestIntegrity = True
                r_httpRequestIntegrity = old_rules_summary.r_httpRequestIntegrity

            if old_rules_summary.r_Aggregator > 23:
                r_Aggregator = old_rules_summary.r_Aggregator
                r_Aggregator_delta = r_Aggregator % 24
                r_Aggregator -= r_Aggregator_delta
                r_Aggregator /= 24
            else:
                Aggregator = True
                r_Aggregator = old_rules_summary.r_Aggregator

            if old_rules_summary.r_behaviourIntegrity > 23:
                r_behaviourIntegrity = old_rules_summary.r_behaviourIntegrity
                r_behaviourIntegrity_delta = r_behaviourIntegrity % 24
                r_behaviourIntegrity -= r_behaviourIntegrity_delta
                r_behaviourIntegrity /= 24
            else:
                behaviourIntegrity = True
                r_behaviourIntegrity = old_rules_summary.r_behaviourIntegrity

            if old_rules_summary.r_Ratelimiting > 23:
                r_Ratelimiting = old_rules_summary.r_Ratelimiting
                r_Ratelimiting_delta = r_Ratelimiting % 24
                r_Ratelimiting -= r_Ratelimiting_delta
                r_Ratelimiting /= 24
            else:
                Ratelimiting = True
                r_Ratelimiting = old_rules_summary.r_Ratelimiting

            if old_rules_summary.monitor > 23:
                monitor = old_rules_summary.monitor
                monitor_delta = monitor % 24
                monitor -= monitor_delta
                monitor /= 24
            else:
                montr = True
                monitor = old_rules_summary.monitor

            if old_rules_summary.captcha > 23:
                captcha = old_rules_summary.captcha
                captcha_delta = captcha % 24
                captcha -= captcha_delta
                captcha /= 24
            else:
                cpcha = True
                captcha = old_rules_summary.captcha

            if old_rules_summary.block > 23:
                block = old_rules_summary.block
                block_delta = block % 24
                block -= block_delta
                block /= 24
            else:
                blk = True
                block = old_rules_summary.block

            if old_rules_summary.feedfakedata > 23:
                feedfakedata = old_rules_summary.feedfakedata
                feedfakedata_delta = feedfakedata % 24
                feedfakedata -= feedfakedata_delta
                feedfakedata /= 24
            else:
                ffdata = True
                feedfakedata = old_rules_summary.feedfakedata

            for i in range(24):
                line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"\
                .format(int(old_rules_summary.sid.internal_sid),
                        str(convert_date_to_datetime_with_delta(old_rules_summary.dt, i)),
                        int(r_browserIntgrity if i == 23 else 0) if browserIntgrity else int(r_browserIntgrity + r_browserIntgrity_delta if i == 23 else r_browserIntgrity),
                        int(r_httpRequestIntegrity if i == 23 else 0) if httpRequestIntegrity else int(r_httpRequestIntegrity + r_httpRequestIntegrity_delta if i == 23 else r_httpRequestIntegrity),
                        int(r_Aggregator if i == 23 else 0) if Aggregator else int(r_Aggregator + r_Aggregator_delta if i == 23 else r_Aggregator),
                        int(r_behaviourIntegrity if i == 23 else 0) if behaviourIntegrity else int(r_behaviourIntegrity + r_behaviourIntegrity_delta if i == 23 else r_behaviourIntegrity),
                        int(r_Ratelimiting if i == 23 else 0) if Ratelimiting else int(r_Ratelimiting + r_Ratelimiting_delta if i == 23 else r_Ratelimiting),
                        int(monitor if i == 23 else 0) if montr else int(monitor + monitor_delta if i == 23 else monitor),
                        int(captcha if i == 23 else 0) if cpcha else int(captcha + captcha_delta if i == 23 else captcha),
                        int(block if i == 23 else 0) if blk else int(block + block_delta if i == 23 else block),
                        int(feedfakedata if i == 23 else 0) if ffdata else int(feedfakedata + feedfakedata_delta if i == 23 else feedfakedata),
                        int(eval ('old_rules_summary.genuineusers' + str(i))),
                        int(eval ('old_rules_summary.trustedbots' + str(i))),
                        int(eval ('old_rules_summary.badbots' + str(i))),
                        int(eval ('old_rules_summary.all_js' + str(i))),
                        int(eval ('old_rules_summary.all_api' + str(i)))
                        )
                fd.write(line)
    with open('rules_summary.txt', 'r') as fd:
        for line in fd:
            record = line.split(',')
            instance = Subscriber.objects.get(internal_sid = int(record[0]))
            print instance, datetime.datetime.strptime(str(record[1]), "%Y-%m-%d %H:%M:%S")
            try:
                NewRulesSummary.objects.get_or_create\
                (sid                      = instance,
                 dt                       = datetime.datetime.strptime(str(record[1]), "%Y-%m-%d %H:%M:%S"),
                 r_browser_integrity      = record[2],
                 r_http_request_integrity = record[3],
                 r_aggregator             = record[4],
                 r_behaviour_integrity    = record[5],
                 r_rate_limiting          = record[6],
                 monitor                  = record[7],
                 captcha                  = record[8],
                 block                    = record[9],
                 feed_fake_data           = record[10],
                 genuine_users            = record[11],
                 trusted_bots             = record[12],
                 bad_bots                 = record[13],
                 all_js                   = record[14],
                 all_api                  = record[15]
                )
            except IntegrityError as e:
                print e
    print datetime.datetime.now()

def ip_analysis_migration():
    with open('ip_analysis.txt', 'w') as fd:
        counter = 0
        for old_ip_analysis in OldIpAnalysis.objects.all():
            line = "{},{},{},{},{},{},{},{},{},{}\n"\
            .format(int(old_ip_analysis.sid.internal_sid),
                    str(convert_date_to_datetime(old_ip_analysis.dt)),
                    int(old_ip_analysis.ipaddress.id),
                    int(old_ip_analysis.totalrequests),
                    int(old_ip_analysis.browserIntgrity),
                    int(old_ip_analysis.httpRequestIntegrity),
                    int(old_ip_analysis.Aggregator),
                    int(old_ip_analysis.behaviourIntegrity),
                    int(old_ip_analysis.Ratelimiting),
                    int(old_ip_analysis.genuinerequests),
                    )
            print "Writing :", counter, line
            counter = counter + 1
            fd.write(line)

    lines = open('ip_analysis.txt').readlines()
    counter = 0
    for line in lines:
        print counter, line
        counter = counter + 1
        record = line.split(',')
        subscriber  = Subscriber.objects.get(internal_sid = record[0])
        ip_details   = IpDetails.objects.get(id = record[2])
        try:
            NewIpAnalysis.objects.get_or_create\
            (sid                      = subscriber,
             dt                       = datetime.datetime.strptime(str(record[1]), "%Y-%m-%d %H:%M:%S"),
             ip_address               = ip_details,
             total_requests           = int(record[3]),
             browser_integrity        = int(record[4]),
             http_request_integrity   = int(record[5]),
             aggregator               = int(record[6]),
             behavior_integrity       = int(record[7]),
             rate_limiting            = int(record[8]),
             genuine_requests         = int(record[9])
            )
        except IntegrityError as e:
            print e

def ip_details_migration():
    with open('ip_details.txt', 'w') as fd:
        for old_ip_detail in OldIpDetails.objects.all():
            line = "{},{},{},{},{},{}\n"\
            .format(old_ip_detail.id,
                    str(old_ip_detail.ipaddress),
                    str(old_ip_detail.country_name),
                    str(old_ip_detail.city_name),
                    str(old_ip_detail.isp),
                    str(old_ip_detail.domain)
                    )
            fd.write(line)
            print "Writing : ", line
    with open('ip_details.txt', 'r') as fd:
        for line in fd:
            print "Reading : ", line
            record = line.split(',')
            print record[0]
            try:
                NewIpDetails.objects.get_or_create\
                (id = record[0],
                ip_address = record[1],
                country_name= record[2],
                city_name   = record[3],
                isp         = record[4],
                domain      = record[5],
                )
            except IntegrityError as e:
                print e

def ip_actions():
    with open('ip_analysis.txt', 'w') as fd:
        counter = 0
        for old_ip_analysis in NewIpAnalysis.objects.all().order_by('-dt'):
            line = "{},{},{}\n"\
            .format(int(old_ip_analysis.sid.internal_sid),
                    str(convert_date_to_datetime(old_ip_analysis.dt)),
                    int(old_ip_analysis.ip_address.id)
                    )
            print "Writing :", counter, line
            counter = counter + 1
            fd.write(line)

    lines = open('ip_analysis.txt').readlines()
    counter = 0
    for line in lines:
        print counter, line
        counter = counter + 1
        record = line.split(',')
        subscriber    = Subscriber.objects.get(internal_sid = record[0])
        ip_details    = NewIpDetails.objects.get(id = record[2])
        action0     = ResponseCode.objects.get(id=0) #Allow
        action1     = ResponseCode.objects.get(id=2) #Show Captcha
        status0     = IpStatus.objects.get(id=0) #Clean
        status1     = IpStatus.objects.get(id=1) #Malicious

        try:
            if datetime.datetime.strptime(record[1], "%Y-%m-%d") < datetime.datetime(2014, 8, 25, 0, 0):
                i = NewIpActions.objects.create\
                (sid                      = subscriber,
                 ip_address               = ip_details,
                 expiry_date              = datetime.datetime.strptime(record[1], "%Y-%m-%d"),
                 status                   = status0,
                 action                   = action0)
                i.save()
            else:
                i = NewIpActions.objects.create\
                (sid                     = subscriber,
                 ip_address               = ip_details,
                 expiry_date              = datetime.date.today() + timedelta(days=7),
                 status                   = status1,
                 action                   = action1)
                i.save()
        except IntegrityError as e:
            print e

'''
Subscriber table migration scripts:

EXEC sp_RENAME 'subscriber.r_browserIntgrity', 'browser_integrity_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.r_httpRequestIntegrity', 'http_request_integrity_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.r_Aggregator', 'aggregator_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.r_behaviourIntegrity', 'behaviour_integrity_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.r_Pagepermin', 'page_per_min_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.r_pagepersess', 'page_per_sess_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.r_sesslength', 'sess_length_resp', 'COLUMN'
EXEC sp_RENAME 'subscriber.Pagepermin', 'page_per_min_limit', 'COLUMN'
EXEC sp_RENAME 'subscriber.pagepersess', 'page_per_sess_limit', 'COLUMN'
EXEC sp_RENAME 'subscriber.sesslength', 'sess_length_limit', 'COLUMN'

ALTER TABLE subscriber ADD site_url varchar(250) NOT NULL DEFAULT 'http://example.com'

ALTER TABLE subscriber ADD mini_uuid varchar(200) NOT NULL DEFAULT 1234
'''

for item in Subscriber.objects.all():
    external_id = item.external_sid
    try:
        item.mini_uuid   = str(external_id).split('-')[3]
    except IndexError:
        pass
    item.save()