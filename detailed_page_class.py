

class detailed_page_class:
    def get_pictures(self, url_ad):
        driver.get(url_ad)

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
                i = i +1
            except:
                ok = False
        # if there is only one image in the ad
        if len(urls_img) == 0:
            xpath = "/html/body/section[1]/main/section/section/section/section/div/span/img"
            elem = driver.find_element_by_xpath(xpath)
            url_img = elem.get_attribute("src")
            urls_img.append(url_img)
        return urls_img

    def get_infos_ad(self):
        # we get the city
        xpath_city = "/html/body/section[1]/main/section/section/section/section/section/div[5]/h2/span[2]"
        city_elmt = self.tree_ad.xpath(xpath_city)
        city = city_elmt[0].text

        # we get the description
        # if there is only one image, there is only one section
        try:
            xpath_desc = "/html/body/section[1]/main/section/section/section/section/section[2]/div[6]/p[2]"
            desc_elmt = self.tree_ad.xpath(xpath_desc)
            text_iterator = desc_elmt[0].itertext()
            desc = ""
            for txt in text_iterator:
                desc = desc + " " + txt
        except:
            xpath_desc = "/html/body/section[1]/main/section/section/section/section/section/div[6]/p[2]"
            desc_elmt = self.tree_ad.xpath(xpath_desc)
            text_iterator = desc_elmt[0].itertext()
            desc = ""
            for txt in text_iterator:
                desc = desc + " " + txt

        # to get the images :
        # they are protected : a javascript code creates the link, so we have no direct access to the urls
        # we have to use selenium
        urls_img = self.get_pictures(self.url_ad)

        return city,  desc
    def __init__(self, url_ad):
        self.url_ad = url_ad
        htmlparser = etree.HTMLParser()
        page_ad = urlopen(url_ad)
        self.tree_ad = etree.parse(page_ad, htmlparser)
        self.city, self.desc = self.get_infos_ad()
