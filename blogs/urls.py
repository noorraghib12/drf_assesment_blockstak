from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns= [
    path('me/blogs/setting/',BlogView.as_view()),
    path('<str:username>/blogs/',PublicBlogView.as_view())
]
# urlpatterns=format_suffix_patterns(urlpatterns)
