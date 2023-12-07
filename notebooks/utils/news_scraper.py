from GoogleNews import GoogleNews
from newspaper import Article
import requests
import nltk
from fake_useragent import UserAgent
import ssl

from notebooks.utils import sentiment_analysis

keywords = ['xrp',
            'XRP',
            'Ripple Price Prediction',
            'XRP prediction']

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')
user_agent = UserAgent()


def get_news(period, path):
    score = 0

    headers = {'User-Agent': user_agent.random, "Upgrade-Insecure-Requests": "1", "DNT": "1",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    googlenews = GoogleNews(lang="en")
    googlenews.set_period(period)
    print("Scraping started.")
    index = 0
    scraped = []
    data_to_save = []
    titles = []
    for key in keywords:
        googlenews.get_news(key=key)
        articles = googlenews.result()
        for article in articles:
            title = article["title"]
            if title in titles:
                continue
            titles.append(title)
            url = article["link"]
            published_date = article["datetime"]
            try:
                r = requests.get(f"https://{url}", timeout=15, headers=headers)
                url = r.url
            except Exception:
                continue
            if not url in scraped:
                news_article = Article(url=url, language="en")
                try:
                    news_article.download()
                    news_article.parse()
                    news_article.nlp()
                    for c_key in keywords:
                        if c_key in news_article.text:
                            text = news_article.text.replace("\n\n", "\n")
                            data_to_save.append(f"{published_date}\n{news_article.title}\n{text}")

                            verdict = sentiment_analysis.flair_prediction(text)
                            if verdict == "POSITIVE":
                                score += 1
                            elif verdict == "NEGATIVE":
                                score -= 1
                            print(verdict)

                            index += 1
                            print(f"Sources scraped: {index}")
                            break
                    scraped.append(url)
                except Exception:
                    pass

    data_to_save = list(set(data_to_save))

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n\n".join(data_to_save))
    score = score / index
    return score
