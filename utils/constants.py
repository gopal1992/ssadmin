# -*- coding: utf-8 -*-

ACCESS_STATUS_ALLOW = True
ACCESS_STATUS_DENY  = False

ACCESS_STATUS = [ACCESS_STATUS_ALLOW, ACCESS_STATUS_DENY]

ACCESS_STATUS_MAP = {ACCESS_STATUS_DENY: False, ACCESS_STATUS_ALLOW: True}


RULES_ACTION = [(1, 'Allow'),
                (2, 'Show Captcha'),
                (3, 'Block'),
                (4, 'Feed Fake Data')
                ]

RULES_ACTION_1 = [(0, 'Allow'),
                  (2, 'Show Captcha'),
                  (3, 'Block'),
                  (4, 'Feed Fake Data')
                  ]

# User Analysis, User Access List pages

USER_ACCESS_TYPE_WHITELIST    = True  #Whitelist
USER_ACCESS_TYPE_BLACKLIST    = False #Blacklist

USER_ACCESS_TYPE = [USER_ACCESS_TYPE_WHITELIST, USER_ACCESS_TYPE_BLACKLIST]

USER_ACCESS_TYPE_MAP = {USER_ACCESS_TYPE_WHITELIST: True, USER_ACCESS_TYPE_BLACKLIST: False}


USER_ACCESS_STATUS_PERMANENT  = True  #Permanent
USER_ACCESS_STATUS_TEMPORARY  = False #Temporary

USER_ACCESS_STATUS = [USER_ACCESS_STATUS_PERMANENT, USER_ACCESS_STATUS_TEMPORARY]

USER_ACCESS_STATUS_MAP = {USER_ACCESS_STATUS_PERMANENT: True, USER_ACCESS_STATUS_TEMPORARY: False}

# Redis Keys

RK_RULE_BASE = "H:sid"

RK_USER_ACCESS_BASE = "H:usraction"

RK_IP_ACTION_BASE = "H:ipaction"

RK_RULE_PAGE_PER_MINUTE_EXCEEDS  =   "pmin"
RK_RULE_PAGE_PER_SESSION_EXCEEDS =   "psess"
RK_RULE_SESSION_LENGTH_EXCEEDS   =   "sesslen"

RK_RULE_BROWSER_INTGRITY        = "r1"
RK_RULE_LIMITING_CHECK_FAILED   = "r2"
RK_RULE_HTTP_REQUEST_INTEGRITY  = "r3"
RK_RULE_AGGREGATOR              = "r4"
RK_RULE_BEHAVIOUR_INTEGRITY     = "r5"

RK_BLACK_LIST = "S:BIP"
RK_WHITE_LIST = "S:WIP"

RK_HEALTH_CHECK_BASE = "HEALTH_CHECK:ADMIN"
RK_HEALTH_CHECK_KEY  = "REDIS"

RK_USER_ACCESS      = 'usracc'
RK_USER_ANALYSIS    = 'usranalys'
RK_IP_ACCESS        = 'ipacc'
RK_IP_ANALYSIS      = 'ipanalys'
RK_VERIFY           = 'L:verify'

RK_SID_MAP          = 'H:sidmap'
RK_SID_MIN_MAP      = 'H:sidminmap'
RK_VERIFY_INT       = 'vint'
