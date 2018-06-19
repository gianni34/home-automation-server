import _json
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, generics
from rest_framework.utils import json

from rest_framework.decorators import api_view, detail_route
from HomeAutomation.serializers import *
from HomeAutomation.models import *


class ListArtifacts(generics.ListAPIView):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer


class Artifacts(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer


class ListArtifactTypes(generics.ListAPIView):
    queryset = ArtifactType.objects.all().order_by('name')
    serializer_class = ArtifactSerializer


class ArtifactTypes(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArtifactType.objects.all()
    serializer_class = ArtifactTypeSerializer


class ListZones(generics.ListAPIView):
    queryset = Zone.objects.all().order_by('name')
    serializer_class = ZoneSerializer


class Zones(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class ListIntermediaries(generics.ListAPIView):
    queryset = Intermediary.objects.all().order_by('name')
    serializer_class = IntermediarySerializer


class Intermediaries(generics.RetrieveUpdateDestroyAPIView):
    queryset = Intermediary.objects.all()
    serializer_class = IntermediarySerializer


class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer


class Users(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListRoles(generics.ListAPIView):
    queryset = Role.objects.all().order_by('name')
    serializer_class = RoleSerializer


class Roles(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ListParameters(generics.ListAPIView):
    queryset = Parameters.objects.all().order_by('name')
    serializer_class = ParametersSerializer


class Parameters(generics.ListAPIView):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer


class ListScenes(generics.ListAPIView):
    queryset = Scene.objects.all().order_by('name')
    serializer_class = SceneSerializer


class Scene(generics.ListAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


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


@api_view(['PUT'])
def change_password(request):

    user = request.GET['user']
    old_password = request.GET['oPass']
    new_password = request.GET['nPass']

    usu = User.objects.filter(name=user).first()
    ret = usu.change_password(old_password, new_password)

    if ret == 'OK':
        return JsonResponse({'EXITO': 'OK'})
    else:
        return JsonResponse({'ERROR': ret})


def check_answer(request):

    user = request.GET['user']
    answer = request.GET['answer']

    u = User.objects.filter(name=user).first()
    ret = u.check_answer(answer)

    if ret:
        return JsonResponse({'EXITO': 'OK'})
    else:
        return JsonResponse({'ERROR': 'La respuesta no coincide.'})


def login(request):
    user = request.GET['user']
    password = request.GET['pass']

    response_data = {'result': False, 'message': 'Usuario y/o contraseña incorrectos.'}

    obj = User.objects.filter(name=user).first()
    if obj and obj.password == password:
        response_data = {'result': True, 'message': 'Inició correctamente.'}
    return JsonResponse(response_data)
    #return HttpResponse(json.dumps(response_data), content_type="application/json")


@api_view(['POST'])
def new_user(request):
    user = request.GET['usuario']
    new = request.GET['usuarioN']
    password = request.GET['pass']
    role = request.GET['rol']
    question = request.GET['pregunta']
    answer = request.GET['respuesta']

    usu = User.objects.filter(name=user).first()

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