from datetime import datetime
import math

class UserInputs:

    def inputPrompt (self, what, parameters, skips):
        initialPrompt = '\nElija de la siguiente lista la opción para -' + what + '- que desea utilizar: \n'
        optionsPrompt = ''
        l = 0
        while l < len(parameters):
            parameter = parameters[l]
            l += skips
            optionsPrompt += '\n' + str(int(l / skips)) + '-' + parameter
        optionsPrompt += '\n\n---> Respuesta: '

        while True:
            selection = input(initialPrompt + optionsPrompt)
            if selection not in parameters:
                print('Valor no aceptado! Intente de nuevo..\n')
                continue
            else: break
        return selection 

    def inputFecha (self, what):
        while True:
            try:
                fecha = datetime.strptime(input('\nDigite la fecha ' + what + ' en formato yyyy-mm-dd: '),'%Y/%m/%d')
            except ValueError:
                print('Esta fecha es incompatible con los parámetros. Digitar en manera yyyy-mm-dd')
                continue
            f = 'Fecha ingresada: ' + str(fecha.day) + ' de ' + str(self.seleccionMes(fecha.month)) + ' del ' + str(fecha.year)
            while True:
                confirmacion = input('\n' + f + '. Es correcto? \n1-si \n2-no \nRespuesta: ')
                if confirmacion not in ['si', '1', 'no', '2']:
                    print('Opción no válida, intente de nuevo..')
                    continue
                else: break
            if confirmacion != 'si' and confirmacion != '1':
                print('Confirmación negada, intente de nuevo..')
                continue
            break
        return fecha

    def pbsInput(self):    
        while True:
            try:
                bps = int(input('\nIntroduzca cantidad de puntos básicos (ej.: 100, 200): '))
            except ValueError:
                print('Valor inválido, inténtelo de nuevo..')
                continue
            if bps < 0:
                print('Este valor no puede ser negativo, inténtelo de nuevo..')
            else: break
        return bps

    def inputMonto(self, default):
        amount = input('\nIntroduzca el Valor Nominal (en blanco valor predeterminado es ' + f"{default:,.2f}" + '):')
        if amount == '':
            amount = float(default)
        else: amount = float(amount)
        return amount

    def emisorPrompt(self):
        while True:
            seleccion = input('\nEmisor especial: sólo aplica para el Ministerio de Hacienda (en blanco -no- predeterminado) \n1-si \n2-no \n3-info \nRespuesta: ')
            if seleccion == '':
                seleccion = 'Otros Emisores'
                break
            else:
                if seleccion in ['si','1','no','2','info','3']:
                    if seleccion == 'info' or seleccion == '3':
                        print('\nNota: \n*Esto se debe a que el Ministerio tiene una forma de cálculo diferente para el valor presente..')
                        continue
                    elif seleccion == 'si' or seleccion == '1':
                        seleccion = 'Hacienda'
                        break
                    else: 
                        seleccion = 'Otros Emisores'
                        break
                else: continue
        return seleccion

    def inputIntegers(self):
        while True:
            try:
                cantidad = int(input('\nIngrese la cantidad de amortizaciones que desee realizar: '))
            except ValueError:
                print('valor no aceptado, verifique si ha digitado un número...')
                continue
            if cantidad <= 0:
                print('valor no aceptado, debe ser mayor que 0...')
                continue
            else: break
        return cantidad

    def fwdPrompt(self, fechaVencimiento, años):
        while True: 
            tipo_cupones = self.inputPrompt('forma de inicio de pago de cupones', ['normal','1','FW1','2','FW2','3','FW3','4', 'info', '5'], 2)
            if tipo_cupones == 'normal' or tipo_cupones == '1':
                forward_date = None
                break
            elif (tipo_cupones == 'FW1' or tipo_cupones == '2') or (tipo_cupones == 'FW2' or tipo_cupones == '3'):
                forward_date = datetime(fechaVencimiento.year - math.trunc(años),fechaVencimiento.month,fechaVencimiento.day,0,0)
                break
            elif (tipo_cupones == 'FW3' or tipo_cupones == '4'):
                forward_date = self.inputFecha('forward')
                break
            elif (tipo_cupones == 'info' or tipo_cupones == '5'):
                print('\nNotas: \n-normal: Los pagos son regulares'
                        + '\n-FW1: Acumula los intereses hasta el próximo pago de cupón, es decir 6 meses después de un primer pago teórico.'
                        + '\n-FW2: Paga los intereses en un primer periodo desde la fecha de emisión hasta el primer pago de cupón teórico, esto resulta en un pago adicional.'
                        + '\n-FW3: Se introduce una fecha deseada, acumulando los intereses hasta que se normalice el pago de cupones.')
                continue
        return tipo_cupones, forward_date

    def seleccionMes(self, mes):
        if mes == 1:
            return 'enero'
        if mes == 2:
            return 'febrero'
        if mes == 3:
            return 'marzo'
        if mes == 4:
            return 'abril'
        if mes == 5:
            return 'mayo'
        if mes == 6:
            return 'junio'
        if mes == 7:
            return 'julio'
        if mes == 8:
            return 'agosto'
        if mes == 9:
            return 'septiembre'
        if mes == 10:
            return 'octubre'
        if mes == 11:
            return 'noviembre'
        if mes == 12:
            return 'diciembre'