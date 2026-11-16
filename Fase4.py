# ===========================================================================================================================
# UNAD - PROGRAMACIÓN
# FASE 4 Prácticas Simuladas

# Nombre de los estudiante: [Henry Laurin Velasquez Leal][Erika Yadira Hernandez Romero][Diego Alejandro Luque Rodriguez]
# Grupo: [213023_645]
# Programa: Ingeniería de Sistemas
# Código Fuente:Fuente Colaborativa
# ========================================================================================================================= 



import datetime
from abc import ABC, abstractmethod

# ==========================================
# 1. EXCEPCIONES PERSONALIZADAS Y LOGS
# ==========================================
class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Excepción para datos de cliente erróneos o incompletos."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción cuando un servicio no está disponible o es incorrecto."""
    pass

class ReservaError(SoftwareFJError):
    """Excepción para fallas en la creación o procesamiento de reservas."""
    pass

def registrar_log(mensaje, tipo="INFO"):
    """Registra eventos y errores en un archivo de texto plano."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_linea = f"[{timestamp}] [{tipo}] {mensaje}\n"
    try:
        with open("sistema_fj.log", "a", encoding="utf-8") as archivo:
            archivo.write(log_linea)
    except Exception as e:
        print(f"Error crítico al escribir en el log: {e}")


# ==========================================
# 2. CLASE ABSTRACTA BASE Y CLIENTE
# ==========================================
class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema[cite: 1]."""
    @abstractmethod
    def obtener_detalles(self):
        pass

class Cliente(EntidadBase):
    def __init__(self, identificacion, nombre, correo, telefono):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._validar_datos()

    def _validar_datos(self):
        if not self.identificacion or not str(self.identificacion).strip():
            raise ClienteInvalidoError("La identificación del cliente no puede estar vacía.")
        if not self.nombre or len(self.nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        if "@" not in self.correo or "." not in self.correo:
            raise ClienteInvalidoError(f"El correo '{self.correo}' no es válido.")
        if not str(self.telefono).isdigit() or len(str(self.telefono)) < 7:
            raise ClienteInvalidoError(f"El teléfono '{self.telefono}' debe contener solo dígitos (mínimo 7).")

    def obtener_detalles(self):
        return f"Cliente [ID: {self.identificacion}] - Nombre: {self.nombre} - Correo: {self.correo}"


# ==========================================
# 3. JERARQUÍA DE SERVICIOS
# ==========================================
class Servicio(ABC):
    def __init__(self, codigo, nombre_servicio, costo_base):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
        self._validar_servicio()

    def _validar_servicio(self):
        if not self.codigo or not self.nombre_servicio:
            raise ServicioNoDisponibleError("El código y nombre del servicio son obligatorios.")
        if self.costo_base < 0:
            raise ServicioNoDisponibleError("El costo base no puede ser negativo.")

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass


class ReservaSalas(Servicio):
    def __init__(self, codigo, nombre_servicio, costo_base, capacidad_personas):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.capacidad_personas = capacidad_personas

    def describir_servicio(self):
        return f"Reserva de Sala: {self.nombre_servicio} (Capacidad: {self.capacidad_personas} personas)"

    def calcular_costo(self, horas, incluye_catering=False, descuento_porcentaje=0.0):
        try:
            if horas <= 0:
                raise ValueError("Las horas deben ser mayores a cero.")
            costo_total = self.costo_base * horas
            if incluye_catering:
                costo_total += 50.0 * self.capacidad_personas
            if descuento_porcentaje > 0:
                costo_total -= costo_total * (descuento_porcentaje / 100)
            return round(costo_total, 2)
        except Exception as e:
            registrar_log(f"Error calculando costo en ReservaSalas: {e}", "ERROR")
            raise


class AlquilerEquipos(Servicio):
    def __init__(self, codigo, nombre_servicio, costo_base, tipo_equipo):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.tipo_equipo = tipo_equipo

    def describir_servicio(self):
        return f"Alquiler de Equipo: {self.nombre_servicio} [Tipo: {self.tipo_equipo}]"

    def calcular_costo(self, dias, seguro_adicional=False):
        try:
            if dias <= 0:
                raise ValueError("Los días de alquiler deben ser mayores a cero.")
            costo_total = self.costo_base * dias
            if seguro_adicional:
                costo_total += 15.0 * dias
            return round(costo_total, 2)
        except Exception as e:
            registrar_log(f"Error calculando costo en AlquilerEquipos: {e}", "ERROR")
            raise


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre_servicio, costo_base, especialidad):
        super().__init__(codigo, nombre_servicio, costo_base)
        self.especialidad = especialidad

    def describir_servicio(self):
        return f"Asesoría Especializada: {self.nombre_servicio} (Área: {self.especialidad})"

    def calcular_costo(self, sesiones, aplicar_impuesto=True):
        try:
            if sesiones <= 0:
                raise ValueError("El número de sesiones debe ser mayor a cero.")
            costo_total = self.costo_base * sesiones
            if aplicar_impuesto:
                costo_total *= 1.19
            return round(costo_total, 2)
        except Exception as e:
            registrar_log(f"Error calculando costo en AsesoriaEspecializada: {e}", "ERROR")
            raise

