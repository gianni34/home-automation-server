from HomeAutomation.models import Artifact, Intermediary, User , Role, Zone, State, ArtifactType
from rest_framework import serializers


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = ('id', 'zone', 'type', 'name', 'intermediary', 'pin', 'state')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
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
