from HomeAutomation.models import *
import decimal


class VariableValidations:

    @staticmethod
    def d_range(x, y, jump):
        while x < y:
            yield x
            x += decimal.Decimal(jump)

    def value_validation(self, variable, value):
        var = StateVariable.objects.filter(id=variable).first()
        if var.min > value > var.max:
            return False, "El valor pasado no pertenece al rango de la variable"
        else:
            values = self.d_range(var.min, var.max, var.scale)
            for i in values:
                if i == value:
                    return True, ""
            return False, "El valor pasado, no contiene una precision correcta."
