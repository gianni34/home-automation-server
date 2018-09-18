from django.conf.urls import include, url
from rest_framework import routers
from HomeAutomation import views
from HomeAutomation.business import Main

router = routers.DefaultRouter()
router.register(r'scenes', views.SceneViewSet)
router.register(r'listScenes', views.ListScenesViewSet)
router.register(r'stateVariables', views.StateVariableViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'zones', views.ZonesViewSet)
router.register(r'parameters', views.ParametersViewSet)

urlpatterns = [
    url(r'^setTemperature$', views.set_temperature, name='set_temperature'),
    url(r'^deleteUser$', views.delete_user, name='delete_user'),
    url(r'^checkAnswer', views.check_answer, name='check_answer'),
    url(r'^userQuestion$', views.user_question, name='user_question'),
    url(r'^createUser$', views.new_user, name='new_user'),
    url(r'^login$', views.login, name='login'),
    url(r'^changePower$', views.change_power, name='change_power'),
    url(r'^changeVariable', views.change_variable, name='change_variable'),
    url(r'^executeScene', views.execute_scene, name='execute_scene'),
    url(r'^', include(router.urls))
]

# Main.scheduler()
