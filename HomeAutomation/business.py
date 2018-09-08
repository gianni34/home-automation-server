# Aca tengo que refactorizar todos los metodos que tengo dispersos por clases incorrectas
# y ponerlos aca como logica de negocio
import time
from HomeAutomation.models import *


def auto_execution_scene():
    scenes = Scene.objects.all()
    for s in scenes:
        if s.automatica:
            if s.hora == time.clock():
                Scene.execute_scene()


