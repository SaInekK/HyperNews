from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
import json
import random
from itertools import groupby
from datetime import datetime
# Create your views here.


def main_page(request):
    return redirect('/news')


class ShowPost(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as f:
            posts = json.load(f)
            for post in posts:
                if post['link'] == kwargs['link']:
                    break
        return render(request, 'post.html', {'post': post})


class MainPage(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as f:
            posts = json.load(f)
            q = request.GET.get('q')
            print(f'q: {q}')
            if q:
                posts = [post for post in posts if q in post['title']]

            posts.sort(key=lambda x: x['created'], reverse=True)
            data = []
            for k, g in groupby(posts, key=lambda x: x['created'][:10]):
                data.append({'date': k, 'posts': list(g)})
            # print(query)
            # print(data)
        return render(request, 'main.html', {'posts': data})


class CreatePost(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r+') as f:
            list_of_posts = json.load(f)
            f.seek(0)
            print(list_of_posts)
            links = [a_dict['link'] for a_dict in list_of_posts]
            while True:
                link = random.randint(1, 10000000)
                if link not in links:
                    break
            date = datetime.now().isoformat(' ', 'seconds')
            title = request.POST.get('title')
            text = request.POST.get('text')
            list_of_posts.append({'created': date, 'text': text, 'title': title, 'link': link})
            print(list_of_posts)
            json.dump(list_of_posts, f)
        return redirect('/news')
