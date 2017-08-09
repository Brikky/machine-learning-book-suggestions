## Scraping Process:
Variables:
```Python
rootUser #first user we'll start from, collected by hand
nextUser #next user whos reviews will be scraped
scrapedUsers #list of users we've already collected reviews from
reviewsByUser #list of scraped reviews
```

**1.** Start with some arbitrary `rootUser`

**2.** Go to their profile

**3.** Scrape friends of `rootUser` and their associated number of books
**<br>3.1** Add that friend with the greatest number of books to a list, `scrapedUsers` if they are not already present, and set `nextUser` to that user's username
**<br>3.2** If they are present, revert to the second, third, nth friend until a unique user is found
**<br>3.3** If no friends are unique, `exit`

**4.** Navigate to the reviews page of `rootUser`

**5.** Scrape all reviews from the page, stored in a list
<br>`reviewsByUser = ([bookTitle, review, user], [bookTitle, review, user], ...)`
**<br>5.1** Navigate to next review page if present, restart at step 5

**6.** Set `rootUser` to `nextUser`, and `nextUser` to `None`

**7.** Restart from 1
