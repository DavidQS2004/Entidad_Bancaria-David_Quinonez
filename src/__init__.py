import os

def limpiar_terminal():
    os.system("cls")

limpiar_terminal()

from abc import ABC, abstractmethod
from datetime import datetime


#Clase abstracta
class CuentaBancaria(ABC):

    def __init__(self, numero_cuenta, titular, saldo_inicial=0):
        self.__numero_cuenta = numero_cuenta
        self.__titular = titular
        # Encapsulamiento para saldo privado y datos en general.
        self.__saldo = saldo_inicial
        self.__fecha_apertura = datetime.now()
        # Atributo protegido
        self._historial_movimientos = []
        # Simulación de firma digital para transacciones protegidas
        self._firma_digital = hash(f"{self.__numero_cuenta}{self.__titular}")

    @abstractmethod
    def calcular_interes_mensual(self):
        pass

    @abstractmethod
    def calcular_comision_mantenimiento(self):
        pass

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            self._historial_movimientos.append((datetime.now(), "Depósito", monto, self.__saldo))
            return f"Depósito de ${monto:.2f} realizado con éxito."
        return "El monto del depósito debe ser positivo."

    def retirar(self, monto):
        if self.__validar_fondos_suficientes(monto):
            self.__saldo -= monto
            self._historial_movimientos.append((datetime.now(), "Retiro", -monto, self.__saldo))
            return f"Retiro de ${monto:.2f} realizado con éxito."
        return "Fondos insuficientes o monto no válido."

    # Encapsulamiento
    def __validar_fondos_suficientes(self, monto):
        if self._firma_digital and monto > 0 and self.__saldo >= monto:
            return True
        return False

    @property
    def saldo(self):
        return self.__saldo

    @property
    def numero_cuenta(self):
        return self.__numero_cuenta

    def generar_estado_cuenta_mensual(self):
        interes = self.calcular_interes_mensual()
        comision = self.calcular_comision_mantenimiento()
        print("-" * 50)
        print(f"ESTADO DE CUENTA MENSUAL - {type(self).__name__}")
        print(f"Titular: {self.__titular} | Cuenta #: {self.__numero_cuenta}")
        print(f"Saldo Inicial Mes: ${self.saldo:.2f}")
        print(f"Intereses Ganados: ${interes:.2f}")
        print(f"Comisiones Cobradas: ${comision:.2f}")


        self.__saldo += interes
        self.__saldo -= comision

        self._historial_movimientos.append((datetime.now(), "Ajuste Intereses", interes, self.__saldo))
        self._historial_movimientos.append((datetime.now(), "Ajuste Comisión", -comision, self.__saldo))

        print(f"Saldo Final Mes: ${self.saldo:.2f}")
        print("\n--- Historial de Movimientos Recientes ---")
        for mov in self._historial_movimientos[-5:]:#Muestra los ultimos 5 movimientos.
            print(
                f"  {mov[0].strftime('%Y-%m-%d %H:%M')} | {mov[1]:<15} | Monto: ${mov[2]:8.2f} | Saldo: ${mov[3]:.2f}")
        print("-" * 50)


#Herencia y polimorfismo
class CuentaAhorro(CuentaBancaria):

    def __init__(self, numero_cuenta, titular, saldo_inicial, tasa_interes, retiros_gratis_mes, saldo_minimo):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.tasa_interes = tasa_interes  # Ej: 0.02 (2%)
        self.retiros_gratis_mes = retiros_gratis_mes
        self.saldo_minimo = saldo_minimo
        self._contador_retiros = 0
        self.comision_por_retiro_extra = 5.0

    def calcular_interes_mensual(self):
        # El interés se calcula sobre el saldo actual
        return self.saldo * self.tasa_interes

    def calcular_comision_mantenimiento(self):
        return 0.0

    def retirar(self, monto):
        if self._contador_retiros < self.retiros_gratis_mes:
            resultado = super().retirar(monto)
            if "éxito" in resultado:
                self._contador_retiros += 1
            return resultado
        else:
            monto_total = monto + self.comision_por_retiro_extra
            if super()._CuentaBancaria__validar_fondos_suficientes(monto_total):
                super().retirar(monto_total)  # Retira el monto solicitado + la comisión
                self._historial_movimientos.append(
                    (datetime.now(), "Comisión Retiro Extra", -self.comision_por_retiro_extra, self.saldo))
                return f"Retiro de ${monto:.2f} (+$5.00 comisión) realizado con éxito. Retiros gratis agotados."
            return "Fondos insuficientes para cubrir retiro y comisión extra."


class CuentaCorriente(CuentaBancaria):

    def __init__(self, numero_cuenta, titular, saldo_inicial, sobregiro_permitido, chequera):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.sobregiro_permitido = sobregiro_permitido
        self.chequera = chequera
        self.comision_alta = 15.0  # Comisión fija mensual

    def calcular_interes_mensual(self):
        return 0.0

    def calcular_comision_mantenimiento(self):
        return self.comision_alta

    def retirar(self, monto):
        if (self.saldo - monto) >= -self.sobregiro_permitido:
            super()._CuentaBancaria__saldo -= monto
            self._historial_movimientos.append((datetime.now(), "Retiro", -monto, self.saldo))
            return f"Retiro de ${monto:.2f} realizado con éxito. Saldo actual: ${self.saldo:.2f}"
        return f"Retiro excede el límite de sobregiro permitido (${self.sobregiro_permitido:.2f})."


class CuentaInversion(CuentaBancaria):

    def __init__(self, numero_cuenta, titular, saldo_inicial, plazo_meses, tasa_preferencial):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.plazo_meses = plazo_meses
        self.tasa_preferencial = tasa_preferencial
        self.penalidad_retiro = 0.10  # 10% de penalidad si se retira antes de plazo

    def calcular_interes_mensual(self):
        return self.saldo * self.tasa_preferencial

    def calcular_comision_mantenimiento(self):
        return 0.0

    def retirar(self, monto):
        print("Penalidad del 10% aplicada por retiro anticipado simulado.")
        penalidad = monto * self.penalidad_retiro
        monto_total = monto + penalidad
        if super()._CuentaBancaria__validar_fondos_suficientes(monto_total):
            super().retirar(monto_total)
            self._historial_movimientos.append((datetime.now(), "Penalidad Retiro", -penalidad, self.saldo))
            return f"Retiro de ${monto:.2f} realizado con éxito (Penalidad: ${penalidad:.2f})."
        return "Fondos insuficientes para retiro y penalidad."


class CuentaNomina(CuentaBancaria):

    def __init__(self, numero_cuenta, titular, saldo_inicial, empresa):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.empresa = empresa
        self.deposito_automatico = True

    def calcular_interes_mensual(self):
        # Tasa de interés baja para cuentas nómina (1%)
        return self.saldo * 0.01

    def calcular_comision_mantenimiento(self):
        # Sin comisiones (restricción del tipo de cuenta)
        return 0.0


#Simulacion de cuentas
print("Inicializando Cuentas")

cuentas = []

cta_ahorro1 = CuentaAhorro("A1001", "Ana Lopez", 1200.00, tasa_interes=0.02, retiros_gratis_mes=3, saldo_minimo=100.00)
cta_ahorro2 = CuentaAhorro("A1002", "Pedro Martinez", 50.00, tasa_interes=0.02, retiros_gratis_mes=3,
                           saldo_minimo=100.00)

cta_corriente1 = CuentaCorriente("C2001", "Carlos Ruiz", 500.00, sobregiro_permitido=1000.00, chequera=True)
cta_corriente2 = CuentaCorriente("C2002", "Maria Garcia", -200.00, sobregiro_permitido=500.00, chequera=False)

cta_inversion1 = CuentaInversion("I3001", "Javier Perez", 10000.00, plazo_meses=12, tasa_preferencial=0.05)
cta_inversion2 = CuentaInversion("I3002", "Luisa Hernandez", 2000.00, plazo_meses=6, tasa_preferencial=0.04)

cta_nomina1 = CuentaNomina("N4001", "Roberto Jimenez", 800.00, empresa="TechCorp")
cta_nomina2 = CuentaNomina("N4002", "Sofia Castro", 1500.00, empresa="RetailInc")

cuentas.extend([cta_ahorro1, cta_ahorro2, cta_corriente1, cta_corriente2,
                cta_inversion1, cta_inversion2, cta_nomina1, cta_nomina2])

print("\nSimulación de Operaciones")

# Simular depósitos y retiros
print(cta_ahorro1.depositar(200.00))
print(cta_ahorro1.retirar(50.00))  # Retiro gratis 1/3
print(cta_ahorro1.retirar(50.00))  # Retiro gratis 2/3
print(cta_ahorro1.retirar(50.00))  # Retiro gratis 3/3
print(cta_ahorro1.retirar(50.00))  # Retiro con comisión extra


print(cta_corriente2.retirar(400.00))  # Supera el sobregiro permitido

print(cta_inversion1.retirar(1000.00))  # Aplica penalidad

print(cta_nomina1.depositar(2500.00))  # Depósito de nómina

# Estado mensual de cuenta

print("\nReporte Mensual General (Polimorfismo)")

for cuenta in cuentas:
    cuenta.generar_estado_cuenta_mensual()

import os
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

def limpiar_terminal():
    os.system("cls")

limpiar_terminal()
# Clase abstracta
class Transaccion(ABC):

    def __init__(self, monto, cuenta_origen):
        self.__id_transaccion = str(uuid.uuid4())
        self.__fecha = datetime.now()
        self.__monto = monto
        self.__cuenta_origen = cuenta_origen
        # Atributo protegido con log de cambios para el encapsulamiento
        self._estado = "pendiente"
        self.__log_estado = [("creada", self.__fecha)]
        self.__datos_sensibles_encriptados = f"ENCRYPTED_{self.__cuenta_origen}"

    @abstractmethod
    def procesar(self):
        """Método abstracto que define el flujo de procesamiento."""
        pass

    @abstractmethod
    def calcular_comision(self):
        """Método abstracto para calcular la comisión específica."""
        pass

    def generar_comprobante(self):
        """Método concreto para generar un resumen de la transacción."""
        comision = self.calcular_comision()
        total_cargo = self.__monto + comision
        return (f"COMPROBANTE DE TRANSACCION\n"
                f"ID: {self.__id_transaccion}\n"
                f"Fecha: {self.__fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Tipo: {self.__class__.__name__}\n"
                f"Cuenta Origen (encriptada): {self.__datos_sensibles_encriptados}\n"
                f"Monto: ${self.__monto:.2f}\n"
                f"Comisión: ${comision:.2f}\n"
                f"Total Cargado: ${total_cargo:.2f}\n"
                f"Estado: {self._estado.upper()}\n"
                f"------------------------------------")

    # Encapsulamiento

    def _actualizar_estado(self, nuevo_estado):
        self._estado = nuevo_estado
        self.__log_estado.append((nuevo_estado, datetime.now()))
        print(f"[LOG] ID {self.__id_transaccion[:8]} -> Nuevo estado: {nuevo_estado}")

    def __validar_seguridad(self):
        # Simulación de validación
        return True

    @property
    def monto(self):
        return self.__monto

    @property
    def estado(self):
        return self._estado


# Herencia y Polimorfismo

class Transferencia(Transaccion):
    def __init__(self, monto, cuenta_origen, cuenta_destino, banco_destino, tipo):
        super().__init__(monto, cuenta_origen)
        self.cuenta_destino = cuenta_destino
        self.banco_destino = banco_destino
        self.tipo = tipo  # interna - externa

    def calcular_comision(self):
        if self.tipo == 'interna':
            return 1.00
        elif self.tipo == 'externa':
            return 5.00
        else:
            return 0.00

    def procesar(self):
        print(f"Procesando transferencia {self.tipo} de ${self.monto}...")
        if self._Transaccion__validar_seguridad():
            self._actualizar_estado("procesada")
            print("Transferencia completada exitosamente.")
        else:
            self._actualizar_estado("rechazada")
            print("Validación de seguridad fallida. Transferencia rechazada.")


class PagoServicio(Transaccion):
    def __init__(self, monto, cuenta_origen, empresa, codigo_servicio, fecha_vencimiento):
        super().__init__(monto, cuenta_origen)
        self.empresa = empresa
        self.codigo_servicio = codigo_servicio
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d')

    def calcular_comision(self):
        return 0.50

    def procesar(self):
        print(f"Procesando pago de servicio para {self.empresa} por ${self.monto}...")
        if datetime.now() > self.fecha_vencimiento:
            self._actualizar_estado("rechazada")
            print("Pago rechazado: La fecha de vencimiento ha pasado.")
        else:
            # Lógica de comunicación con el sistema de la empresa
            self._actualizar_estado("procesada")
            print("Pago de servicio aplicado correctamente.")


class RetiroATM(Transaccion):
    # se crea variable para simular el limite.
    LIMITE_DIARIO_GLOBAL = 1000.00

    def __init__(self, monto, cuenta_origen, cajero_ubicacion, comision_cajero):
        super().__init__(monto, cuenta_origen)
        self.cajero_ubicacion = cajero_ubicacion
        self.comision_cajero = comision_cajero
        self.limite_diario = RetiroATM.LIMITE_DIARIO_GLOBAL

    def calcular_comision(self):
        return 2.00 + self.comision_cajero

    def procesar(self):
        print(f"Procesando retiro ATM de ${self.monto} en {self.cajero_ubicacion}...")
        if self.monto > self.limite_diario:
            self._actualizar_estado("rechazada")
            print(f"Retiro rechazado: Excede el límite diario de ${self.limite_diario:.2f}.")
        else:
            # Lógica de dispensación de efectivo
            self._actualizar_estado("procesada")
            print("Efectivo dispensado. Retiro completado.")


class Cheque(Transaccion):
    def __init__(self, monto, cuenta_origen, numero_cheque, beneficiario, fecha_emision, fecha_cobro):
        super().__init__(monto, cuenta_origen)
        self.numero_cheque = numero_cheque
        self.beneficiario = beneficiario
        self.fecha_emision = datetime.strptime(fecha_emision, '%Y-%m-%d')
        self.fecha_cobro = datetime.strptime(fecha_cobro, '%Y-%m-%d')
        # Los cheques inician en un estado diferente
        self._actualizar_estado("emitido")

    def calcular_comision(self):
        return 0.00

    def procesar(self):
        print(f"Procesando cobro de cheque #{self.numero_cheque} por ${self.monto}...")
        if self.fecha_cobro > datetime.now():
            self._actualizar_estado("pendiente_cobro")
            print("Cheque a fecha futura, se registrará pero no se cobrará hoy.")
        elif self.estado == "procesada":
            self._actualizar_estado("rechazada")
            print("Cheque ya fue cobrado anteriormente (duplicado).")
        else:
            # Lógica de verificación de fondos y compensación bancaria
            self._actualizar_estado("procesada")
            print("Cheque cobrado y fondos transferidos al beneficiario.")


# Ejecucion del programa

if __name__ == "__main__":

    print("1. Creación y Simulación de Transacciones (3 de cada tipo) ---")

    # Ejemplo de polimorfismo
    transacciones_del_dia = []

    # cuentas para simulacion

    # 3 Transferencias
    t1 = Transferencia(100.00, "CC123456", "CA987654", "Banco B", "externa")
    t2 = Transferencia(500.00, "CA654321", "CC112233", "Banco A", "interna")
    t3 = Transferencia(50.00, "CC123456", "CA445566", "Banco C", "externa")

    # 3 Pagos de Servicio (uno vencido para mostrar rechazo)
    p1 = PagoServicio(85.50, "CA654321", "Luz SA", "10101", "2025-12-01")  # Futuro
    p2 = PagoServicio(30.00, "CC123456", "Agua MX", "20202", "2023-01-15")  # Pasado
    p3 = PagoServicio(120.00, "CA654321", "Internet Global", "30303", "2025-11-30")

    # 3 Retiros ATM
    a1 = RetiroATM(200.00, "CC123456", "ATM Lobby Principal", 0.50)  # $2.50 total com
    a2 = RetiroATM(1100.00, "CA654321", "ATM Sucursal A", 0.00)  # Excede límite
    a3 = RetiroATM(40.00, "CC123456", "ATM Tienda Express", 1.00)  # $3.00 total com

    # 3 Cheques
    c1 = Cheque(50.00, "CA654321", "001", "Pedro Perez", "2025-11-25", "2025-11-28")  # Cobro hoy
    c2 = Cheque(250.00, "CC123456", "002", "Maria Lopez", "2025-11-28", "2026-01-01")  # Cobro futuro
    c3 = Cheque(1000.00, "CA654321", "003", "Juan Garcia", "2025-11-20", "2025-11-28")  # Cobro hoy

    # Se agregan todos los objetos a la lista.
    transacciones_del_dia.extend([t1, t2, t3, p1, p2, p3, a1, a2, a3, c1, c2, c3])

    print("\n2. Procesamiento de Transacciones y Generación de Comprobantes")

    for transaccion in transacciones_del_dia:
        print(f"\nIniciando transacción tipo: {transaccion.__class__.__name__}")
        transaccion.procesar()  # Ejecución polimórfica del método procesar()
        print(transaccion.generar_comprobante())  # Uso del método concreto de la clase base

    print("\n3. Cálculo Total de Comisiones del Día")

    total_comisiones = 0.0
    for transaccion in transacciones_del_dia:
        if transaccion.estado == 'procesada' or transaccion.estado == 'pendiente_cobro':
            total_comisiones += transaccion.calcular_comision()

    print(f"\nEl total de comisiones cobradas por transacciones procesadas/pendientes hoy es: ${total_comisiones:.2f}")

import os

def limpiar_terminal():
    os.system("cls")

limpiar_terminal()

from abc import ABC, abstractmethod
from datetime import date

class Cliente(ABC):
    def __init__(self, nombre, cedula, fecha_registro, score_crediticio):
        self.__nombre = nombre
        self.__cedula = cedula
        self.__fecha_registro = fecha_registro
        self.__score_crediticio = score_crediticio
        self._cuentas = []
        self._historial_financiero = []
    @property
    def score_crediticio(self):
        return self.__score_crediticio

    @score_crediticio.setter
    def score_crediticio(self, nuevo_score):
        if 0 <= nuevo_score <= 1000:
            self.__score_crediticio = nuevo_score

    def __evaluar_riesgo(self):
        return "ALTO" if self.__score_crediticio < 500 else "BAJO"

    def agregar_cuenta(self, cuenta):
        self._cuentas.append(cuenta)

    @abstractmethod
    def calcular_limite_credito(self):
        pass

    @abstractmethod
    def obtener_beneficios(self):
        pass

class ClienteBasico(Cliente):
    def __init__(self, nombre, cedula, fecha_registro, score_crediticio,
                 ingresos_mensuales, primera_cuenta):
        super().__init__(nombre, cedula, fecha_registro, score_crediticio)
        self.ingresos_mensuales = ingresos_mensuales
        self.primera_cuenta = primera_cuenta

    def calcular_limite_credito(self):
        return 5000

    def obtener_beneficios(self):
        return ["Débito gratis", "Acceso a banca móvil"]

class ClientePreferencial(Cliente):
    def __init__(self, nombre, cedula, fecha_registro, score_crediticio,
                 años_cliente, saldo_promedio, asesor_asignado):
        super().__init__(nombre, cedula, fecha_registro, score_crediticio)
        self.años_cliente = años_cliente
        self.saldo_promedio = saldo_promedio
        self.asesor_asignado = asesor_asignado

    def calcular_limite_credito(self):
        return 20000

    def obtener_beneficios(self):
        return ["Tarjeta Gold", "Atención prioritaria", "Descuentos aliados"]

class ClienteEmpresarial(Cliente):
    def __init__(self, nombre, cedula, fecha_registro, score_crediticio,
                 razon_social, RUC, volumen_transacciones):
        super().__init__(nombre, cedula, fecha_registro, score_crediticio)
        self.razon_social = razon_social
        self.RUC = RUC
        self.volumen_transacciones = volumen_transacciones

    def calcular_limite_credito(self):
        return 100000

    def obtener_beneficios(self):
        return ["Cuenta empresarial", "Líneas de crédito", "Gestor comercial"]

class ClienteVIP(Cliente):
    def __init__(self, nombre, cedula, fecha_registro, score_crediticio,
                 patrimonio, gerente_exclusivo, productos_premium):
        super().__init__(nombre, cedula, fecha_registro, score_crediticio)
        self.patrimonio = patrimonio
        self.gerente_exclusivo = gerente_exclusivo
        self.productos_premium = productos_premium

    def calcular_limite_credito(self):
        return float("inf")

    def obtener_beneficios(self):
        return ["Tarjeta Black", "Salas VIP", "Inversiones exclusivas"]

class Credito(ABC):
    def __init__(self, numero_credito, monto, plazo_meses, tasa_interes):
        self.__numero_credito = numero_credito
        self.__monto = monto
        self.__plazo_meses = plazo_meses
        self.__tasa_interes = tasa_interes
        self._cuotas_pagadas = 0
        self._historial_pagos = []

    @property
    def monto(self):
        return self.__monto

    @property
    def plazo_meses(self):
        return self.__plazo_meses

    @property
    def tasa_interes(self):
        return self.__tasa_interes

    def pagar_cuota(self, monto):
        self._cuotas_pagadas += 1
        self._historial_pagos.append(monto)

    @abstractmethod
    def calcular_cuota_mensual(self):
        pass

    @abstractmethod
    def calcular_seguro(self):
        pass

class CreditoConsumo(Credito):
    def __init__(self, num, monto, plazo, tasa, proposito):
        super().__init__(num, monto, plazo, tasa)
        self.proposito = proposito

    def calcular_cuota_mensual(self):
        return (self.monto * (1 + self.tasa_interes)) / self.plazo_meses

    def calcular_seguro(self):
        return self.monto * 0.02

class CreditoHipotecario(Credito):
    def __init__(self, num, monto, plazo, tasa, valor_propiedad):
        super().__init__(num, monto, plazo, tasa)
        self.valor_propiedad = valor_propiedad

    def calcular_cuota_mensual(self):
        return (self.monto * (1 + 0.07)) / self.plazo_meses

    def calcular_seguro(self):
        return self.monto * 0.01

class CreditoVehicular(Credito):
    def __init__(self, num, monto, plazo, tasa, tipo_vehiculo, anio):
        super().__init__(num, monto, plazo, tasa)
        self.tipo_vehiculo = tipo_vehiculo
        self.anio = anio

    def calcular_cuota_mensual(self):
        return (self.monto * (1 + 0.05)) / self.plazo_meses

    def calcular_seguro(self):
        return self.monto * 0.01

class CreditoEmpresarial(Credito):
    def __init__(self, num, monto, plazo, tasa, plan_negocios):
        super().__init__(num, monto, plazo, tasa)
        self.plan_negocios = plan_negocios

    def calcular_cuota_mensual(self):
        return (self.monto * (1 + 0.03)) / self.plazo_meses

    def calcular_seguro(self):
        return self.monto * 0.005

clientes = [
    ClienteBasico("Ana", "111", date.today(), 650, 1200, True),
    ClienteBasico("Luis", "112", date.today(), 580, 1500, False),

    ClientePreferencial("María", "223", date.today(), 710, 5, 3000, "Oscar"),
    ClientePreferencial("Pedro", "224", date.today(), 800, 8, 4500, "Lucía"),

    ClienteEmpresarial("Comercial S.A.", "335", date.today(), 720, "Comercial", "09999", 50000),
    ClienteEmpresarial("TechCorp", "336", date.today(), 790, "TechCorp", "09998", 90000),

    ClienteVIP("Jorge", "448", date.today(), 900, 500000, "Andrés", ["Inversiones"]),
    ClienteVIP("Andrea", "449", date.today(), 950, 800000, "Marcos", ["Fondos Elite"])
]

print("LÍMITES DE CRÉDITO")
for c in clientes:
    print(c.__class__.__name__, "→", c.calcular_limite_credito())

print("\nBENEFICIOS")
for c in clientes:
    print(c.__class__.__name__, "→", c.obtener_beneficios())

creditos = [
    CreditoConsumo("C1", 5000, 12, 0.15, "Gastos personales"),
    CreditoConsumo("C2", 8000, 18, 0.18, "Viaje"),

    CreditoHipotecario("H1", 60000, 240, 0.08, 75000),
    CreditoHipotecario("H2", 90000, 240, 0.08, 110000),

    CreditoVehicular("V1", 15000, 48, 0.10, "SUV", 2022),
    CreditoVehicular("V2", 18000, 60, 0.10, "Sedán", 2023),

    CreditoEmpresarial("E1", 50000, 36, 0.07, "Plan A"),
    CreditoEmpresarial("E2", 100000, 60, 0.06, "Plan B"),
]

print("\nTABLA DE AMORTIZACIÓN")
for credito in creditos:
    cuota = credito.calcular_cuota_mensual()
    print(credito.__class__.__name__, credito.monto, "→ cuota:", round(cuota, 2))

print("\nCOSTO TOTAL")
for credito in creditos:
    total = credito.calcular_cuota_mensual() * 12 + credito.calcular_seguro()
    print(credito.__class__.__name__, "→", round(total, 2))

import os

def limpiar_terminal():
    os.system("cls")

limpiar_terminal()

from abc import ABC, abstractmethod

# CLASE ABSTRACTA CREDITO

class Credito(ABC):
    def __init__(self, numero_credito, monto, plazo_meses, tasa_interes):
        self.__numero_credito = numero_credito
        self.__monto = monto
        self.plazo_meses = plazo_meses
        self.tasa_interes = tasa_interes
        self._cuotas_pagadas = 0
        self.__historial_pagos = []

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, nuevo_monto):
        if nuevo_monto > 0:
            self.__monto = nuevo_monto

    def __calcular_interes_mora(self):
        return self.__monto * 0.01

    @abstractmethod
    def calcular_cuota_mensual(self):
        pass

    @abstractmethod
    def calcular_seguro(self):
        pass

    # MÉTODO CONCRETO

    def pagar_cuota(self):
        cuota = self.calcular_cuota_mensual()
        seguro = self.calcular_seguro()
        total_pago = cuota + seguro

        self._cuotas_pagadas += 1
        self.__historial_pagos.append(total_pago)

        self.__monto -= (cuota - self.tasa_interes * self.__monto)

        return total_pago

    def generar_tabla_amortizacion(self):
        saldo = self.__monto
        tabla = []

        for mes in range(1, self.plazo_meses + 1):
            interes = saldo * self.tasa_interes
            cuota = self.calcular_cuota_mensual()
            amortizacion = cuota - interes
            saldo -= amortizacion
            seguro = self.calcular_seguro()

            tabla.append({
                "mes": mes,
                "cuota": round(cuota, 2),
                "interes": round(interes, 2),
                "amortizacion": round(amortizacion, 2),
                "seguro": round(seguro, 2),
                "saldo": round(saldo if saldo > 0 else 0, 2)
            })

            if saldo <= 0:
                break

        return tabla

    def costo_total_credito(self):
        tabla = self.generar_tabla_amortizacion()
        total = sum(item["cuota"] + item["seguro"] for item in tabla)
        return round(total, 2)

# CLASES DERIVADAS

class CreditoConsumo(Credito):
    def __init__(self, numero_credito, monto):
        super().__init__(numero_credito, monto, plazo_meses=24, tasa_interes=0.025)
        self.proposito = "Libre uso"
        self.sin_garantia = True
        self.tasa_alta = True

    def calcular_cuota_mensual(self):
        return (self.monto * self.tasa_interes) + (self.monto / self.plazo_meses)

    def calcular_seguro(self):
        return self.monto * 0.002

class CreditoHipotecario(Credito):
    def __init__(self, numero_credito, monto, valor_propiedad):
        super().__init__(numero_credito, monto, plazo_meses=240, tasa_interes=0.009)
        self.valor_propiedad = valor_propiedad
        self.inicial_porcentaje = 0.20
        self.plazo_20años = True

    def calcular_cuota_mensual(self):
        i = self.tasa_interes
        n = self.plazo_meses
        return self.monto * (i * (1+i)**n) / ((1+i)**n - 1)

    def calcular_seguro(self):
        return self.monto * 0.001

class CreditoVehicular(Credito):
    def __init__(self, numero_credito, monto, tipo_vehiculo, año):
        super().__init__(numero_credito, monto, plazo_meses=60, tasa_interes=0.015)
        self.tipo_vehiculo = tipo_vehiculo
        self.año = año
        self.inicial_30 = True

    def calcular_cuota_mensual(self):
        return (self.monto * self.tasa_interes) + (self.monto / self.plazo_meses)

    def calcular_seguro(self):
        return self.monto * 0.0015

class CreditoEmpresarial(Credito):
    def __init__(self, numero_credito, monto, plan_negocios):
        super().__init__(numero_credito, monto, plazo_meses=120, tasa_interes=0.012)
        self.plan_negocios = plan_negocios
        self.garantias = True
        self.tasa_preferencial = True

    def calcular_cuota_mensual(self):
        i = self.tasa_interes
        n = self.plazo_meses
        return self.monto * (i * (1+i)**n) / ((1+i)**n - 1)

    def calcular_seguro(self):
        return self.monto * 0.0008

# CREACIÓN DE CRÉDITOS

consumo1 = CreditoConsumo("C001", 5000)
consumo2 = CreditoConsumo("C002", 8000)

hipo1 = CreditoHipotecario("H001", 120000, 150000)
hipo2 = CreditoHipotecario("H002", 200000, 250000)

vehi1 = CreditoVehicular("V001", 30000, "SUV", 2020)
vehi2 = CreditoVehicular("V002", 45000, "Sedán", 2023)

empre1 = CreditoEmpresarial("E001", 100000, "Restaurante")
empre2 = CreditoEmpresarial("E002", 250000, "Tech Startup")

# DEMO: TABLA DE AMORTIZACIÓN Y COSTOS TOTALES

def mostrar_tabla(credito):
    tabla = credito.generar_tabla_amortizacion()
    print(f"\nTABLA DE AMORTIZACIÓN - {type(credito).__name__} ===")
    for fila in tabla[:12]:
        print(fila)
    print(f"Costo total: ${credito.costo_total_credito()}\n")

# Ejemplo de impresión

mostrar_tabla(consumo1)
mostrar_tabla(hipo1)
mostrar_tabla(vehi1)
mostrar_tabla(empre1)