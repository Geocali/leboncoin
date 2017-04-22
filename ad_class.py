import re

class ad_class:
    def __init__(self, title, price, url, time, city, img):
        self.title = title
        self.price = price
        self.url = url
        self.time = time
        self.city = city
        self.img = img

        # we try to get the capacity from the title
        ah = self.return_ah(self.title)
        # if we don't succeed, we try from the text of the ad
        if (ah == None):
            page_details = detailed_page_class(self.url)
            ah = self.return_ah(self.desc)
        # if we don't succeed, we try to find the info in the pictures
        if (ah == None):
            pass
        self.ah = ah
        print(self.title, self.price)
    # first evaluation to see if the ad is interesting
    # returns True if the ad is interesting
    def looks_interesting(self):
        if float(self.price) > 300:
            return False
        print(str(self.ah / self.price) + " ah/euros")
        return True

    def return_ah(self, string):
        pattern = re.compile(r'([0-9.,]*\Smah)', re.IGNORECASE)
        if (pattern.search(string) != None):
            ah = pattern.search(string).groups()[0][:-3].replace(",", ".")
            return float(ah)/1000
        pattern = re.compile(r'([0-9.,]* mah)', re.IGNORECASE)
        if (pattern.search(string) != None):
            ah = pattern.search(string).groups()[0][:-4].replace(",", ".")
            return float(ah)/1000
        pattern = re.compile(r'([0-9.,]*\Sah)', re.IGNORECASE)
        if (pattern.search(string) != None):
            ah = pattern.search(string).groups()[0][:-2].replace(",", ".")
            return float(ah)
        pattern = re.compile(r'([0-9.,]* ah)', re.IGNORECASE)
        if (pattern.search(string) != None):
            ah = pattern.search(string).groups()[0][:-3].replace(",", ".")
            return float(ah)
