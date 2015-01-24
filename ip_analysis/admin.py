from django.contrib import admin

from ip_analysis.models import ResponseCode, Subscriber, RulesSummary, IpDetails, \
    IpAnalysis, UserSubscriber, IpAddressAccessList


admin.site.register(ResponseCode)
admin.site.register(Subscriber)
admin.site.register(RulesSummary)
admin.site.register(IpDetails)
admin.site.register(IpAddressAccessList)
admin.site.register(IpAnalysis)
admin.site.register(UserSubscriber)