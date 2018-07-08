import _json
from django.http import JsonResponse, HttpResponse
from rest_framework import status, viewsets
from rest_framework.utils import json

from rest_framework.decorators import api_view, detail_route
from HomeAutomation.serializers import *
from HomeAutomation.models import *
from HomeAutomation.business import *


class ArtifactsViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer


class ArtifactTypesViewSet(viewsets.ModelViewSet):
    queryset = ArtifactType.objects.all()
    serializer_class = ArtifactTypeSerializer


class ZonesViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class IntermediariesViewSet(viewsets.ModelViewSet):
    queryset = Intermediary.objects.all()
    serializer_class = IntermediarySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ParametersViewSet(viewsets.ModelViewSet):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer


class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


class StateVariableViewSet(viewsets.ModelViewSet):
    queryset = StateVariable.objects.all()
    serializer_class = StateVariableSerializer


@api_view(['PUT'])
def set_temperature(request):

    print("------- algo consume el servicio -----------")
    print(request.data)
    intermediary = request.data['intermediary']
    print(intermediary)
    value = request.data['value']
    print(value)

    try:
        i = Intermediary.objects.filter(name=intermediary).first()
        z = Zone.objects.filter(intermediary=i.id).first()
        z.set_temperature(value)
    except ValueError:
        #return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'ERROR': 'No se encontró la zona correspondiente.'})

    #return Response(status=status.HTTP_200_OK)
    return JsonResponse({'EXITO': 'Estado modificado con Exito'})


""""
@api_view(['PUT'])
def change_password(request):

    user = request.data['user']
    old_password = request.data['oPass']
    new_password = request.data['nPass']

    usu = User.objects.filter(name=user).first()
    ret = usu.change_password(old_password, new_password)

    if ret == 'OK':
        return JsonResponse({'EXITO': 'OK'})
    else:
        return JsonResponse({'ERROR': ret})
"""


def check_answer(request):

    user = request.data['user']
    answer = request.data['answer']

    u = User.objects.filter(name=user).first()
    if u.check_answer(answer):
        return HttpResponse('Respuesta correcta.', status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("Respuesta incorrecta incorrectos.", status=status.HTTP_400_BAD_REQUEST)


def login(request):
    user = request.data['user']
    password = request.data['pass']

    obj = User.objects.filter(name=user).first()
    if obj.login(password):
        return HttpResponse('Inició correctamente.', status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("Usuario y/o contraseña incorrectos.", status=status.HTTP_400_BAD_REQUEST)


def user_question(request):
    user = request.data['user']
    obj = User.objects.filter(name=user).first();
    question = obj.get_question()
    return HttpResponse(question, content_type="application/json")
