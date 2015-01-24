from datetime import timedelta
import datetime
from random import randint
import random

from django.db.utils import IntegrityError

from ip_analysis.models import Subscriber
from persistance.user_analysis import UserAnalysis, UserIpDetails


def user_ip_details_table_dummy_data():

    ips_list = []
    for _ in range(3000):
        x = "{}:{}:{}:{}".format(randint(1,255), randint(1,255), randint(1,255), randint(1,255))
        ips_list.append(x)

    country_names = ['India', 'United States', 'United Kingdom', 'Russia', 'China', 'Japan']

    city_name   =   ['Kolkatta', 'New York', 'Vladivostok', 'London', 'Beijing', 'Tokyo']

    isp = ['Google', 'Yahoo', 'Bing', 'Tata Communications', 'Reliance Communications', 'Microsoft']

    for ip in ips_list:
        UserIpDetails.objects.create(ip_address     = ip,
                                     country_name   = random.choice(country_names),
                                     city_name      = random.choice(city_name),
                                     isp            = random.choice(isp),
                                     domain         = 'None')

def user_analysis_table_dummy_data():
    user_id =   ['User123', 'User456', 'User789', 'User000']

    dt = [datetime.datetime.today()]
    temp = datetime.datetime.today()
    for _ in range(180):
        dat = temp - timedelta(days = 1)
        dt.append(dat)
        temp = dat

    try:
        for _ in range(20000):
            UserAnalysis.objects.create(sid             = random.choice(Subscriber.objects.filter(internal_sid__in = [4,7,18,33,25])),
                                        user_id         = random.choice(user_id),
                                        dt              = random.choice(dt),
                                        ip_address      = random.choice(UserIpDetails.objects.all()),
                                        total_requests  = randint(1,1000))

    except IntegrityError:
        pass