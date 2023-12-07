import time
from notebooks.utils import news_scraper
from notebooks.utils import sentiment_analysis


while True:

    date = '1h'
    prediction = news_scraper.get_news(period=date, path='data')

    if prediction < 0:
        print("S")

    elif prediction > 0:
        print("B")
    else:
        print("chillin")

    time.sleep(1800)

