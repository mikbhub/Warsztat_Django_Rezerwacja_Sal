from django.conf.urls import url

from . views import (
    SearchAvaliableAuditoriums,
    ShowSearchResults,
)

app_name = 'search'

urlpatterns = [
    url(r'^make-search/$', SearchAvaliableAuditoriums.as_view(), name='make-search'),
    url(r'^search-results/$', ShowSearchResults.as_view(), name='search-results'),
]
