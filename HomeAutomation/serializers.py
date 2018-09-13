from HomeAutomation.models import *
from HomeAutomation.business import *
from rest_framework import serializers, status


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

    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'question', 'answer', 'user', 'old_password', 'isAdmin')

    def create(self, validated_data):
        id_aux = validated_data['user']
        user_admin = User.objects.filter(id=id_aux).first()
        del validated_data['user']
        # del validated_data['old_password']
        if user_admin.is_admin():
            ret = super(UserSerializer, self).create(validated_data)
            return ret
        else:
            raise serializers.ValidationError({'result': False, 'message': 'Debe ser administrador para dar de alta un usuario.'})

    def update(self, instance, validated_data):
        id_aux = validated_data['user']
        user_admin = User.objects.filter(id=id_aux).first()
        mod_user = User.objects.filter(id=instance.id).first()
        old_password = validated_data['old_password']
        del validated_data['user']
        del validated_data['old_password']
        if id_aux == mod_user.id:
            if not user_admin.verify_old_password(old_password):
                raise serializers.ValidationError({'result': False, 'message': 'La contraseña actual no es correcta.'})
            else:
                ret = super(UserSerializer, self).update(mod_user, validated_data)
                return ret
        elif user_admin.is_admin():
            ret = super(UserSerializer, self).update(mod_user, validated_data)
            return ret
        else:
            raise serializers.ValidationError({'result': False, 'message': 'Debe ser administrador para modificar un usuario.'})


class VariableRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariableRange
        fields = ('id', 'type', 'name', 'value', 'variable')


class StateVariableSerializer(serializers.ModelSerializer):

    ranges = VariableRangeSerializer(many=True)
    # artifact = ArtifactSerializer()

    class Meta:
        model = StateVariable
        fields = ('id', 'name', 'artifact', 'type', 'typeUI', 'value', 'min', 'max', 'scale', 'ranges')

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
        ret.change_variable(ret.artifact.on, ret.artifact.id, ret.value)
        return ret


class ArtifactSerializer(serializers.ModelSerializer):
    variables = StateVariableSerializer(many=True)

    class Meta:
        model = Artifact
        fields = ('id', 'zone', 'type', 'name', 'intermediary', 'connector', 'on', 'variables')


class SceneActionsSerializer(serializers.ModelSerializer):
    id_aux = serializers.IntegerField(required=False, allow_null=True)
    zone_id = serializers.PrimaryKeyRelatedField(
        queryset=Zone.objects.all(),
        required=False,
        source='zone',
    )
    artifact_id = serializers.PrimaryKeyRelatedField(
        queryset=Artifact.objects.all(),
        allow_null=True,
        required=False,
        source='artifact',
    )

    zone = ZoneSerializer(
        read_only=False,
        required=False,
        allow_null=True,
    )
    artifact = ArtifactSerializer(
        required=False,
        allow_null=True,
        read_only=True,
    )

    class Meta:
        model = SceneActions
        fields = ('id', 'id_aux', 'variable', 'value', 'artifact', 'zone', 'artifact_id', 'zone_id')
        depth = 1

    def create(self, validated_data):
        super(SceneActionsSerializer, self).create(validated_data)

    """"
    def update(self, instance, validated_data):
        # id_aux = instance['variable'].id
        # mod_action = User.objects.filter(id=id_aux).first()
        # a_id = validated_data['variable'].id
        a = SceneActions.objects.filter(id=validated_data['id_aux']).first()
        if not a:
            a_id = 0
            del validated_data['id_aux']
            ret = super(SceneActionsSerializer, self).create(validated_data)
            return ret
        else:
            del validated_data['id_aux']
            ret = super(SceneActionsSerializer, self).update(instance, validated_data)
            return ret
    """

    def __delete__(self, data):
        # id_aux = data['variable'].id
        to_del = SceneActions.objects.filter(id=data.id_aux).first()
        to_del.delete()
        return True


class SceneSerializer(serializers.ModelSerializer):
    actions = SceneActionsSerializer(many=True)

    class Meta:
        model = Scene
        fields = ('id', 'name', 'description', 'time_condition', 'time', 'on_demand', 'days', 'actions')
        depth = 1

    def create(self, validated_data):
        actions = validated_data['actions']
        del validated_data['actions']
        ret = super(SceneSerializer, self).create(validated_data)
        action_serializer = SceneActionsSerializer()
        for action in actions:
            action['scene'] = ret
            action_serializer.create(action)
        return ret

    def update(self, instance, validated_data):
        actions = validated_data['actions']
        del validated_data['actions']
        action_serializer = SceneActionsSerializer()
        scene_aux = Scene.objects.filter(id=instance.id).first()
        Main.delete_actions(instance.id)
        for action in actions:
            # mod_action = SceneActions.objects.filter(id=action['id_aux']).first()
            action['scene'] = scene_aux
            action_serializer.create(action)
        ret = super(SceneSerializer, self).update(scene_aux, validated_data)
        return ret


class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = ('id', 'name', 'value')
