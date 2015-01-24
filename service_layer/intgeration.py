import json

from django.core.cache import get_cache

from dal.integration import get_integration_details, get_smembers
from utils.app_messages import *


def api_data_verification(ip_address_list, session_details_list, identifier_details_list):
    if not len(ip_address_list) < 5:
        if ip_address_list:
            if not any(ip_address_list) in [None, u'', '']:
                if len(set(ip_address_list)) == 1:
                    ip_address_result = {'ip_address_res' : True, 'ip_address_msg': IP_ADDRESS_MATCHES, 'ip_address': ip_address_list[0]}
                else:
                    ip_address_result = {'ip_address_res' : False, 'ip_address_msg': NO_5_SAME_IP_ADDRESS}
            else:
                ip_address_result = {'ip_address_res' : False, 'ip_address_msg': NO_IP_ADDRESS}

        if session_details_list:
            if not any(session_details_list) in [None, u'', '']:
                if len(set(session_details_list)) < 5:
                    session_details_result = {'session_details_res' : True,}
                else:
                    session_details_result = {'session_details_res' : False, 'session_details_msg': MIN_2_SAME_SESSION_ID}
            else:
                session_details_result = {'session_details_res' : False, 'session_details_msg': NO_SESSION_ID}

        if identifier_details_list:
            if not any(identifier_details_list) in [None, u'', '']:
                if len(set(identifier_details_list)) < 5:
                    identifier_details_result = {'identifier_details_res' : True,}
                else:
                    identifier_details_result = {'identifier_details_res' : False, 'identifier_details_msg': MIN_2_SAME_UZMA}
            else:
                identifier_details_result = {'identifier_details_res' : False, 'identifier_details_msg': NO_UZMA}

        return {'api_data': True,
                'ip_address_result': ip_address_result,
                'session_details_result': session_details_result,
                'identifier_details_result':identifier_details_result}

    return {'api_data': False, 'api_message': NO_API_DATA}

def js_data_verification(js_data_list, user_agent_list):
    if not len(js_data_list) < 5:

        if user_agent_list:

            if not any(user_agent_list) in [None, u'', '']:
                user_agent_result = {'user_agent_res' : True,}
            else:
                user_agent_result = {'user_agent_res' : False, 'user_agent_msg': NO_USER_AGENT}

        return {'js_data': True, 'user_agent_result': user_agent_result}

    return {'js_data': False, 'js_message': NO_JS_DATA}

def listing_the_packets_received(list_of_json_data):
    ip_address_list, session_details_list, identifier_details_list, js_data_list, user_agent_list = [], [], [], [], []

    for packets in list_of_json_data:
        for data in range(len(packets)):

            if packets[data]['Type'] == 'A':
                ip_address_list.append(packets[data]['_zpsbd6'])
                session_details_list.append(packets[data]['_zpsbd5'])
                identifier_details_list.append(packets[data]['__uzma'])
            elif packets[data]['Type'] == 'J':
                js_data_list.append(True)
                user_agent_list.append(packets[data]['s2'])

    return api_data_verification(ip_address_list,
                                 session_details_list,
                                 identifier_details_list),\
           js_data_verification(js_data_list, user_agent_list)

def splitting_the_packets_into_json_data(list_of_packets):
    packet_set_1, packet_set_2, packet_set_3, packet_set_4, packet_set_5, segregated_json_data, json_data_set = [], [], [], [], [], [], []

    for items in list_of_packets:
        json_data_set.append(get_smembers(items))

    # Creating 5 packets of data
    for val, packet in enumerate(json_data_set):
        eval('packet_set_'+str(val+1)).append(packet)

    #Processing the data packets and converting them into json loads into a muliti dimensional list
    for limit in range(5):
        temp = []
        for i in eval('packet_set_'+str(limit+1)):
            for z in range(len(list(i))):
                temp.append(json.loads(list(i)[z]))
            segregated_json_data.append(temp)

    return segregated_json_data

def verifying_integration(subscriber):
    redis = get_cache('default').raw_client
    data  = get_integration_details(subscriber)
    list_of_packets = []

    if len(data) == 5:

        for item in data:
            list_of_packets.append('S:'+str(subscriber.sb_internal_sid)+':'+str(item))

        list_of_json_data = splitting_the_packets_into_json_data(list_of_packets)
        api_message, js_message = listing_the_packets_received(list_of_json_data)
        return True, {'api_message': api_message, 'js_message':js_message}

    elif len(data) == 0:
        return False, NO_DATA

    else:
        return False, NO_5_REQUESTS