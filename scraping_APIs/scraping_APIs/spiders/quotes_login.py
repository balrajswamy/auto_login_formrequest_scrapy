import scrapy
from scrapy import FormRequest


class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        print("response_url=>", response.url)
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        print("token=>", csrf_token)

        yield FormRequest.from_response(response,
                                        formxpath="//form",
                                        formdata={"csrf_token":csrf_token,
                                                  "username":"admin",
                                                  "password":"123"},
                                        callback = self.after_login)
    def after_login(self,response):
        if response.xpath("//p/a[contains(@href,'logout')]/text()").get():
            print("Logged success!")
        else:
            print("Login Failed")


