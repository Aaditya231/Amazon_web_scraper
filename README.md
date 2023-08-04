# Default assignment
# Amazon Product Scraper

This Python script scrapes product information from Amazon.in based on a search query. It utilizes the `BeautifulSoup` library to parse HTML content and extract relevant data such as product names, ratings, prices, and descriptions.

## Features

- Fetches product information from Amazon.in search results.
- Retrieves product details including name, rating, rating count, price, and description.
- Handles pagination to scrape multiple pages of search results.
- Outputs scraped data to a CSV file for further analysis.

## Prerequisites

- Python 3.x
- Required Python libraries: `BeautifulSoup`, `pandas`,'gzip', 'urllib'

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/amazon-product-scraper.git

## Insights
The number of pages can be taken as an input , I used a loop and count to know if the total rows hit 2k then the loop will break 
The code gives description not available in some cases, I tried to solve this problem but was unable to find the solution the the given time frame.
The code can be made better by adding some more try and catch statements to cover different layouts as per our requirements
Two sample outputs are added in the repository covering a lot to analyse 
The code is slow because I had to add the delay in order to bypass the server security
Best option is to avoid captcha so I made a detailed user-agent
The requests library of python was not working properly and was giving 503 response and I spent a lot of time scrolling the web to find a solution to make it work like adding different user agents or adding more delay but in the end when I used urllib.request it worked fine
