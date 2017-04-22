


class page_class:
    def __init__(self, url_request):
        htmlparser = etree.HTMLParser()
        page_ads = urlopen(url_request)
        self.tree_ads = etree.parse(page_ads, htmlparser)
    def get_infos_ad(self, i):
        ad_glob = self.tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a")
        ad_url = "http:" + ad_glob[0].values()[0]
        ad_title = ad_glob[0].values()[1]

        ad_img = self.tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/div[1]/span[1]/span[1]")
        url_img_ad = "http:" + ad_img[0].values()[2]

        ad_city_elmt = self.tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/section/p[2]")
        ad_city = ad_city_elmt[0].getchildren()[0].values()

        ad_price_elmt = self.tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[" + str(i) + "]/a/section/h3")
        ad_price = ad_price_elmt[0].values()[2]

        ad_time_elmt = self.tree_ads.xpath("/html/body/section[1]/main/section/section/section/section/ul/li[1]/a/section/aside/p")
        ad_time = ad_time_elmt[0].values()[2]

        return ad_class(ad_title, ad_price, ad_url, ad_time, ad_city, url_img_ad)
