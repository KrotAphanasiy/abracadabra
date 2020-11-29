from Parser import Parser
from time import sleep


class ParEg(Parser):
    def find(self, name, sur):
        res = None
        try:
            self.driver.get("https://egrul.nalog.ru/index.html")
            self.driver.find_element_by_xpath('//*[@id="query"]').send_keys(str(name) + " " + str(sur))
            self.driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
            sleep(3)
            els = self.driver.find_elements_by_class_name('res-row')
            res = list()
            for a in els:
                res.append(dict(name=a.find_element_by_class_name('op-excerpt').text,
                                text=a.find_element_by_class_name('res-text').text))
            for a in res:
                print(a)
            print("\n")
            print("############################################")
        finally:
            if res:
                return res
