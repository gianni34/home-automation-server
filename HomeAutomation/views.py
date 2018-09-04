import _json
from django.http import JsonResponse, HttpResponse
from rest_framework import status, viewsets
from rest_framework.utils import json

from rest_framework.decorators import api_view, detail_route
from HomeAutomation.serializers import *
from HomeAutomation.models import *
from HomeAutomation.business import *

error_not_admin_message = {'result': False, 'message': 'No tiene permisos de administrador.'}
error_temperature = {'result': False, 'message': 'Falta algún dato en el mensaje enviado por el sensor.'}
error_inputs = {'result': False, 'message': 'Falta algún dato requerido para la operación.'}


class ZonesViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    @detail_route()
    def artifact_list(self, request, pk=None):
        zone = self.get_object()  # retrieve an object by pk provided
        artifacts = Artifact.objects.filter(zone=zone).distinct()
        artifact_json = ArtifactSerializer(artifacts, many=True)
        # artifacts_json = json.dumps(artifacts)
        # return HttpResponse(artifacts, content_type="application/json", status=200)
        return JsonResponse(artifact_json.data, safe=False)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
    try:
        intermediary = request.data['intermediary']
        value = request.data['value']
    except e:
        # falta loggear el error
        return JsonResponse({'result': False, 'message': 'Falta algún dato en el mensaje enviado por el sensor.'})

    try:
        i = Intermediary.objects.filter(name=intermediary).first()
        z = Zone.objects.filter(intermediary=i.id).first()
        z.set_temperature(value)
    except ValueError:
        return JsonResponse({'result': False, 'message': 'No se encontró la zona correspondiente.'})
    return Response(status=status.HTTP_200_OK)


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


@api_view(['DELETE'])
def delete_user(request):
    try:
        user = request.data['user']
        id = request.data['id']
        admin = User.objects.get(id=user)
    except e:
        # falta loggear el error
        return JsonResponse({'result': False, 'message': 'Falta algún dato en el mensaje enviado.'})
    if not admin or not admin.isAdmin:
        return JsonResponse(error_not_admin_message)
    if User.objects.get(id=id):
        User.objects.get(id=id).delete()
    response_data = {'result': True, 'message': 'Usuario eliminado.'}
    return JsonResponse(response_data)


@api_view(['PUT'])
def check_answer(request):
    try:
        user = request.data['user']
        answer = request.data['answer']
    except e:
        # falta loggear el error
        return JsonResponse({'result': False, 'message': 'Falta algún dato en el mensaje enviado por el sensor.'})
    u = User.objects.filter(name=user).first()
    if u.check_answer(answer):
        return HttpResponse('Respuesta correcta.', status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("Respuesta incorrecta incorrectos.", status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def login(request):
    try:
        user = request.data['user']
        password = request.data['password']
    except e:
        # falta loggear el error
        return JsonResponse({'result': False, 'message': 'Falta algún dato en el mensaje enviado por el sensor.'})
    response_data = {'result': False, 'message': 'Usuario y/o contraseña incorrectos.'}
    obj = User.objects.filter(name=user).first()
    if obj and obj.login(password):
        response_data = {'result': True, 'message': 'Inició correctamente.', 'data': obj.id}
        return JsonResponse(response_data)
    return JsonResponse(response_data)


@api_view(['PUT'])
def change_power(request):
    # try:
    artifact = request.data['artifact']
    power = request.data['power']
    # except e:
    # falta loggear el error
    #    return JsonResponse(error_inputs)
    response_data = {'result': False, 'message': 'Se produjo un error, no se encontró el artefacto.'}
    obj = Artifact.objects.filter(id=artifact).first()
    if obj:
        # mandarle al onion correspondiente que prenda/apague
        obj.change_power(power)

        if power:
            response_data = {'result': True, 'message': 'El artefacto se prendio correctamente.', 'data': obj.id}
        else:
            response_data = {'result': True, 'message': 'El artefacto se apago correctamente.', 'data': obj.id}
    return JsonResponse(response_data)


@api_view(['PUT'])
def change_variable(request):
    # try:
    variable = request.data['variable']
    value = request.data['value']
    # except e:
    # falta loggear el error
    #    return JsonResponse(error_inputs)
    response_data = {'result': False, 'message': 'Se produjo un error, no se encontró la variable.'}
    obj = StateVariable.objects.filter(id=variable).first()
    if obj:
        # mandarle al onion correspondiente que prenda/apague
        obj.change_variable(value)

        response_data = {'result': True, 'message': 'La variable se modificó correctamente.', 'data': obj.id}
    return JsonResponse(response_data)


@api_view(['POST'])
def new_user(request):
    try:
        user = request.data['user']
        admin = request.data['admin']
    except e:
        # falta loggear el error
        return JsonResponse(error_inputs)
    if len(User.objects.filter(name=user["name"])) > 0:
        return JsonResponse({'result': False, 'message': 'El nombre de usuario ingresado ya existe.'})
    usu = User.objects.filter(id=admin).first()

    if User.is_admin(usu):
        new = User()
        new.name = user["name"]
        new.isAdmin = user["isAdmin"]
        new.password = user["password"]
        new.save()
        return JsonResponse({'result': True})
    else:
        return JsonResponse(error_not_admin_message)


@api_view(['PUT'])
def user_question(request):
    try:
        user = request.data['user']
    except e:
        # falta loggear el error
        return JsonResponse(error_inputs)
    response_data = {'result': False, 'question': ''}
    obj = User.objects.filter(name=user).first()
    if obj and obj.question:
        response_data = {'result': True, 'question': obj.question}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

