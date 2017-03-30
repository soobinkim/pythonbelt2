from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$',views.process),
    url(r'^logout$',views.logout),
    url(r'^travels$', views.travel),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^add$', views.add),
    url(r'^addplan$', views.addplan)
]
