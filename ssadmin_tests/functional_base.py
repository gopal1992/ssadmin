# -*- coding: utf-8 -*-
import time

from django.test.testcases import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from inital_setup import create_groups
from ssadmin_tests.factories import SubscriberFactory, IpDetailsFactory, \
     IpAddressAccessListFactory, UserFactory, UserSubscriberFactory

# class BaseLogin(object):



class FunctionalBase(TestCase):

    def create_user_and_groups(self):
        create_groups()
        SubscriberFactory()
        IpDetailsFactory()
        IpAddressAccessListFactory()
        UserFactory()
        UserSubscriberFactory()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.create_user_and_groups()

    def tearDown(self):
        self.browser.quit()

    def test_super_admin_user_case(self):
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('s@s.ss')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)
        self.browser.find_element_by_link_text('View Reports').click()

        select = Select(self.browser.find_element_by_id('id_subscriber'))
        select.select_by_visible_text('<Subscriber: India Property>')

        select = Select(self.browser.find_element_by_id('id_reports'))
        select.select_by_visible_text('IP Access List')

        self.browser.find_element_by_class_name('btn-primary').click()
        time.sleep(5)


        ############### Input Form functional test ###############


        ############### IP Address search results ###############

        # USE CASE (1.a) - When No IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = ''
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)

        # USE CASE (1.b.i) - When Improper IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.a.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.1.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '65.57.245.11'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[0].text == 'No data available.' or tds[0].text == '65.57.245.11'):
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            self.fail('Wrong data is returned for ip search result')


        ############### Location search results ###############

        # USE CASE (2.a) - When No Location given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = ''
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)

        # USE CASE (2.b.i) - When Location is NOT AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'blah'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Location is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (2.b.ii) - When Location is AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'UNITED STATES'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[1].text == 'UNITED STATES'):
                    self.fail('wrong location is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)

        ############### ISP results ###############

        # USE CASE (3.a) - When No ISP given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = ''
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)

        # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'blah'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'LEVEL 3 COMMUNICATIONS INC.'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[2].text == 'LEVEL 3 COMMUNICATIONS INC.'):
                    self.fail('wrong ISP is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)



        ############### Organization search results ###############

        # USE CASE (4.a) - When No Organization given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = ''
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        # USE CASE (4.b.i) - When an Organization is NOT AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'blah'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Organization is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (4.b.ii) - When an Organization is AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'MICROSOFT'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[3].text == input_value):
                    self.fail('wrong Organization is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        ############### Access Status search results ###############

        # USE CASE (5.a) - When No Access Status given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value =   ''
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)

        # USE CASE (5.b.i) - When Access Status is NOT AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value =   'Deny'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        # USE CASE (5.b.ii) - When Access Status is AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Allow'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)





    def test_monitor_mode_demo_user_use_case(self):
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('demo1@shieldsquare.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('demo1')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)
        self.browser.find_element_by_link_text('IP Access List').click()

        ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
        if ip_address.is_enabled():
            self.fail('IP input box is enabled for the Monitor mode-Demo user')

        self.browser.find_element_by_class_name('whitelist').click()
        time.sleep(2)
        self.assertEqual(self.browser.find_element_by_class_name('demo-user-info-text').text, "You are in monitor mode.", "Blacklisting IP test - failure" )
        self.browser.find_element_by_id('id_demo_account_info_message').click()
        time.sleep(5)

        self.browser.find_element_by_class_name('blacklist').click()
        time.sleep(2)
        self.assertEqual(self.browser.find_element_by_class_name('demo-user-info-text').text, "You are in monitor mode.", "Blacklisting IP test - failure" )
        self.browser.find_element_by_id('id_demo_account_info_message').click()
        time.sleep(5)

        ############### Input Form functional test ###############


        ############### IP Address search results ###############

        # USE CASE (1.a) - When No IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = ''
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)

        # USE CASE (1.b.i) - When Improper IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.a.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value =   '1.1.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value =   '195.154.185.238'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[0].text == 'No data available.' or tds[0].text == input_value):
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            self.fail('Wrong data is returned for ip search result')


        ############### Location search results ###############

        # USE CASE (2.a) - When No Location given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value =   ''
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)

        # USE CASE (2.b.i) - When Location is NOT AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value =   'blah'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Location is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (2.b.ii) - When Location is AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'FRANCE'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[1].text == input_value):
                    self.fail('wrong location is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)

        ############### ISP results ###############

        # USE CASE (3.a) - When No ISP given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value =   ''
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)

        # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'blah'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value =   'ONLINE S.A.S.'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[2].text == input_value):
                    self.fail('wrong ISP is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)



        ############### Organization search results ###############

        # USE CASE (4.a) - When No Organization given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = ''
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        # USE CASE (4.b.i) - When an Organization is NOT AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'blah'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Organization is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (4.b.ii) - When an Organization is AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'MICROSOFT'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[3].text == input_value):
                    self.fail('wrong Organization is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        ############### Access Status search results ###############

        # USE CASE (5.a) - When No Access Status given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = ''
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)

        # USE CASE (5.b.i) - When Access Status is NOT AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value =   'Deny'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        # USE CASE (5.b.ii) - When Access Status is AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Allow'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


    def test_active_mode_demo_user_use_case(self):
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('demo2@shieldsquare.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('demo2')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)
        self.browser.find_element_by_link_text('IP Access List').click()

        ip_address_search  =   self.browser.find_element_by_id('id_ip_address_add')
        ip_address_search.clear()
        input_value =   '195.154.185.238'
        ip_address_search.send_keys(input_value)
        self.browser.find_element_by_class_name('whitelist').click()
        time.sleep(2)
        self.assertEqual(self.browser.find_element_by_class_name('demo-user-info-text').text, "You are using a demo account. All the write operations are either disabled or not saved.", "Blacklisting IP test - failure" )
        self.browser.find_element_by_id('id_demo_account_info_message').click()
        time.sleep(5)

        # USE CASE (2.b.ii) - When Proper IP that is AVAILABLE in the database given as input and clicked on blacklist button
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address_add')
        ip_address_search.clear()
        input_value =   '199.21.99.123'
        ip_address_search.send_keys(input_value)
        self.browser.find_element_by_class_name('blacklist').click()
        time.sleep(2)
        self.assertEqual(self.browser.find_element_by_class_name('demo-user-info-text').text, "You are using a demo account. All the write operations are either disabled or not saved.", "Blacklisting IP test - failure" )
        self.browser.find_element_by_id('id_demo_account_info_message').click()
        time.sleep(5)

        ############### Input Form functional test ###############


        ############### IP Address search results ###############

        # USE CASE (1.a) - When No IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = ''
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)

        # USE CASE (1.b.i) - When Improper IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.a.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value =   '1.1.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value =   '195.154.185.238'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[0].text == 'No data available.' or tds[0].text == input_value):
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            self.fail('Wrong data is returned for ip search result')


        ############### Location search results ###############

        # USE CASE (2.a) - When No Location given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value =   ''
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)

        # USE CASE (2.b.i) - When Location is NOT AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value =   'blah'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Location is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (2.b.ii) - When Location is AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'FRANCE'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[1].text == input_value):
                    self.fail('wrong location is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)

        ############### ISP results ###############

        # USE CASE (3.a) - When No ISP given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value =   ''
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)

        # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'blah'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value =   'ONLINE S.A.S.'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[2].text == input_value):
                    self.fail('wrong ISP is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)



        ############### Organization search results ###############

        # USE CASE (4.a) - When No Organization given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = ''
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        # USE CASE (4.b.i) - When an Organization is NOT AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'blah'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Organization is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (4.b.ii) - When an Organization is AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'MICROSOFT'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[3].text == input_value):
                    self.fail('wrong Organization is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        ############### Access Status search results ###############

        # USE CASE (5.a) - When No Access Status given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = ''
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)

        # USE CASE (5.b.i) - When Access Status is NOT AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value =   'Deny'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        # USE CASE (5.b.ii) - When Access Status is AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Allow'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)





    def test_user_use_case(self):
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('nithya@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)
        self.browser.find_element_by_link_text('IP Access List').click()

        ############### Input Form functional test ###############


        ############### IP Address search results ###############

        # USE CASE (1.a) - When No IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = ''
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)

        # USE CASE (1.b.i) - When Improper IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.a.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.1.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '65.57.245.11'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[0].text == 'No data available.' or tds[0].text == '65.57.245.11'):
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            self.fail('Wrong data is returned for ip search result')


        ############### Location search results ###############

        # USE CASE (2.a) - When No Location given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = ''
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)

        # USE CASE (2.b.i) - When Location is NOT AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'blah'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Location is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (2.b.ii) - When Location is AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'UNITED STATES'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[1].text == 'UNITED STATES'):
                    self.fail('wrong location is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)

        ############### ISP results ###############

        # USE CASE (3.a) - When No ISP given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = ''
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)

        # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'blah'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'LEVEL 3 COMMUNICATIONS INC.'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[2].text == 'LEVEL 3 COMMUNICATIONS INC.'):
                    self.fail('wrong ISP is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)



        ############### Organization search results ###############

        # USE CASE (4.a) - When No Organization given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = ''
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        # USE CASE (4.b.i) - When an Organization is NOT AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'blah'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Organization is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (4.b.ii) - When an Organization is AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'MICROSOFT'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[3].text == input_value):
                    self.fail('wrong Organization is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        ############### Access Status search results ###############

        # USE CASE (5.a) - When No Access Status given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value =   ''
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)

        # USE CASE (5.b.i) - When Access Status is NOT AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value =   'Deny'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


        # USE CASE (5.b.ii) - When Access Status is AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Allow'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if tds[0].text == 'No data available.':
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        else:
            for i in range(1, len(trs)):
                tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
                if not (tds[4].text == input_value):
                    self.fail('wrong Access Status is returned')
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)


    def test_monitor_mode_admin_use_case(self):
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('ganesh@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('Ganesh')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)
        self.browser.find_element_by_link_text('IP Access List').click()

        ############### Listing IP functional tests ###############

        ############### Whitelisting tests #################
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[0].find_elements(By.TAG_NAME, 'td')

        if (tds[0].text == 'No data available.'):

            # USE CASE (1.a) - Page loads initially, "No data available." to be dsiplayed
            # self.assertEqual(tds[0].text, 'No data available.', "Initially when the page doesn't have data, 'No data available.' message is not displayed")

            ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
            if ip_address.is_enabled():
                self.fail('Input box is enabled for the Monitor mode-Admin')

        ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
        if ip_address.is_enabled():
            self.fail('Input box is enabled for the Monitor mode-Admin')

        ############### Input Form functional test ###############


        ############### IP Address search results ###############

        # USE CASE (1.a) - When No IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = ''
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.1.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '65.57.245.11'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        if (tds[0].text == '65.57.245.11'):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')

        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)


        ############### Location search results ###############

        # USE CASE (2.a) - When No Location given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = ''
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)

        # USE CASE (2.b.i) - When Location is NOT AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'blah'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Location is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (2.b.ii) - When Location is AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'UNITED STATES'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[1].text == input_value):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')

        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)


        ############### ISP results ###############

        # USE CASE (3.a) - When No ISP given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = ''
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)

        # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'blah'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'LEVEL 3 COMMUNICATIONS INC.'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[2].text == input_value):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')

        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)



        ############### Organization search results ###############

        # USE CASE (4.a) - When No Organization given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = ''
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[0].find_elements(By.TAG_NAME, 'td')

        if (tds[3].text == input_value):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')

        # USE CASE (4.b.i) - When an Organization is NOT AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'blah'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Organization is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (4.b.ii) - When an Organization is AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'MICROSOFT'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[0].text == 'No data available.'):
            self.browser.find_element_by_link_text('Go Back').click()
            time.sleep(2)
        elif (tds[3].text == input_value):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')


        ############### Access Status search results ###############

        # USE CASE (5.a) - When No Access Status given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = ''
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)

        # USE CASE (5.b.i) - When Access Status is NOT AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Deny'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[4].text == input_value):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')

        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (5.b.ii) - When Access Status is AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Allow'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')

        if (tds[4].text == input_value):
            tds[5].find_element_by_tag_name('i').click()
            time.sleep(5)
            self.assertFalse(self.browser.find_elements_by_class_name('modal-footer'), 'Monitor mode-Admin able to remove the IP from listing')

        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)


    def test_base_class_login(self):
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('jagadesh@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)
        self.browser.find_element_by_link_text('IP Access List').click()



        ############### Listing IP functional tests ###############

        ############### Whitelisting tests #################
        table       =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')

        for tr in trs:
            tds =   tr.find_elements(By.TAG_NAME, 'td')

            if (tds[0].text == 'No data available.'):

                # USE CASE (1.a) - Page loads initially, "No data available." to be dsiplayed
                self.assertEqual(tds[0].text, 'No data available.', "Initially when the page doesn't have data, 'No data available.' message is not displayed")

                # USE CASE (1.a) - When there is no input given and clicked on whitelist button
                ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address.clear()
                input_value = ''
                ip_address.send_keys(input_value)
                self.browser.find_element_by_class_name('whitelist').click()
                time.sleep(10)
                self.assertEqual(self.browser.find_element_by_id('id_validation_message_panel').text, "This field is required.", "No IP test - failure")

                # USE CASE (1.b.i) - When an imporper input given and clicked on whitelist button
                ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address.clear()
                input_value = '1.a.1.1'
                ip_address.send_keys(input_value)
                self.browser.find_element_by_class_name('whitelist').click()
                time.sleep(10)
                self.assertEqual(self.browser.find_element_by_id('id_validation_message_panel').text, "Enter a valid IPv4 address.", "Improper IP test - failure")

                # USE CASE (1.b.ii) - When Proper IP but NOT AVAILABLE in the database is given as input and clicked on whitelist button
                ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address.clear()
                input_value = '1.1.1.1'
                ip_address.send_keys(input_value)
                self.browser.find_element_by_class_name('whitelist').click()
                #self.assertEqual(self.browser.find_element_by_id('id_validation_message_panel'), "This field is required.", "No IP is given is failure")

                # USE CASE (1.b.ii) - When Proper IP that is AVAILABLE in the database given as input and clicked on whitelist button
                ip_address_search  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address_search.clear()
                input_value = '94.23.202.191'
                ip_address_search.send_keys(input_value)
                self.browser.find_element_by_class_name('whitelist').click()
                time.sleep(20)
                self.assertEqual(self.browser.find_element_by_id('id_alert_success_message').text, "Successfully added the IP Address '94.23.202.191' to whitelist.", "Whitelisting IP test - failure" )
                self.browser.find_element_by_id('id_alert_success').click()
                time.sleep(5)


                table   =   self.browser.find_element_by_class_name('table-hover')
                table_body  =   table.find_element_by_tag_name('tbody')
                trs     =   table_body.find_elements(By.TAG_NAME, 'tr')
                for tr in trs:
                    tds =   tr.find_elements(By.TAG_NAME, 'td')

                    #Check for the whitelisted IP is available in the same page and to remove it from the whitelisting
                    if (tds[4].text == 'Allow' and tds[0].text == '94.23.202.191'):

                        # USE CASE (1.b.ii.1) - Click on the 'X' symbol to close the modal popup
                        tds[5].find_element_by_tag_name('i').click()
                        time.sleep(5)
                        modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                        self.browser.find_element_by_class_name('bootbox-close-button').click()
                        time.sleep(10)

                        # USE CASE (1.b.ii.2) - Click on the CANCEL button to exit the modal popup
                        tds[5].find_element_by_tag_name('i').click()
                        time.sleep(5)
                        modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                        modal_popup.find_element_by_class_name('btn-default').click()
                        time.sleep(10)

                        # USE CASE (1.b.ii.3) - Click on the OK button to remove the IP from whitelist
                        tds[5].find_element_by_tag_name('i').click()
                        time.sleep(5)
                        modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                        modal_popup.find_element_by_class_name('btn-primary').click()
                        time.sleep(20)
                        self.assertEqual(self.browser.find_element_by_id('id_alert_success_message').text, "Successfully deleted the IP Address '94.23.202.191' from Whitelist", "Remove from whitelist test 1-failure")
                        self.browser.find_element_by_id('id_alert_success').click()
                        time.sleep(5)

                    else:
                        pass

#             # Check whether the IP removed from whitelist is available in the IP Access list
#             if tds[0].text == '94.23.202.191':
#                 self.assertTrue(tds[0].text == '94.23.202.191', "IP removed from whitelist still exists")

            elif (tds[4].text == 'Allow' and tds[0].text == '94.23.202.191'):

                # USE CASE (1.b.ii.1) - Click on the 'X' symbol to close the modal popup
                tds[5].find_element_by_tag_name('i').click()
                time.sleep(5)
                modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                self.browser.find_element_by_class_name('bootbox-close-button').click()
                time.sleep(10)

                # USE CASE (1.b.ii.2) - Click on the CANCEL button to exit the modal popup
                tds[5].find_element_by_tag_name('i').click()
                time.sleep(5)
                modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                modal_popup.find_element_by_class_name('btn-default').click()
                time.sleep(10)

                # USE CASE (1.b.ii.3) - Click on the OK button to remove the IP from whitelist
                tds[5].find_element_by_tag_name('i').click()
                time.sleep(5)
                modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                modal_popup.find_element_by_class_name('btn-primary').click()
                time.sleep(20)
                self.assertEqual(self.browser.find_element_by_id('id_alert_success_message').text, "Successfully deleted the IP Address '94.23.202.191' from Whitelist", "Remove from whitelist test 1-failure")
                self.browser.find_element_by_id('id_alert_success').click()
                time.sleep(5)

#                 # Check whether the IP removed from whitelist is available in the IP Access list
#                 if tds[0].text == '94.23.202.191':
#                     self.assertTrue(tds[0].text == '94.23.202.191', "IP removed from whitelist still exists")

            else:
                pass


        ############### Blacklisting tests #################
        table   =   self.browser.find_element_by_class_name('table-hover')
        table_body  =   table.find_element_by_tag_name('tbody')
        trs     =   table_body.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            tds =   tr.find_elements(By.TAG_NAME, 'td')

            # USE CASE (1.a) - Page loads initially, "No data available." to be dsiplayed
            self.assertEqual(tds[0].text, 'No data available.', "Initially when the page doesn't have data, 'No data available.' message is not displayed")

            if (tds[0].text == 'No data available.'):

                # USE CASE (2.a) - When there is no input given and clicked on blacklist button
                ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address.clear()
                input_value = ''
                ip_address.send_keys(input_value)
                self.browser.find_element_by_class_name('blacklist').click()
                time.sleep(10)
                self.assertEqual(self.browser.find_element_by_id('id_validation_message_panel').text, "This field is required.", "No IP test - failure")

                # USE CASE (2.b.i) - When an imporper input given and clicked on blacklist button
                ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address.clear()
                input_value = '1.a.1.1'
                ip_address.send_keys(input_value)
                self.browser.find_element_by_class_name('blacklist').click()
                time.sleep(10)
                self.assertEqual(self.browser.find_element_by_id('id_validation_message_panel').text, "Enter a valid IPv4 address.", "Improper IP test - failure")

                # USE CASE (2.b.ii) - When Proper IP but NOT AVAILABLE in the database is given as input and clicked on blacklist button
                ip_address  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address.clear()
                input_value = '1.1.1.1'
                ip_address.send_keys(input_value)
                self.browser.find_element_by_class_name('blacklist').click()
                #self.assertEqual(self.browser.find_element_by_id('id_validation_message_panel'), "This field is required.", "No IP is given is failure")

                # USE CASE (2.b.ii) - When Proper IP that is AVAILABLE in the database given as input and clicked on blacklist button
                ip_address_search  =   self.browser.find_element_by_id('id_ip_address_add')
                ip_address_search.clear()
                input_value = '94.23.245.151'
                ip_address_search.send_keys(input_value)
                self.browser.find_element_by_class_name('blacklist').click()
                time.sleep(20)
                self.assertEqual(self.browser.find_element_by_id('id_alert_success_message').text, "Successfully added the IP Address '94.23.245.151' to blacklist.", "Blacklisting IP test - failure" )
                self.browser.find_element_by_id('id_alert_success').click()
                time.sleep(5)


                table   =   self.browser.find_element_by_class_name('table-hover')
                table_body  =   table.find_element_by_tag_name('tbody')
                trs     =   table_body.find_elements(By.TAG_NAME, 'tr')
                for tr in trs:
                    tds =   tr.find_elements(By.TAG_NAME, 'td')

                    #Check for the blacklisted IP is available in the same page and to remove it from the blacklisting
                    if (tds[4].text == 'Deny' and tds[0].text == '94.23.245.151'):

                        # USE CASE (2.b.ii.1) - Click on the 'X' symbol to close the modal popup
                        tds[5].find_element_by_tag_name('i').click()
                        time.sleep(5)
                        modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                        self.browser.find_element_by_class_name('bootbox-close-button').click()
                        time.sleep(10)

                        # USE CASE (2.b.ii.2) - Click on the CANCEL button to exit the modal popup
                        tds[5].find_element_by_tag_name('i').click()
                        time.sleep(5)
                        modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                        modal_popup.find_element_by_class_name('btn-default').click()
                        time.sleep(10)

                        # USE CASE (2.b.ii.3) - Click on the OK button to remove the IP from blacklist
                        tds[5].find_element_by_tag_name('i').click()
                        time.sleep(5)
                        modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                        modal_popup.find_element_by_class_name('btn-primary').click()
                        time.sleep(20)
                        self.assertEqual(self.browser.find_element_by_id('id_alert_success_message').text, "Successfully deleted the IP Address '94.23.245.151' from Blacklist", "Remove from blacklist test 1-failure")
                        self.browser.find_element_by_id('id_alert_success').click()
                        time.sleep(5)

#                         # Check whether the IP removed from blacklist is available in the IP Access list
#                         self.assertTrue(any(tds[0].text == '94.23.245.151'), "IP removed from blacklist still exists")

            elif (tds[4].text == 'Deny' and tds[0].text == '94.23.245.151'):

                # USE CASE (2.b.ii.1) - Click on the 'X' symbol to close the modal popup
                tds[5].find_element_by_tag_name('i').click()
                time.sleep(5)
                modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                self.browser.find_element_by_class_name('bootbox-close-button').click()
                time.sleep(10)

                # USE CASE (2.b.ii.2) - Click on the CANCEL button to exit the modal popup
                tds[5].find_element_by_tag_name('i').click()
                time.sleep(5)
                modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                modal_popup.find_element_by_class_name('btn-default').click()
                time.sleep(10)

                # USE CASE (2.b.ii.3) - Click on the OK button to remove the IP from blacklist
                tds[5].find_element_by_tag_name('i').click()
                time.sleep(5)
                modal_popup  = self.browser.find_element_by_class_name('modal-footer')
                modal_popup.find_element_by_class_name('btn-primary').click()
                time.sleep(20)
                self.assertEqual(self.browser.find_element_by_id('id_alert_success_message').text, "Successfully deleted the IP Address '94.23.245.151' from Blacklist", "Remove from blacklist test 1-failure")
                self.browser.find_element_by_id('id_alert_success').click()
                time.sleep(5)

#                 # Check whether the IP removed from blacklist is available in the IP Access list
#                 self.assertTrue(any(tds[0].text == '94.23.245.151'), "IP removed from blacklist still exists")

            else:
                pass


        ############### Input Form functional test ###############


        ############### IP Address search results ###############

        # USE CASE (1.a) - When No IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = ''
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)

        # USE CASE (1.b.i) - When Improper IP given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.a.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '1.1.1.1'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
        ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
        ip_address_search.clear()
        input_value = '94.23.202.191'
        ip_address_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_ip_address_search').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)


        ############### Location search results ###############

        # USE CASE (2.a) - When No Location given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = ''
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)

        # USE CASE (2.b.i) - When Location is NOT AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'blah'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Location is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (2.b.ii) - When Location is AVAILABLE in the database given as input and searched
        location_search  =   self.browser.find_element_by_id('id_location')
        location_search.clear()
        input_value = 'FRANCE'
        location_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_location_search').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)


        ############### ISP results ###############

        # USE CASE (3.a) - When No ISP given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = ''
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)

        # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'blah'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
        isp_search  =   self.browser.find_element_by_id('id_isp')
        isp_search.clear()
        input_value = 'OVH SAS'
        isp_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_isp_search').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)



        ############### Organization search results ###############

        # USE CASE (4.a) - When No Organization given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = ''
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)

        # USE CASE (4.b.i) - When an Organization is NOT AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'blah'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        table_body  =   self.browser.find_element_by_tag_name('tbody')
        trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
        tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(tds[0].text, 'No data available.', 'Organization is NOT AVAILABLE in the database case failure')
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (4.b.ii) - When an Organization is AVAILABLE in the database given as input and searched
        organization_search  =   self.browser.find_element_by_id('id_organization')
        organization_search.clear()
        input_value = 'MICROSOFT'
        organization_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_organization_search').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)



        ############### Access Status search results ###############

        # USE CASE (5.a) - When No Access Status given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = ''
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)

        # USE CASE (5.b.i) - When Access Status is NOT AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Deny'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)

        # USE CASE (5.b.ii) - When Access Status is AVAILABLE in the database given as input and searched
        access_status_search  =   self.browser.find_element_by_id('id_access_status')
        access_status_search.clear()
        input_value = 'Access'
        access_status_search.send_keys(input_value)
        time.sleep(2)
        self.browser.find_element_by_id('id_access_status_search').click()
        time.sleep(2)
        self.browser.find_element_by_link_text('Go Back').click()
        time.sleep(2)


class BotResponseListPage(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def active_mode_admin_login(self):
        """
        USE CASE: Active mode admin-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('jagadesh@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def monitor_mode_admin_login(self):
        """
        USE CASE: Monitor mode admin-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('ganesh@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('Ganesh')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def active_mode_user_login(self):
        """
        USE CASE: Active mode user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('jaga@jagadesh.in')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def monitor_mode_user_login(self):
        """
        USE CASE: Monitor mode user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('nithya@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def active_mode_demo_user_login(self):
        """
        USE CASE: Active mode Demo user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('demo2@shieldsquare.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('demo2')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def monitor_mode_demo_user_login(self):
        """
        USE CASE: Monitor mode Demo user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('demo1@shieldsquare.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('demo1')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def active_mode_admin_for_bot_reponse_page_test(self):
        """
        USE CASE: Active mode admin-Bot Reponse List page usage

        The dropdowns and the input boxes are checked whether it is enabled for the active mode admins
        """
        table_data  =   self.browser.find_element_by_id('id_action_browser_integrity')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Browser Integrity Check-Dropdown is disabled for active mode Admin')
        table_data  =   self.browser.find_element_by_id('id_action_http_request_integrity_check_failed')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'HTTP Request Integrity-Dropdown is disabled for active mode Admin')
        table_data  =   self.browser.find_element_by_id('id_action_aggregator_bot_traffic')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Aggregator Bot Traffic-Dropdown is disabled for active mode Admin')
        table_data  =   self.browser.find_element_by_id('id_action_behaviour_integrity')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Behaviour Integrity-Dropdown is disabled for active mode Admin')
        table_data  =   self.browser.find_element_by_id('id_action_pages_per_minute_input')
        self.assertTrue(table_data.find_element_by_tag_name('input').is_enabled(), 'Pages Per Minute-Input box is disabled for active mode Admin')
        table_data  =   self.browser.find_element_by_id('id_action_pages_per_minute')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Pages Per Minute-Dropdown is disabled for active mode Admin')
        time.sleep(2)

    def other_users_and_admin_for_bot_reponse_page_test(self):
        """
        USE CASE: Monitor mode admin, Active mode user, Monitor mode user, Monitor mode Demo user-Bot Reponse List page usage

        The dropdowns and the input boxes are checked whether it is disabled for all the above mentioned users
        """
        table_data  =   self.browser.find_element_by_id('id_action_browser_integrity')
        self.assertFalse(table_data.find_element_by_id('id_action').is_enabled(), 'Browser Integrity Check-Dropdown is enabled for monitor mode Admin or acitve mode user or monitor mode user')
        table_data  =   self.browser.find_element_by_id('id_action_http_request_integrity_check_failed')
        self.assertFalse(table_data.find_element_by_id('id_action').is_enabled(), 'HTTP Request Integrity-Dropdown is enabled for monitor mode Admin or acitve mode user or monitor mode user')
        table_data  =   self.browser.find_element_by_id('id_action_aggregator_bot_traffic')
        self.assertFalse(table_data.find_element_by_id('id_action').is_enabled(), 'Aggregator Bot Traffic-Dropdown is enabled for monitor mode Admin or acitve mode user or monitor mode user')
        table_data  =   self.browser.find_element_by_id('id_action_behaviour_integrity')
        self.assertFalse(table_data.find_element_by_id('id_action').is_enabled(), 'Behaviour Integrity-Dropdown is enabled for monitor mode Admin or acitve mode user or monitor mode user')
        table_data  =   self.browser.find_element_by_id('id_action_pages_per_minute_input')
        self.assertFalse(table_data.find_element_by_tag_name('input').is_enabled(), 'Pages Per Minute-Input box is enabled for monitor mode Admin or acitve mode user or monitor mode user')
        table_data  =   self.browser.find_element_by_id('id_action_pages_per_minute')
        self.assertFalse(table_data.find_element_by_id('id_action').is_enabled(), 'Pages Per Minute-Dropdown is enabled for monitor mode Admin or acitve mode user or monitor mode user')
        time.sleep(2)

    def active_mode_demo_user_for_bot_response_list(self):
        """
        USE CASE: Active mode Demo users-Bot Reponse List page usage

        The dropdowns and the input boxes are checked whether it is enabled for the active mode Demo Users also
        on clicking any of the dropdowns or changing the input value in page per minute-limit will be alerted
        with the message "You are using a demo account. All the write operations are either disabled or not
        saved."
        """
        table_data  =   self.browser.find_element_by_id('id_action_browser_integrity')
        if table_data.find_element_by_tag_name("option").get_attribute('selected'):
            self.assertEqual(table_data.find_element_by_tag_name("option").text, "Show Captcha", 'Default value for demo user is not Show Captcha')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Browser Integrity Check-Dropdown is disabled for active mode Demo User')
        table_data  =   self.browser.find_element_by_id('id_action_http_request_integrity_check_failed')
        if table_data.find_element_by_tag_name("option").get_attribute('selected'):
            self.assertEqual(table_data.find_element_by_tag_name("option").text, "Show Captcha", 'Default value for demo user is not Show Captcha')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'HTTP Request Integrity-Dropdown is disabled for active mode Demo User')
        table_data  =   self.browser.find_element_by_id('id_action_aggregator_bot_traffic')
        if table_data.find_element_by_tag_name("option").get_attribute('selected'):
            self.assertEqual(table_data.find_element_by_tag_name("option").text, "Monitor", 'Default value for demo user is not Monitor')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Aggregator Bot Traffic-Dropdown is disabled for active mode Demo User')
        table_data  =   self.browser.find_element_by_id('id_action_behaviour_integrity')
        if table_data.find_element_by_tag_name("option").get_attribute('selected'):
            self.assertEqual(table_data.find_element_by_tag_name("option").text, "Show Captcha", 'Default value for demo user is not Show Captcha')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Behaviour Integrity-Dropdown is disabled for active mode Demo User')
        table_data  =   self.browser.find_element_by_id('id_action_pages_per_minute_input')
        self.assertTrue(table_data.find_element_by_tag_name('input').is_enabled(), 'Pages Per Minute-Input box is disabled for active mode Admin')
        table_data.find_element_by_tag_name('input').clear()
        table_data.find_element_by_tag_name('input').send_keys(551)
        self.browser.find_element_by_id('id_action_pages_per_minute').click()
        self.assertEqual(self.browser.find_element_by_class_name('demo-user-info-text').text, "You are using a demo account. All the write operations are either disabled or not saved.", "Demo info message error")
        self.browser.find_element_by_id('id_demo_account_info_message').click()
        self.assertEqual(table_data.find_element_by_tag_name('input').get_attribute('value'), "150", "Demo info message error")
        table_data  =   self.browser.find_element_by_id('id_action_pages_per_minute')
        if table_data.find_element_by_tag_name("option").get_attribute('selected'):
            self.assertEqual(table_data.find_element_by_tag_name("option").text, "Show Captcha", 'Default value for demo user is not Show Captcha')
        self.assertTrue(table_data.find_element_by_id('id_action').is_enabled(), 'Pages Per Minute-Dropdown is disabled for active mode Demo User')


    def test_active_mode_admin_bot_response_list(self):
        self.active_mode_admin_login()
        self.browser.find_element_by_link_text('Bot Response List').click()
        self.active_mode_admin_for_bot_reponse_page_test()

    def test_monitor_mode_admin_bot_response_list(self):
        self.monitor_mode_admin_login()
        self.browser.find_element_by_link_text('Bot Response List').click()
        self.other_users_and_admin_for_bot_reponse_page_test()

    def test_active_mode_user_bot_response_list(self):
        self.active_mode_user_login()
        self.browser.find_element_by_link_text('Bot Response List').click()
        self.other_users_and_admin_for_bot_reponse_page_test()

    def test_monitor_mode_user_bot_response_list(self):
        self.monitor_mode_user_login()
        self.browser.find_element_by_link_text('Bot Response List').click()
        self.other_users_and_admin_for_bot_reponse_page_test()

    def test_active_mode_demo_user_bot_response_list(self):
        self.active_mode_demo_user_login()
        self.browser.find_element_by_link_text('Bot Response List').click()
        self.active_mode_demo_user_for_bot_response_list()

    def test_monitor_mode_demo_user_bot_response_list(self):
        self.monitor_mode_demo_user_login()
        self.browser.find_element_by_link_text('Bot Response List').click()
        self.other_users_and_admin_for_bot_reponse_page_test()


class BotIPAnalysisPage(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def active_mode_admin_login(self):
        """
        USE CASE: Active mode admin-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('jagadesh@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def monitor_mode_admin_login(self):
        """
        USE CASE: Monitor mode admin-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('ganesh@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('Ganesh')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def active_mode_user_login(self):
        """
        USE CASE: Active mode user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('jaga@jagadesh.in')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def monitor_mode_user_login(self):
        """
        USE CASE: Monitor mode user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('nithya@pydan.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('s')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def active_mode_demo_user_login(self):
        """
        USE CASE: Active mode Demo user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('demo2@shieldsquare.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('demo2')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)

    def monitor_mode_demo_user_login(self):
        """
        USE CASE: Monitor mode Demo user-Login function
        """
        self.browser.get("http://localhost:8000")
        username = self.browser.find_element_by_id('id_email')
        username.send_keys('demo1@shieldsquare.com')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('demo1')
        login = self.browser.find_element_by_id('id_login')
        login.send_keys(Keys.RETURN)


#     def test_active_mode_admin_bot_ip_analysis(self):
#         self.active_mode_admin_login()
#         self.browser.find_element_by_link_text('IP Analysis').click()
#         table_data = self.browser.find_element_by_id('demo').find_element_by_tag_name('tbody')
#         self.assertEqual(table_data.find_element_by_tag_name('h5').text, "No data available.", 'Wrong message is desplayed')
#
#         ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
#         ip_address_search.clear()
#         input_value = ''
#         ip_address_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_ip_address_search').click()
#         time.sleep(2)
#
#         # USE CASE (1.b.i) - When Improper IP given as input and searched
#         ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
#         ip_address_search.clear()
#         input_value = '1.a.1.1'
#         ip_address_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_ip_address_search').click()
#         time.sleep(2)
#         table_body  =   self.browser.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         self.assertEqual(tds[0].text, 'No data available.', 'Improper IP Address case failure')
#         self.browser.find_element_by_link_text('Go Back').click()
#         time.sleep(2)
#
#         # USE CASE (1.b.ii.1) - When Proper IP but NOT AVAILABLE in the database given as input and searched
#         ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
#         ip_address_search.clear()
#         input_value = '1.1.1.1'
#         ip_address_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_ip_address_search').click()
#         time.sleep(2)
#         table_body  =   self.browser.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         self.assertEqual(tds[0].text, 'No data available.', 'Proper IP but Not Available in database case failure')
#         self.browser.find_element_by_link_text('Go Back').click()
#         time.sleep(2)
#
#         # USE CASE (1.b.ii.2) - When Proper IP that is AVAILABLE in the database given as input and searched
#         ip_address_search  =   self.browser.find_element_by_id('id_ip_address')
#         ip_address_search.clear()
#         input_value = '65.57.245.11'
#         ip_address_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_ip_address_search').click()
#         time.sleep(2)
#         table       =   self.browser.find_element_by_class_name('table-hover')
#         table_body  =   table.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#
#         if (tds[0].text == 'No data available.' or tds[0].text == '65.57.245.11'):
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)
#         else:
#             self.fail('Wrong data is returned for ip search result')
#
#         ############### ISP results ###############
#
#         # USE CASE (3.a) - When No ISP given as input and searched
#         isp_search  =   self.browser.find_element_by_id('id_isp')
#         isp_search.clear()
#         input_value = ''
#         isp_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_isp_search').click()
#         time.sleep(2)
#
#         # USE CASE (3.b.i) - When ISP is NOT AVAILABLE in the database given as input and searched
#         isp_search  =   self.browser.find_element_by_id('id_isp')
#         isp_search.clear()
#         input_value = 'blah'
#         isp_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_isp_search').click()
#         time.sleep(2)
#         table_body  =   self.browser.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         self.assertEqual(tds[0].text, 'No data available.', 'ISP is NOT AVAILABLE in the database case failure')
#         self.browser.find_element_by_link_text('Go Back').click()
#         time.sleep(2)
#
#         # USE CASE (3.b.ii) - When ISP is AVAILABLE in the database given as input and searched
#         isp_search  =   self.browser.find_element_by_id('id_isp')
#         isp_search.clear()
#         input_value = 'LEVEL 3 COMMUNICATIONS INC.'
#         isp_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_isp_search').click()
#         time.sleep(2)
#         table       =   self.browser.find_element_by_class_name('table-hover')
#         table_body  =   table.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         if tds[0].text == 'No data available.':
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)
#         else:
#             for i in range(1, len(trs)):
#                 tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
#                 if not (tds[2].text == 'LEVEL 3 COMMUNICATIONS INC.'):
#                     self.fail('wrong ISP is returned')
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)
#
#         ############### City search results ###############
#
#         # USE CASE (2.a) - When No City given as input and searched
#         city_search  =   self.browser.find_element_by_id('id_city_name')
#         city_search.clear()
#         input_value = ''
#         city_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_city_search').click()
#         time.sleep(2)
#
#         # USE CASE (2.b.i) - When City is NOT AVAILABLE in the database given as input and searched
#         city_search  =   self.browser.find_element_by_id('id_city_name')
#         city_search.clear()
#         input_value = 'blah'
#         city_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_city_search').click()
#         time.sleep(2)
#         table_body  =   self.browser.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         self.assertEqual(tds[0].text, 'No data available.', 'City is NOT AVAILABLE in the database case failure')
#         self.browser.find_element_by_link_text('Go Back').click()
#         time.sleep(2)
#
#         # USE CASE (2.b.ii) - When City is AVAILABLE in the database given as input and searched
#         city_search  =   self.browser.find_element_by_id('id_city_name')
#         city_search.clear()
#         input_value = 'UNITED STATES'
#         city_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_city_search').click()
#         time.sleep(2)
#         table       =   self.browser.find_element_by_class_name('table-hover')
#         table_body  =   table.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         if tds[0].text == 'No data available.':
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)
#         else:
#             for i in range(1, len(trs)):
#                 tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
#                 if not (tds[1].text == 'UNITED STATES'):
#                     self.fail('wrong city is returned')
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)
#
#         ############### Country search results ###############
#
#         # USE CASE (4.a) - When No Country given as input and searched
#         country_search  =   self.browser.find_element_by_id('id_country_name')
#         country_search.clear()
#         input_value = ''
#         country_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_country_search').click()
#         time.sleep(2)
#
#         # USE CASE (4.b.i) - When an Country is NOT AVAILABLE in the database given as input and searched
#         country_search  =   self.browser.find_element_by_id('id_country_name')
#         country_search.clear()
#         input_value = 'blah'
#         country_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_country_search').click()
#         time.sleep(2)
#         table_body  =   self.browser.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         self.assertEqual(tds[0].text, 'No data available.', 'Country is NOT AVAILABLE in the database case failure')
#         self.browser.find_element_by_link_text('Go Back').click()
#         time.sleep(2)
#
#         # USE CASE (4.b.ii) - When an Country is AVAILABLE in the database given as input and searched
#         country_search  =   self.browser.find_element_by_id('id_country_name')
#         country_search.clear()
#         input_value = 'MICROSOFT'
#         country_search.send_keys(input_value)
#         time.sleep(2)
#         self.browser.find_element_by_id('id_country_search').click()
#         time.sleep(2)
#
#         table       =   self.browser.find_element_by_class_name('table-hover')
#         table_body  =   table.find_element_by_tag_name('tbody')
#         trs         =   table_body.find_elements(By.TAG_NAME, 'tr')
#         tds         =   trs[1].find_elements(By.TAG_NAME, 'td')
#         if tds[0].text == 'No data available.':
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)
#         else:
#             for i in range(1, len(trs)):
#                 tds         =   trs[i].find_elements(By.TAG_NAME, 'td')
#                 if not (tds[3].text == input_value):
#                     self.fail('wrong Country is returned')
#             self.browser.find_element_by_link_text('Go Back').click()
#             time.sleep(2)


    def test_date_wise_search(self):
        self.active_mode_admin_login()
        self.browser.find_element_by_id('reportrange').click()
        unordered_list = self.browser.find_element_by_class_name('ranges').find_element_by_tag_name('ul')
        list_elements = unordered_list.find_elements_by_tag_name('li')
        for i in range(len(list_elements)):
            unordered_list.find_elements_by_tag_name('li')[i].click()
            time.sleep(10)
