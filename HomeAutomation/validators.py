from HomeAutomation.models import *
import decimal


class VariableValidations:

    def __init__(self):
        return

    @staticmethod
    def d_range(x, y, jump):
        while x < y:
            yield x
            x += decimal.Decimal(jump)

    def value_validation(self, variable, value):
        if value < variable.min or value > variable.max:
            return {'result': False, 'message': "El valor pasado no pertenece al rango de la variable."}
        else:
            values = self.d_range(variable.min, variable.max, variable.scale)
            for i in values:
                if i == value:
                    return {'result': True, 'message': ""}
            return {'result': False, 'message': "El valor pasado, no contiene una precision correcta."}

    @staticmethod
    def parse_raw_to_array(raw_code):
        codes = raw_code.split(',')
        int_codes = list(map(int, codes))
        return int_codes
