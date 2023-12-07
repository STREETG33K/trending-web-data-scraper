from requests_html import HTML, HTMLSession

session = HTMLSession()
url = 'https://news.google.com/search?q=xrp%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen'

r = session.get(url)

r.html.render(sleep=1, scrolldown=0)

articles = r.html.find('article')

newslist = []

#loop through each article to find the title and link. try and except as repeated articles from other sources have different h tags.
for item in articles:
    try:
        newsitem = item.find('h3', first=True)
        title = newsitem.text
        link = newsitem.absolute_links
        newsarticle = {
            'title': title,
            'link': link 
        }
        newslist.append(newsarticle)
    except:
       pass

#print the length of the list
print(len(newslist))

