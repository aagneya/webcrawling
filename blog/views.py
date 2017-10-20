from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Crawler
from .forms import CrawlerForm
from django.utils import timezone

import sys
import bs4 as bs
import urllib2

import feedparser

import smtplib
import os


def index(request):
    return render(request, 'index.html', {})


@login_required
def home(request):
    form = CrawlerForm()
    return render(request, 'home.html', {'form':form})


def search(request):

    if request.method == "POST":
       form = CrawlerForm(request.POST)
       if form.is_valid():
          post = form.save(commit=False)
          post.published_date = timezone.now()
          post.save()

       posts = {}

         ##### 2 lists stop words ######
       lis1 = []
       lis2 = []



         #### search word
       search = request.POST.get('search','')

       mail = request.POST.get('mail','')

       search = search.split()

         ### stop words checking #####


       stop_words_list = open(os.path.abspath("stop_words.txt")).read().split()
       for word in search:
           if word not in stop_words_list:

              lis1.append(word)
           else:
              lis2.append(word)


         ##### checking the list items stop_words and other words ##########
       if len(lis1) == 0:

          st = " ".join(lis2).title().split()
          stri = "".join(st)

       else:
          st = " ".join(lis1).title().split()
          stri = "".join(st)



         ####### urls retrieving ##########
       sauce = urllib2.urlopen("https://en.wikipedia.org/wiki/"+stri).read()
       soup = bs.BeautifulSoup(sauce,'lxml')

          ###### limiting the paragraph #######
       all_data = soup.find_all("p")[0:3]
       for para in all_data:
             dic = para.text
             posts[dic] = dic

         ############### RSS READERRRRR #######################

       rss = feedparser.parse("https://www.reddit.com/r/"+stri+"/.rss")
       lis = {}

       feed = rss.entries[0:3]
       for post in feed:
             lis[post.title] = post.link


             mail = request.user.email
             server = smtplib.SMTP('smtp.gmail.com', 587)

             server.starttls()
                    #Next, log in to the server
             server.login("nibinshatest@gmail.com", "1234!@#$")

                    #Send the mail
             msg = post.title # The /n separates the message from the headers
             msg = msg.encode('ascii', 'ignore').decode('ascii')
             server.sendmail("nibinshatest@gmail.com", mail, msg)




       return render(request, 'result.html', {'posts': posts,'value': lis})
    else:
         return render(request, 'index.html', {})



def about(request):
    return render(request, 'about.html', {})


################# LAst SEARCH Result #####################
@login_required
def Last_search(request):
    search = Crawler.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'last_search.html', {'search':search})
