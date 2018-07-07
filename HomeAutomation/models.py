from django.db import models
from HomeAutomation.SSHConnection import Connection
from HomeAutomation.validators import VariableValidations


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


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)

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


class Artifact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)
    type = models.ForeignKey(ArtifactType, on_delete=models.DO_NOTHING)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING, null=True)
    intermediary = models.ForeignKey(Intermediary, on_delete=models.DO_NOTHING, null=True)
    power = models.BooleanField(default=False)
    pin = models.IntegerField(null=True)

    def __str__(self):
        return self.name + "(" + self.zone.name + ")"

    def turn_on(self):
        self.power = True
        params = Parameters()
        method_name = params.get_change_v_method()
        command = method_name + "(" + str(self.pin) + "," + str(1) + ")"
        script = params.get_script_name()
        Connection.execute_script(script, command)
        self.save(update_fields=['power'])

    def turn_off(self):
        self.power = False
        params = Parameters()
        method_name = params.get_change_v_method()
        command = method_name + "(" + str(self.pin) + "," + str(0) + ")"
        script = params.get_script_name()
        Connection.execute_script(script, command)
        self.save(update_fields=['power'])


class StateVariable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)
    artifact = models.ForeignKey(Artifact, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=50, null=True)
    typeUI = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50, null=True)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=1)
    scale = models.IntegerField(default=1)

    def change_variable(self, power, artifact, value):
        a = Artifact.objects.filter(id=artifact).first()
        variable = self.id
        if not power:
            Artifact.turn_off(a)
        else:
            validate = VariableValidations.value_validation(variable, value)
            if validate[0]:
                self.value = value
                pin = a.pin
                params = Parameters()
                method_name = params.get_change_v_method()
                # ver si tengo que cambiar el valor por otro valor para que onion lo entienda
                command = method_name + "(" + str(pin) + "," + value + ")"
                script = params.get_script_name()
                Connection.execute_script(script, command)
                a.save()
                self.save()
            else:
                return validate[1]


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=False)
    question = models.CharField(max_length=100, unique=False, null=False)
    answer = models.CharField(max_length=100, unique=False, null=False)
    password = models.CharField(max_length=100, unique=False, null=False)

    def change_password(self, old_password, new_password):
        if not old_password == self.password:
            raise ValueError('La contraseña vieja no coincide')
        else:
            self.password = new_password
            self.save()
            return 'OK'

    def login(self, password):

        if self.password == password:
            return True
        else:
            return False

    def check_answer(self, answer):

        if self.answer == answer:
            return True
        else:
            return False

    def is_admin(self):
        if self.role.name == 'Administrador':
            return True
        else:
            return False

    def __str__(self):
        return self.name + '(' + self.role.name + ')'


class Scene(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.CharField(max_length=200, unique=False, null=False)
    end_time = models.DateTimeField(null=True)
    initial_time = models.DateTimeField(null=True)
    frequency = models.CharField(max_length=20, unique=False, null=False)
    on_demand = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SceneActions(models.Model):
    id = models.AutoField(primary_key=True)
    variable = models.ForeignKey(StateVariable, on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=50, null=False)
    scene = models.ForeignKey(Scene, on_delete=models.DO_NOTHING, related_name='actions')
