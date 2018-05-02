from HomeAutomation.models import *
from rest_framework import serializers


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = ('id', 'zone', 'type', 'name', 'intermediary', 'pin')
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


class ValueVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueVariable
        fields = ('id', 'name', 'value', 'artifact', 'values')
        depth = 1


class BooleanVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanVariable
        fields = ('id', 'name', 'value', 'artifact', 'on')
        depth = 1


class ValueVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangeVariable
        fields = ('id', 'name', 'value', 'artifact', 'min', 'max', 'scale')
        depth = 1