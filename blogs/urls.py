from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns= [
    path('blogs/',BlogView.as_view()),
]
# urlpatterns=format_suffix_patterns(urlpatterns)
