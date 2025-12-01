from django.db import models

class DatoSensor(models.Model):
    municipio = models.CharField(max_length=50)
    variable = models.CharField(max_length=50) # Ejemplo: temperatura
    valor = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True) # Se guarda la hora automática

    class Meta:
        verbose_name = "Lectura de Sensor"
        verbose_name_plural = "Historial de Sensores"

    def __str__(self):
        return f"{self.fecha} - {self.municipio}: {self.valor}"