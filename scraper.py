import csv, scrapy, sys
from scrapy.http import Request

scanned_users = []
users = ['17438949-melissa-dog-lover-martin']

with open('/Volumes/storage/goodreads-book-reviews.csv', 'a') as f:
  writer = csv.writer(f, lineterminator='\n')
  writer.writerows([["title", "rating", "user"]])

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

        thisUser = users[0]
        nextUser = users[1]
        
        REVIEW_SELECTOR = 'tr.review'
        for review in response.css(REVIEW_SELECTOR):

            TITLE_SELECTOR = '.title a::attr(title)'
            RATING_SELECTOR = '.rating .value .staticStars .staticStar::attr(title)'
            title = review.css(TITLE_SELECTOR).extract()
            rating = review.css(RATING_SELECTOR).extract_first()

            if rating is not None:
                with open('/Volumes/storage/goodreads-book-reviews.csv', 'a') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerow([title[0], rating, thisUser])

        print('\n\n', len(users), " users in line to be scraped ", 'previous: ', thisUser, ' next: ', nextUser)

        nextPage = response.css('a.next_page::attr(href)').extract_first()

        if nextPage is not None:
            return Request(url="https://www.goodreads.com"+ nextPage, callback=self.parse_review_page, dont_filter=True, meta = {'dont_redirect': True, 'handle_httpstatus_list': [301,302]})    
        
        users.pop(0)
        scanned_users.append(thisUser)
        return Request(url="https://www.goodreads.com/user/show/" + nextUser, callback=self.parse_friends, dont_filter=True, meta = {'dont_redirect': True, 'handle_httpstatus_list': [301,302]})

    def parse_friends(self, response):
        global scanned_users, users

        FRIEND_SELECTOR = 'div.rightContainer div.left div.friendName a::attr(href)'
        theseusers = response.css(FRIEND_SELECTOR).extract()
        theseusers = [x.split('/')[3] for x in theseusers]

        for user in theseusers:
            if user not in users and user not in scanned_users:
                users.append(user)

        return Request(url="https://www.goodreads.com/review/list/"+users[0]+"?utf8=%E2%9C%93&order=d&sort=review&view=reviews&per_page=100", callback=self.parse_review_page, dont_filter=True, meta = {'dont_redirect': True, 'handle_httpstatus_list': [301,302]})