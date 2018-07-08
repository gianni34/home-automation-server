import _json
from django.http import JsonResponse, HttpResponse
from rest_framework import status, generics, viewsets
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


""""
@api_view(['PUT'])
def change_state(request):

    zone = request.GET['zone']
    name = request.GET['name']

    try:
        z = Zone.objects.filter(name=zone).first()
        artifact = Artifact.objects.filter(zone=z.id, name=name).first()
    except ValueError:
        #return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'ERROR': 'No se encontro el artefacto.'})

    state = request.GET['state']
    artifact.change_state(state)

    #return Response(status=status.HTTP_200_OK)
    return JsonResponse({'EXITO': 'Estado modificado con Exito'})

"""


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


def check_answer(request):

    user = request.data['user']
    answer = request.data['answer']

    u = User.objects.filter(name=user).first()
    ret = u.check_answer(answer)

    if ret:
        return JsonResponse({'EXITO': 'OK'})
    else:
        return JsonResponse({'ERROR': 'La respuesta no coincide.'})


def login(request):
    user = request.data['user']
    password = request.data['pass']

    response_data = {'result': False, 'message': 'Usuario y/o contraseña incorrectos.'}

    obj = User.objects.filter(name=user).first()
    if obj and obj.password == password:
        response_data = {'result': True, 'message': 'Inició correctamente.'}
    return JsonResponse(response_data)
    #return HttpResponse(json.dumps(response_data), content_type="application/json")


@api_view(['POST'])
def new_user(request):
    user = request.data['usuario']
    new = request.data['usuarioN']
    password = request.data['pass']
    role = request.data['rol']
    question = request.data['pregunta']
    answer = request.data['respuesta']

    usu = User.objects.filter(name=user).first()

    """"
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
    """

    if User.is_admin(usu):
        User.save(new, role, question, answer, password)
    else:
        return JsonResponse({'ERROR': 'Debe ser administrador para dar de alta un usuario.'})


def user_question(request):
    user = request.GET['user']
    response_data = {'result': False, 'question': ''}
    obj = User.objects.filter(name=user).first();
    if obj and obj.question:
        response_data = {'result': True, 'question': obj.question}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
