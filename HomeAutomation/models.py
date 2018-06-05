from django.db import models
from polymorphic.models import PolymorphicModel
from HomeAutomation.SSHConnection import Connection


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
    onoff = models.BooleanField(default=False)
    pin = models.IntegerField(null=True)

    def __str__(self):
        return self.name + "(" + self.zone.name + ")"


"""def change_state(self, state):
        if state == 'Prendido':
            value = 1
        elif state == "Apagado":
            value = 0

        e = State.objects.filter(name=state).first()
        self.state = e
        command = "cambiarEstado(" + str(self.pin) + "," + str(value) + ")"
        Connection.execute_script("funciones.py", command)
        self.save()
    """


class StateVariable(PolymorphicModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    artifact = models.ForeignKey(Artifact, on_delete=models.DO_NOTHING, null=True)
    value = models.IntegerField()

    class Meta:
        abstract = True

    def change_variable(self, id, artifact, variable, value):
        if type == "onoff":
            a = Artifact.objects.filter(artifact=artifact).first()
            a.onoff = True
            a.save(update_fields=['onoff'])
        else:
            if variable == "Range":
                v = RangeVariable.objects.filter(id=variable).first()
                if v.min >= value <= v.max:
                    #Comparar con la escala
                    self.value = value
                    a = Artifact.objects.filter(artifact=artifact).first()
                    pin = a.pin
                    command = "cambiarEstado(" + str(pin) + "," + str(value) + ")"
                    Connection.execute_script("funciones.py", command)
                    self.save()
                else:
                    #error
                    return
            elif variable == "Boolean":
                v = BooleanVariable.objects.filter(id=variable).first()
                v.bool = value
                a = Artifact.objects.filter(artifact=artifact).first()
                pin = a.pin
                if value:
                    command = "cambiarEstado(" + str(pin) + "," + str(1) + ")"
                    Connection.execute_script("funciones.py", command)
                else:
                    command = "cambiarEstado(" + str(pin) + "," + str(0) + ")"
                    Connection.execute_script("funciones.py", command)
                self.save()


class RangeVariable(StateVariable):
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=1)
    scale = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class BooleanVariable(StateVariable):
    bool = models.BooleanField()

    def __str__(self):
        return self.name


class ValueVariable(StateVariable):
    values = {}

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=False, null=False)
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
