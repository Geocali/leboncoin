import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
from lxml import etree
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
import os


#from ad_class import ad_class

def get_pictures_lvl2(driver, url_ad):
    driver.get(url_ad)
    #print(url_ad)
    # only if there is more than 1 image
    urls_img = []
    ok = True
    i = 1
    while(ok):
        try:
            xpath = "/html/body/section[1]/main/section/section/section/section/section[1]/div/ul/li[" + str(i) + "]/span/img"
            elem = driver.find_element_by_xpath(xpath)
            url_img = elem.get_attribute("src")
            urls_img.append(url_img)
            i = i + 1
        except:
            ok = False
    # if there is only one image in the ad
    try:
        if len(urls_img) == 0:
            xpath = "/html/body/section[1]/main/section/section/section/section/div/span/img"
            elem = driver.find_element_by_xpath(xpath)
            url_img = elem.get_attribute("src")
            urls_img.append(url_img)
    except:
        # if there is 0 image
        pass
    return urls_img

def get_infos_lvl2(driver, url_ad):
    htmlparser = etree.HTMLParser()
    if('http' not in url_ad):
        tree_ad = etree.parse(url_ad, htmlparser)
    else:
        page_ad = urlopen(url_ad)
        tree_ad = etree.parse(page_ad, htmlparser)

    # we get the description
    # if there is only one image, there is only one section
    try:
        xpath_desc = "/html/body/section[1]/main/section/section/section/section/section[2]/div[6]/p[2]"
        desc_elmt = tree_ad.xpath(xpath_desc)
        text_iterator = desc_elmt[0].itertext()
        desc = ""
        for txt in text_iterator:
            desc = desc + " " + txt
    except:
        xpath_desc = "/html/body/section[1]/main/section/section/section/section/section/div[6]/p[2]"
        desc_elmt = tree_ad.xpath(xpath_desc)
        text_iterator = desc_elmt[0].itertext()
        desc = ""
        for txt in text_iterator:
            desc = desc + " " + txt

    # to get the images :
    # they are protected : a javascript code creates the link, so we have no direct access to the urls
    # we have to use selenium
    urls_img = get_pictures_lvl2(driver, url_ad)

    return desc, urls_img

def process_nb(ah):
    # we remove the separators of thousands
    part = ah.split(".")
    if ('0' in part[-1] and len(part[-1]) == 3):
        ah = ah.replace(".", "")
    part = ah.split(",")
    if ('0' in part[-1] and len(part[-1]) == 3):
        ah = ah.replace(",", "")

    # we replace the separator of decimals
    ah = ah.replace(",", ".")
    return ah

def return_ah_from_str(string):
    pattern = re.compile(r'([0-9.,]*\Smah)', re.IGNORECASE)
    if (pattern.search(string) != None):
        ah = pattern.search(string).groups()[0][:-3]
        ah = process_nb(ah)
        try:
            ah = float(ah) / 1000
        except:
            ah = None
        return ah
    pattern = re.compile(r'([0-9.,]* mah)', re.IGNORECASE)
    if (pattern.search(string) != None):
        ah = pattern.search(string).groups()[0][:-4]
        ah = process_nb(ah)
        try:
            ah = float(ah) / 1000
        except:
            ah = None
        return ah
    pattern = re.compile(r'([0-9.,]*\Sah)', re.IGNORECASE)
    if (pattern.search(string) != None):
        ah = pattern.search(string).groups()[0][:-2]
        ah = process_nb(ah)
        try:
            ah = float(ah)
        except:
            ah = None
        return ah
    pattern = re.compile(r'([0-9.,]* ah)', re.IGNORECASE)
    # iop = open("iop.txt", 'w')
    # iop.write(pattern.search(string))
    # iop.close()
    if (pattern.search(string) != None):
        ah = pattern.search(string).groups()[0][:-3]
        ah = process_nb(ah)
        try:
            ah = float(ah)
        except:
            ah = None
        return ah

def return_ah_from_img(url_img):
    return None

def get_infos_lvl1(tree_ads, i, lvl2):
    ad_glob = tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a")
    ad_url = "http:" + ad_glob[0].values()[0]

    ad_title = ad_glob[0].values()[1]

    # we try to find the capacity of the battery
    ah = return_ah_from_str(ad_title)
    desc = None

    ad_img = tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/div[1]/span[1]/span[1]")
    try:
        url_img_ad = "http:" + ad_img[0].values()[2]
    except:
        url_img_ad = None

    if (ah == None):
        # we try to find the capacity of the battery from this image
        if (url_img_ad != None):
            ah = return_ah_from_img(url_img_ad)

        if (ah == None and lvl2 == True):
            # we try to find the capacity in the detailed description of the ad
            # !!!!!!!!!!! to do
            desc, urls_img = get_infos_lvl2(driver, ad_url)
            ah = return_ah_from_str(desc)
            if (ah == None):
                # we try to find the capacity in the images of the detailed description
                # !!!!!!!!!!! to do
                ah = None

    ad_city_elmt = tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/section/p[2]")
    ad_city = ad_city_elmt[0].getchildren()[0].values()[1]

    ad_price_elmt = tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/section/h3")
    ad_price = int(ad_price_elmt[0].values()[2])

    ad_time_elmt = tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/section/aside/p")
    ad_time = ad_time_elmt[0].values()[2]

    results = pd.DataFrame([ad_title, ah, ad_price, ad_url, ad_time, ad_city, url_img_ad, desc], index=['title', 'ah', 'price', 'url', 'time', 'city', 'url_img', 'desc']).transpose()

    return results



class page_class:
    def __init__(self, url_request):
        htmlparser = etree.HTMLParser()
        page_ads = urlopen(url_request)
        self.tree_ads = etree.parse(page_ads, htmlparser)
    def get_infos_ad(self, driver_in, i):
        global driver
        driver = driver_in
        return get_infos_lvl1(self.tree_ads, i, True)

class Test_infos_lvl1(unittest.TestCase):
    #def setUp(self):
    @classmethod
    def setUpClass(self):
        file_html = open("ads_page.htm", 'r')
        self.prices = [100, 10, 40, 10, 20, 10, 10, 20, 15, 20, 15, 40, 35, 7, 10, 10, 50, 40]
        self.times = ['2017-04-22', '2017-04-22', '2017-04-21', '2017-04-16', '2017-04-16', '2017-04-15', '2017-04-05', '2017-04-03', '2017-04-03', '2017-03-21', '2017-03-19', '2017-03-13', '2017-03-13', '2017-03-08', '2017-03-06', '2017-03-06', '2017-02-28', '2017-02-22']

        string_html = file_html.read().encode('utf8').decode('utf8')
        file_html.close()
        htmlparser = etree.HTMLParser()
        tree_ads = etree.parse("ads_page.htm", htmlparser)

        batteries = []
        ok = True
        i = 1
        while (ok == True):
            try:
                battery = get_infos_lvl1(tree_ads, i, False)
                ls_batt = pd.DataFrame(battery, index=["title", "capacity", "price", "url", "time", "city", "url_img", 'desc']).transpose()
                batteries.append(ls_batt)
                i = i + 1
            except:
                ok = False
        self.df = pd.concat(batteries)

    def test_prices(self):
        prices_found = self.df['price'].tolist()
        self.assertEqual(prices_found, self.prices)

    def test_times(self):
        times_found = self.df['time'].tolist()
        self.assertEqual(times_found, self.times)

class Test_infos_lvl2_page1(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #self.driver = webdriver.Firefox()
        path = os.path.realpath(__file__)
        path = path.split("\\")[:-1]
        path.append("ad_detailed_page.htm")
        self.path = path
        url_ad = "file:///" + "/".join(path)
        self.desc, self.urls_img = get_infos_lvl2(driver, url_ad)

    def test_ah(self):
        ah = return_ah_from_str(self.desc)
        self.assertEqual(6, ah)

    def test_img(self):
        url = "file:///" + "/".join(self.path[:-1]) + "/ad_detailed_page_fichiers/6c4e2409c4722404ca97885b131afa1219ee3fbe.jpeg"
        self.assertEqual(self.urls_img, [url])


class Test_infos_lvl2_page2(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #self.driver = webdriver.Firefox()
        path = os.path.realpath(__file__)
        path = path.split("\\")[:-1]
        path.append("ad_detailed_page2.htm")
        self.path = path
        url_ad = "file:///" + "/".join(path)
        self.desc, self.urls_img = get_infos_lvl2(driver, url_ad)

    def test_ah(self):
        ah = return_ah_from_str(self.desc)
        self.assertEqual(4.4, ah)

    def test_img(self):
        url = ['file:///ad-thumb/bea522a8c094fc7e70b3db2b37bc6c212024ccef.jpg', 'file:///ad-thumb/bcf9377259612bf7f7c11220d7c92248221315e5.jpg', 'file:///ad-thumb/10416909729efe9c983aeaf1e9b6b7704bbb0b83.jpg']
        #print(self.urls_img)
        self.assertEqual(self.urls_img, url)

    @classmethod
    def tearDownClass(self):
        driver.close()
        driver.quit()


if __name__ == "__main__":
    global driver
    driver = webdriver.Firefox()
    unittest.main()
