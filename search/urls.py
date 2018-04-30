from django.conf.urls import url

app_name = 'search'

from .views import (
        SearchProductView
        )

urlpatterns = [
    url(r'^$', SearchProductView.as_view(), name='query'),
]

