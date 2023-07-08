# Web Crawler for Amazon Product Price Monitoring
This project aims to create a web crawler specifically designed to check the prices of products on Amazon. The goal is to monitor the price changes over time for the specified products and provide analysis through a frontend interface. The project will be divided into several steps to achieve the desired outcome.

# Step 1: Creating the Product Information Bot
In this step, a bot will be developed to make requests to Amazon's search results page and retrieve product information. The bot will be built using the Scrapy framework, a powerful tool for web scraping. By utilizing Scrapy, we can efficiently extract data from the HTML structure of the search results page.

The bot will be responsible for scraping essential product details such as the product title, price, and availability. It will navigate through multiple pages of search results if necessary, ensuring that all relevant products are included in the data collection process.

# Step 2: Daily Execution and Default Products
To continuously monitor price changes over time, the application needs to run on a daily basis. In this step, we will implement the necessary scheduling mechanism to automate the execution of the web crawler. A script or scheduler task will be created to trigger the crawler's execution at the specified interval.

Additionally, a list of default products will be defined. These products will be analyzed by the web crawler on a daily basis, even if no specific user input is provided. This ensures that consistent data is collected for analysis, and any price changes are captured for these default products.

# Step 3: Frontend Interface for Data Analysis
To facilitate the analysis of collected data, a frontend interface will be developed. The interface will provide users with an intuitive and visually appealing platform to explore the price changes and trends of the monitored products.

A NextJS web application will be set up to serve the frontend interface. The application will handle requests from the user interface and communicate with the backend to fetch and display the analyzed data. HTML, CSS, and JavaScript frameworks can be utilized to design and implement the frontend interface.

The frontend interface will offer features such as graphical visualizations of price history, charts displaying price fluctuations over time, and filtering options to customize the displayed data. This will enable users to gain insights into the behavior of the monitored products and make informed decisions based on the price trends.

# How to create an environment to run the application
## First step:
Go to root of ur computer running: cd ~
## Second step:
python3 -m venv priceChecker
## Third step:
source priceChecker/bin/activate
## Foutrh step:
deactivate