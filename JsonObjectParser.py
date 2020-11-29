from selenium import webdriver
from ParEgrul import ParEg
from ParZB import ParZB
from ParPos import ParPos


class JParsers:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"D:\Sourse\Python\bank\chromedriver.exe")
        self.eg = ParEg(self.driver)
        self.zb = ParZB(self.driver)
        self.pos = ParPos(self.driver)

    def find(self, name, sur):
        res = dict(name='name',
                   sur=sur,
                   egrul=self.eg.find(name, sur),
                   zachestnyibiznes=self.zb.find(name, sur),
                   zakupki=self.pos.find(name, sur))
        self.driver.quit()
        return res