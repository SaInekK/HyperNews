from django.urls import path, include

from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', main_page, name='home'),
    path('news/<int:link>/', ShowPost.as_view(), name='post'),
    path('news/create/', CreatePost.as_view(), name='create'),
    path('news/', MainPage.as_view(), name='main'),
]

urlpatterns += static(settings.STATIC_URL)
