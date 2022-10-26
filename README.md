# InstagramSortPostsByLikesBot

This project shows a scraper which can sort all posts of a profile by their likes. I coded this because I was running an instagram page and wanted to know which posts perform well in my niche.
So I decided to code a scraper.

The scraper is coded with python and uses packages for web scraping like BeautifulSoup and selenium. 

Selenium is used for all the clicking and input actions. You only need to reconstruate the whole clicking process as code. You need the class names for the HTML elements.
Watch out: They change with time, so you need to adapt them.

BeatifulSoup is used for extracting the links from all posts e.g.

Challenges:
The greatest challenge is that you can't scrape all post data at once. They load dynamically, so you need to scroll until the bottom of a profile and scrape the required data meanwhile.
There was a helpful tutorial from for that:

Whole process explained:

1. Open chrome

2. Click away the cookie window

3. Login

4. Go to the profile

5. scroll through the whole profile and get the links

6. Go through all the post links and scrape nr of likes

7. Data will be saved to dataframe and then to .json file

8. No you can analyze the data
