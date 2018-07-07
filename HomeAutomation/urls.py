from django.conf.urls import include, url
from rest_framework import routers
from HomeAutomation import views

router = routers.DefaultRouter()
router.register(r'scenes', views.SceneViewSet)
router.register(r'statevariables', views.StateVariableViewSet)

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
    url(r'^parameters/$', views.ListParameters.as_view()),
    url(r'^parameter/(?P<pk>[0-9]+)/$', views.Parameters.as_view()),
    # url(r'^scenes/$', views.ListScenes.as_view()),
    # url(r'^scene/(?P<pk>[0-9]+)/$', views.Scene.as_view()),
    # url(r'^scenes/$', views.scene_list),
    # url(r'^scene/(?P<pk>[0-9]+)/$', views.scene_detail),
    url(r'^changeState$', views.change_state, name='change_state'),
    url(r'^changePassword$', views.change_password, name='change_password'),
    url(r'^login$', views.login, name='login'),
    url(r'^', include(router.urls))
]
