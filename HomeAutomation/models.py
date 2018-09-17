from django.db import models
from HomeAutomation.SSHConnection import Connection
from HomeAutomation.validators import VariableValidations
from HomeAutomation.exceptions import *
# import requests
import time
import sys


class Parameters(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    value = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name

    def get_change_v_method(self):
        reg = self.objects.filter(name="changeVariable").first()
        return reg.value

    def get_script_name(self):
        reg = self.objects.filter(name="script").first()
        return reg.value


class ArtifactType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name

    # def __eq__(self, other):
    #   return self.name == other.name


class SSHConfig(models.Model):
    id = models.AutoField(primary_key=True)
    artifactType = models.OneToOneField(ArtifactType, on_delete=models.DO_NOTHING, blank=False, null=False)
    script = models.CharField(max_length=100, null=False)
    method = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.script + ' - ' + self.method


class WSConfig(models.Model):
    id = models.AutoField(primary_key=True)
    artifactType = models.OneToOneField(ArtifactType, on_delete=models.DO_NOTHING, blank=False, null=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Intermediary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, null=False)
    ip = models.CharField(max_length=20, unique=True, null=False)
    user = models.CharField(max_length=40, unique=False, null=False)
    password = models.CharField(max_length=40, unique=False, null=False)

    def __str__(self):
        return self.name + ' -  IP: ' + self.ip


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    type = models.CharField(max_length=40, unique=False, null=True)
    pin = models.IntegerField(null=True)
    intermediary = models.ForeignKey(Intermediary, on_delete=models.DO_NOTHING, blank=True, null=True)
    temperature = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def set_temperature(self, value):
        self.temperature = value
        self.save(update_fields=['temperature'])


class Artifact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)
    type = models.ForeignKey(ArtifactType, on_delete=models.DO_NOTHING)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING, null=True)
    intermediary = models.ForeignKey(Intermediary, on_delete=models.DO_NOTHING, null=True)
    on = models.BooleanField(default=False)
    connector = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name + "(" + self.zone.name + ")"

    def change_power(self, power):
        self.on = power
        # params = Parameters()
        # method_name = params.get_change_v_method()
        ssh = SSHConfig.objects.filter(artifactType=self.type.id).first()
        if ssh:
            command = ssh.method + "(" + str(self.connector) + ", " + power + ")"
            print(command, self.intermediary.name, self.intermediary.user, self.intermediary.password, ssh.script)
            try:
                Connection.execute_script(self.intermediary.name, self.intermediary.user, self.intermediary.password, ssh.script, command)
            except:
                print(sys.exc_info())
                raise ConnectionExc()
            self.save(update_fields=['on'])
            return True
        ws = WSConfig.objects.filter(artifactType=self.type.id).first()
        if ws:
            url = 'http://' + self.intermediary.name + '/' + ws.name
            print(url)
            if self.type.name == 'AC' and power == '1':
                variables = StateVariable.objects.filter(artifact=self.id)
                code = ''
                for v in variables:
                    print(v)
                    code += '#' + v.value if len(code) > 0 else v.value
                print(code)
            else:
                code = '0'
            # cuando no es un AC, o es un off que se manda un cero:
            try:
                req = requests.put(url, json={'value': code})
                print(req.text)
            except:
                raise ConnectionExc()
            self.save(update_fields=['on'])
            return True
            # consumir ws.. etc
        raise ConfigurationExc()

    def is_on(self):
        return self.on


class StateVariable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)
    artifact = models.ForeignKey(Artifact, on_delete=models.DO_NOTHING, related_name='variables')
    type = models.CharField(max_length=50, null=True)
    typeUI = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50, null=True)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=1)
    scale = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def change_variable(self, value):
        # a = Artifact.objects.filter(id=self.artifact).first()
        value = int(value)
        validator = VariableValidations()
        try:
            validator.value_validation(self,  value)
        except:
            raise ValidationExc()

        self.value = value
        ssh = SSHConfig.objects.filter(artifactType=self.artifact.type.id).first()
        if ssh:
            command = ssh.method + "(" + str(self.artifact.connector) + "," + value + ")"
            try:
                Connection.execute_script(self.artifact.intermediary.name, self.artifact.intermediary.user,
                                          self.artifact.intermediary.password, ssh.script, command)
            except:
                raise ConnectionExc()
            self.save(update_fields=['value'])
            return True

        ws = WSConfig.objects.filter(artifactType=self.artifact.type.id).first()
        if ws:
            url = 'http://' + self.artifact.intermediary.name + '/' + ws.name
            code = value
            print(url)
            if self.artifact.type.name == 'AC':
                variables = StateVariable.objects.filter(artifact=self.artifact.id)
                code = ''
                for v in variables:
                    print(v)
                    if v.id == self.id:
                        code += '#' + str(value) if len(code) > 0 else str(value)
                    else:
                        code += '#' + str(v.value) if len(code) > 0 else str(v.value)
                print(code)
            try:
                req = requests.put(url, json={'value': code})
                print(req.text)
            except:
                raise ConnectionExc()
            self.save(update_fields=['value'])
            return True
        raise ConfigurationExc()


class VariableRange(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)
    type = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50, default=0, null=False)
    variable = models.ForeignKey(StateVariable, on_delete=models.DO_NOTHING, null=False, related_name='ranges')

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    # role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=False)
    question = models.CharField(max_length=100, unique=False, null=True)
    answer = models.CharField(max_length=100, unique=False, null=True)
    password = models.CharField(max_length=100, unique=False, null=False)
    isAdmin = models.BooleanField(null=False, default=False)

    def verify_old_password(self, old_password):
        return old_password == self.password

    def login(self, password):
        return self.password == password

    def check_answer(self, answer):
        return self.answer == answer

    def is_admin(self):
        return self.isAdmin

    def get_question(self):
        return self.question

    def get_question(self):
        return self.question

    def change_password(self, new_password):
        self.password = new_password
        return True

    def __str__(self):
        return self.name


class Scene(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.CharField(max_length=200, null=False)
    on_demand = models.BooleanField(default=False)
    time_condition = models.BooleanField(default=False)
    time = models.TimeField(null=True, blank=True)
    days = models.CharField(max_length=20, blank=True, null=True)
    value_condition = models.BooleanField(default=False)
    value = models.CharField(max_length=30, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def execute_scene(self):
        print("entroooooooo")
        actions = SceneActions.objects.filter(scene=self.id).all()
        print(actions)
        for action in actions:
            value = action.value
            print("valor: ", value)
            if action.variable == 0:
                action.artifact.change_power(value)
            else:
                action.variable.change_variable(value)
            time.sleep(1)
        return True


class SceneActions(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    artifact = models.ForeignKey(Artifact, on_delete=models.DO_NOTHING)
    variable = models.IntegerField(default=0)
    # ForeignKey(StateVariable, on_delete=models.DO_NOTHING, default=0, null=False)
    value = models.CharField(max_length=50, null=False)
    scene = models.ForeignKey(Scene, on_delete=models.DO_NOTHING, related_name='actions')

