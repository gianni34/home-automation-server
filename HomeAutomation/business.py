# Aca tengo que refactorizar todos los metodos que tengo dispersos por clases incorrectas
# y ponerlos aca como logica de negocio

from HomeAutomation.models import *
import datetime


class Main:
    @staticmethod
    def is_execution_day(i):
        string_days = Scene.objects.filter(id=i).first()
        days = string_days.split(',')
        for d in days:
            if d == datetime.datetime.now().weekday():
                return True
        return False

    @staticmethod
    def auto_execution_scene():
        scenes = Scene.objects.all()
        for s in scenes:
            if s.time_condition:
                if Main.is_execution_day(s.id):
                    if s.time == datetime.datetime.now().time():
                        Scene.execute_scene()

    @staticmethod
    def delete_actions(i):
        actions = SceneActions.objects.filter(scene=i).all()
        if actions:
            for a in actions:
                SceneActions.delete(a)
