from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

# Create your views here.
def scrape(request):
  session = requests.Session()
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  url = "https://www.theonion.com/"

  content = session.get(url, verify=False).content
  soup = BSoup(content, "html.parser")
  News = soup.find_all('div', {"class":"curation-module__item"})
  for artcile in News:
    main = artcile.find_all('a')[0]
    link = main['href']
    image_src = str(main.find('img')['srcset']).split(" ")[-4]
    title = main['title']
    new_headline = Headline()
    new_headline.title = title
    new_headline.url = link
    new_headline.image = image_src
    new_headline.save()
  return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, 'news/home.html', context)