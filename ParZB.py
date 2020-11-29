from Parser import Parser


class ParZB(Parser):
    def find(self, name, sur):
        res = None
        try:
            self.driver.get("https://zachestnyibiznes.ru/")
            self.driver.find_element_by_xpath('//*[@id="query"]').send_keys(str(name) + " " + str(sur))
            self.driver.find_element_by_xpath('//*[@id="query-form"]/div[1]/span/button[1]').click()
            els = self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div[3]/table/tbody')\
                .find_elements_by_tag_name('tr')
            if len(els) > 10:
                els = els[0::10]
            res = list()
            for a in els:
                td = a.find_elements_by_tag_name('td')
                res.append(dict(com=td[0].find_element_by_tag_name('a').text,
                                stat=td[1].find_element_by_tag_name('span').text,
                                inn=td[2].text,
                                name=td[3].text,
                                date=td[4].text,
                                adr=td[5].text))
        finally:
            if res:
                return res