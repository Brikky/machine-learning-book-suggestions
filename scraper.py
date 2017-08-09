import scrapy
from scrapy.http import Request
import sys


class GoodreadsSpider(scrapy.Spider):
    name = "Goodreads_spider"
    start_urls = ['https://www.goodreads.com/']

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                    formdata={'user[email]': 'brandon.kerr160@topper.wku.edu', 'user[password]': self.password},
                    callback=self.after_login)

    def after_login(self, response):
        # check login succeed before going on
        if b"recognize that email" in response.body:
            print ("################ERROR##################")
            return
        else:
            #authenticated
            return Request(url="https://www.goodreads.com/review/list/17438949-melissa-dog-lover-martin?utf8=%E2%9C%93&sort=rating&view=reviews&per_page=100",
               callback=self.parse_page)

    def parse_page(self, response):
        REVIEW_SELECTOR = 'tr.review'
        for review in response.css(REVIEW_SELECTOR):

            TITLE_SELECTOR = '.title a::attr(title)'
            RATING_SELECTOR = '.rating .value .staticStars .staticStar::attr(title)'
            title = review.css(TITLE_SELECTOR).extract()
            rating = review.css(RATING_SELECTOR).extract_first()

            print(title[0], '\n', rating)
            # yield{
            #     'title': title,
            #     'rating': rating
            # } 
