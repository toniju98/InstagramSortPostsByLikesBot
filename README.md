# InstagramSortPostsByLikesBot

**InstagramSortPostsByLikesBot** is a web scraping project that allows you to sort an Instagram profile's posts by the number of likes they have received. This project originated in 2021 when I managed an Instagram page and wanted to understand the performance of my posts within a specific niche. To achieve this, I developed this web scraper.

## Technologies Used

This scraper is developed using Python and relies on key packages for web scraping, including BeautifulSoup and Selenium. While BeautifulSoup is used to extract post links, Selenium handles all the clicking and input actions. To utilize the scraper effectively, you'll need to reconstruct the clicking process in code.

## Challenges Faced

The primary challenge with this scraper is that Instagram loads posts dynamically. As a result, you must scroll through the profile to trigger the loading of posts and simultaneously scrape the required data.

## The Complete Process Explained

Here's a step-by-step breakdown of the entire process:

1. Open Google Chrome.

2. Dismiss the cookie window if it pops up.

3. Log in to the Instagram account.

4. Navigate to the target profile.

5. Scroll through the entire profile to ensure that all posts are loaded and retrieve their links.

6. Visit each post link and extract the number of likes.

7. Store the scraped data in a dataframe and then save it to a .json file for further analysis.

8. Analyze the obtained data to gain insights into post performance.

Please note: The code may no longer work as expected due to changes in HTML tags over time. You may need to adapt it to the current structure of the Instagram website.

Feel free to explore and modify the code to suit your specific needs or to adapt to any changes in Instagram's web structure. Happy scraping!

