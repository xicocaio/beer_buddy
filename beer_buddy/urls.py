from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from stores import views

urlpatterns = [
    url(r'^pdvs$', views.PDVList.as_view(), name='create'),
    url(r'^pdvs/(?P<pk>[0-9]+)/$', views.PDVDetail.as_view(), name='details'),
    url(r'^pdvs/search', views.PDVSearch.as_view(), name='search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
