# B3 tickers
### What it is
This is a web scraping tool designed to get all the tickers from companies listed on B3 and save it as a CSV.

### How to use it
The requirements for running the application are:

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [Pandas library](https://pandas.pydata.org/)
- [Selenium library](https://www.selenium.dev/)
- [Chrome Webdriver](https://chromedriver.chromium.org/downloads)

It's also needed to change the path for the webdriver in the program ``` get_b3_tickers.py ```

### The output
There is in this repository an output for the day 25/03/2022. It's a CSV file with the ticker, the name of the company, the fantasy name, as well as the Corporate Governance Levels of the companies. If ran, an updated output will be generated.
