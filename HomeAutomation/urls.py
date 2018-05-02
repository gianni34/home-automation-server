from django.conf.urls import include, url
from rest_framework import routers
from HomeAutomation import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^users/$', views.ListUsers.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.Users.as_view()),
    url(r'^zones/$', views.ListZones.as_view()),
    url(r'^zone/(?P<pk>[0-9]+)/$', views.Zones.as_view()),
    url(r'^intermediaries/$', views.ListIntermediaries.as_view()),
    url(r'^intermediary/(?P<pk>[0-9]+)/$', views.Intermediaries.as_view()),
    url(r'^artifacts/$', views.ListArtifacts),
    url(r'^artifact/(?P<pk>[0-9]+)/$', views.Artifacts.as_view()),
    url(r'^artifactType/(?P<pk>[0-9]+)/$', views.ArtifactTypes.as_view()),
    url(r'^artifactTypes/$', views.ListArtifactTypes),
    url(r'^roles/$', views.ListRoles),
    url(r'^role/(?P<pk>[0-9]+)/$', views.Roles.as_view()),
    url(r'^changeState$', views.change_state, name='change_state'),
    url(r'^changePassword$', views.change_password, name='change_password'),
    url(r'^login$', views.login, name='login'),
]
