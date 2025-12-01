import paho.mqtt.client as mqtt
import random
from django.core.cache import cache
from .models import DatoSensor
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Configuración del Broker
BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "sonora/#"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Conectado al Broker MQTT. Suscrito a: {TOPIC}")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Error conexión: {rc}")


def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')

        # Filtramos variables válidas
        if len(topic_parts) == 3 and topic_parts[2] in ['temperatura', 'humedad', 'presion', 'radioactividad']:
            municipio = topic_parts[1]
            variable = topic_parts[2]
            payload = msg.payload.decode('utf-8')

            # 1. Guardar en Caché
            cache_key = f"{municipio}_{variable}"
            cache.set(cache_key, payload, timeout=None)

            # 2. Guardar en BD
            try:
                # Limpieza de datos (quitar letras)
                valor_limpio = payload.lower().replace('hpa', '').replace('µsv', '').replace('usv', '').strip()
                valor_float = float(valor_limpio)

                DatoSensor.objects.create(
                    municipio=municipio,
                    variable=variable,
                    valor=valor_float
                )
                print(f"📥 {municipio} ({variable}): {valor_float} (Guardado)")

                # --- 3. ENVIAR A WEBSOCKET (CORREGIDO) ---
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "sensores",
                    {
                        "type": "sensor_update",
                        "data": {
                            "municipio": municipio,
                            # AQUÍ AGREGAMOS LAS VARIABLES QUE FALTABAN:
                            "temperatura": valor_limpio if variable == 'temperatura' else None,
                            "humedad": valor_limpio if variable == 'humedad' else None,
                            "presion": valor_limpio if variable == 'presion' else None,
                            "radioactividad": valor_limpio if variable == 'radioactividad' else None,
                        }
                    }
                )
                # ----------------------------------------

            except ValueError:
                print(f"⚠️ Dato no numérico recibido: {payload}")

    except Exception as e:
        print(f"❌ Error MQTT: {e}")


def start_mqtt():
    client_id = f'django-sonora-{random.randint(1000, 9999)}'
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT)
        client.loop_start()
    except Exception as e:
        print(f"⚠️ No se pudo conectar al broker MQTT: {e}")