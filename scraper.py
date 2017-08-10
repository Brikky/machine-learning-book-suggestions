import csv, scrapy, sys
from scrapy.http import Request

scanned_users = []
users = []

with open('/Volumes/storage/goodreads-reviews.csv', 'a') as f:
  writer = csv.writer(f, lineterminator='\n')
  writer.writerows([["title", "rating", "user"]])
# writer = csv.writer(open('output.csv', 'a'), lineterminator='\n')
# writer.writerow(fields)

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
            return Request(url="https://www.goodreads.com/user/show/17438949-melissa-dog-lover-martin",
               callback=self.parse_friends)

    def parse_review_page(self, response):
        global scanned_users, users, writer
        thisUser = users.pop(0)
        scanned_users.append(thisUser)

        REVIEW_SELECTOR = 'tr.review'
        for review in response.css(REVIEW_SELECTOR):

            TITLE_SELECTOR = '.title a::attr(title)'
            RATING_SELECTOR = '.rating .value .staticStars .staticStar::attr(title)'
            title = review.css(TITLE_SELECTOR).extract()
            rating = review.css(RATING_SELECTOR).extract_first()

            if rating is not None:
                with open('/Volumes/storage/goodreads-reviews.csv', 'a') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerow([title[0], rating, thisUser])

        print(len(users), " users in line to be scraped")
        return Request(url="https://www.goodreads.com/user/show/" + users[0], callback=self.parse_friends)

    def parse_friends(self, response):
        global scanned_users, users

        FRIEND_SELECTOR = 'div.rightContainer div.left div.friendName a::attr(href)'
        theseusers = response.css(FRIEND_SELECTOR).extract()
        theseusers = [x.split('/')[3] for x in theseusers]

        for user in theseusers:
            if user not in users and user not in scanned_users:
                users.append(user)

        return Request(url="https://www.goodreads.com/review/list/"+users[0]+"?utf8=%E2%9C%93&order=d&sort=review&view=reviews&per_page=100", callback=self.parse_review_page)


 