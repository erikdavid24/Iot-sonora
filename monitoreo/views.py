import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import DatoSensor

# --- IMPORTACIONES PARA API Y SWAGGER ---
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


# --- VISTAS DE PÁGINAS (HTML) ---

@login_required
def dashboard_view(request):
    """Vista principal. Renderiza el template HTML del Dashboard."""
    return render(request, 'monitoreo/dashboard.html')


@login_required
def municipios_view(request):
    """Vista secundaria para detalles específicos."""
    from django.core.paginator import Paginator

    lista_datos = DatoSensor.objects.all().order_by('-fecha')
    paginator = Paginator(lista_datos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'monitoreo/municipios.html', {'page_obj': page_obj})


# --- API DE DATOS (FUSIÓN: SWAGGER + HISTORIAL 15 DATOS) ---

@swagger_auto_schema(
    method='get',
    operation_description="Devuelve el historial reciente (últimos 15 datos) de todos los municipios.",
    responses={200: 'JSON con arrays de datos'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_datos(request):
    """
    Endpoint inteligente: Entrega los últimos 15 registros de cada variable
    para que las gráficas se llenen al instante.
    """
    municipios = [
        'hermosillo', 'guaymas', 'nogales', 'caborca', 'cajeme', 'navojoa',
        'san_luis_rio_colorado', 'puerto_penasco', 'agua_prieta', 'cananea',
        'magdalena', 'altar', 'huatabampo', 'etchojoa', 'benito_juarez', 'bacum'
    ]

    datos = {}
    for muni in municipios:
        datos[muni] = {}
        # Iteramos por las 4 variables
        for var in ['temperatura', 'humedad', 'presion', 'radioactividad']:
            # 1. Obtener los últimos 15 registros de la DB
            registros = DatoSensor.objects.filter(municipio=muni, variable=var).order_by('-fecha')[:15]

            # 2. Formatear para la gráfica (Revertimos para que el más viejo esté a la izquierda)
            historial = [
                {'t': r.fecha.strftime("%H:%M:%S"), 'v': r.valor}
                for r in reversed(registros)
            ]
            datos[muni][var] = historial

    # USAMOS 'Response' DE DRF (CORRECTO PARA SWAGGER)
    return Response(datos)


# --- FUNCIONALIDADES EXTRA ---

@login_required
def exportar_csv(request):
    """Genera y descarga el historial en archivo Excel (CSV)."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historial_climatico.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Hora', 'Municipio', 'Variable', 'Valor'])

    datos = DatoSensor.objects.all().order_by('-fecha')

    for dato in datos:
        fecha_str = dato.fecha.strftime("%d/%m/%Y")
        hora_str = dato.fecha.strftime("%H:%M:%S")
        municipio_bonito = dato.municipio.replace('_', ' ').title()
        variable_bonita = dato.variable.capitalize()
        writer.writerow([fecha_str, hora_str, municipio_bonito, variable_bonita, dato.valor])

    return response


def register(request):
    """Vista para registro de nuevos usuarios."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})