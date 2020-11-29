from Parser import Parser


class ParPos(Parser):
    def find(self, name, sur):
        res = None
        try:
            self.driver.get("https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html")
            self.driver.find_element_by_xpath('//*[@id="searchString"]').send_keys(str(name) + " " + str(sur))
            self.driver.find_element_by_xpath('/html/body/form/section[1]/div/div/div/div[2]/div/div/button').click()
            els = self.driver.find_element_by_class_name('search-registry-entrys-block')\
                .find_elements_by_class_name("search-registry-entry-block")
            if len(els) > 10:
                els = els[0::10]
            res = list()
            for a in els:
                res.append(dict(com=a.find_element_by_class_name('registry-entry__body-value').text,
                                num=a.find_element_by_class_name('registry-entry__header-mid__number')\
                                .find_element_by_tag_name('a').text,
                                inn=a.find_elements_by_class_name('registry-entry__body-value')[1].text))
            for a in res:
                print(a)
            print("\n")
            print("############################################")
        finally:
            if res:
                return res
