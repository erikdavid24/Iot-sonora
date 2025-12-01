from django.contrib import admin
from .models import DatoSensor


@admin.register(DatoSensor)
class DatoSensorAdmin(admin.ModelAdmin):
    # 1. Qué columnas ver en la lista
    list_display = ('fecha', 'municipio', 'variable', 'valor')

    # 2. Filtros laterales (¡Súper útiles!)
    list_filter = ('municipio', 'variable', 'fecha')

    # 3. Barra de búsqueda
    search_fields = ('municipio',)

    # 4. Navegación rápida por fechas (arriba de la lista)
    date_hierarchy = 'fecha'

    # 5. Orden (lo más nuevo primero)
    ordering = ('-fecha',)


# Opcional: Cambiar el título del panel azul
admin.site.site_header = "Administración IoT Sonora"
admin.site.site_title = "Portal IoT"
admin.site.index_title = "Bienvenido al Sistema de Gestión"