from HomeAutomation.models import *
from rest_framework import serializers, status


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
        fields = ('id', 'name', 'intermediary', 'temperature', 'pin', 'type')


class ArtifactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactType
        fields = ('id', 'name')


class IntermediarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Intermediary
        fields = ('id', 'name', 'ip', 'user', 'password')


class UserSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(allow_null=True, required=False)
    old_password = serializers.CharField(allow_blank=True, required=False)
    # role = RoleSerializer

    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'question', 'answer', 'role', 'user', 'old_password')

    def create(self, validated_data):
        id_aux = validated_data['user']
        user_admin = User.objects.filter(id=id_aux).first()
        del validated_data['user']
        # del validated_data['old_password']
        if user_admin.is_admin():
            ret = super(UserSerializer, self).create(validated_data)
            return ret
        else:
            raise serializers.ValidationError({'ERROR': 'Debe ser administrador para dar de alta un usuario.'})

    def update(self, instance, validated_data):
        id_aux = validated_data['user']
        user_admin = User.objects.filter(id=id_aux).first()
        mod_user = User.objects.filter(id=instance.id).first()
        old_password = validated_data['old_password']
        del validated_data['user']
        del validated_data['old_password']
        if id_aux == mod_user.id:
            if not user_admin.verify_old_password(old_password):
                raise serializers.ValidationError({'ERROR': 'La contraseña actual no es correcta.'})
            else:
                ret = super(UserSerializer, self).update(mod_user, validated_data)
                return ret
        elif user_admin.is_admin():
            ret = super(UserSerializer, self).update(mod_user, validated_data)
            return ret
        else:
            raise serializers.ValidationError({'ERROR': 'Debe ser administrador para modificar un usuario.'})


class StateVariableSerializer(serializers.ModelSerializer):

    artifact = ArtifactSerializer()

    class Meta:
        model = StateVariable
        fields = ('id', 'name', 'artifact', 'type', 'typeUI', 'value', 'min', 'max', 'scale')
        depth = 1

    def create(self, validated_data):
        artifact = validated_data['artifact']
        del validated_data['artifact']
        artifact_aux = Artifact.objects.filter(name=artifact['name']).first()
        validated_data['artifact_id'] = artifact_aux.id
        ret = super(StateVariableSerializer, self).create(validated_data)
        return ret

    def update(self, instance, validated_data):
        # variable = StateVariable.objects.filter(id=validated_data['id'])
        variable = StateVariable.objects.filter(id=self.data['id']).first()
        ret = super(StateVariableSerializer, self).update(variable, validated_data)
        ret.change_variable(ret.artifact.power, ret.artifact.id, ret.value)
        return ret


class SceneActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneActions
        fields = ('id', 'variable', 'value')


class SceneSerializer(serializers.ModelSerializer):
    actions = SceneActionsSerializer(many=True)

    class Meta:
        model = Scene
        fields = ('id', 'name', 'description', 'end_time', 'initial_time', 'frequency', 'on_demand', 'actions')
        depth = 1

    def create(self, validated_data):
        actions = validated_data['actions']
        del validated_data['actions']
        ret = super(SceneSerializer, self).create(validated_data)
        actionSerializer = SceneActionsSerializer()
        for action in actions:
            action['scene'] = ret
            actionSerializer.create(action)
        return ret

    def update(self, instance, validated_data):
        sceneAux = Scene.objects.filter(id=validated_data['id'])
        ret = super(SceneSerializer, self).update(self, sceneAux, validated_data)
        return ret


class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = ('id', 'name', 'value')
