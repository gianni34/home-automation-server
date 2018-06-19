from HomeAutomation.models import *
from rest_framework import serializers


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = ('id', 'zone', 'type', 'name', 'intermediary', 'pin', 'power')
        depth = 1


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'name')


class ArtifactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactType
        fields = ('id', 'name')


class IntermediarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Intermediary
        fields = ('id', 'name', 'ip', 'user', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'question', 'answer', 'role')


class StateVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateVariable
        fields = ('id', 'name', 'artifact', 'type', 'value', 'min', 'max', 'scale')
        depth = 1


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'name', 'description', 'end_time', 'initial_time', 'frequency', 'on_demand')


class SceneActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneActions
        fields = ('id', 'variable', 'value', 'scene')
        depth = 1


class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = ('id', 'name', 'value')
