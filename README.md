# mayapipis-sensors

# Documentación del Proyecto: Publicación de Datos Simulados en HiveMQ Cloud usando MQTT

Este proyecto simula datos de sensores (como temperatura, humo, distancia y luz) y los publica en un broker MQTT en la nube utilizando **HiveMQ Cloud**. Los datos generados se pueden visualizar en tiempo real con el cliente **MQTTX**. El sistema incluye dos scripts principales:

- `fake_data_emqx_publisher.py`: Genera datos falsos de sensores en formato JSON y los imprime en la consola.
- `serial_reader_to_emqx.py`: Lee esos datos, los procesa y los publica en tópicos MQTT específicos.

---

## Requisitos Previos

- **Python 3** instalado.
- Una cuenta en **HiveMQ Cloud** (gratis en hivemq.com).
- **MQTTX** instalado para visualizar datos (descarga desde mqttx.app).
- Acceso a las credenciales de tu clúster HiveMQ (Host, Puerto, Usuario, Contraseña).

---

## Instalación

1. **Instala las dependencias**: Ejecuta este comando en tu terminal para instalar la biblioteca MQTT:

   ```bash
   pip3 install paho-mqtt
   ```

2. **Descarga los scripts**: Asegúrate de tener `fake_data_emqx_publisher.py` y `serial_reader_to_emqx.py` en el mismo directorio.

---

## Configuración del Broker (HiveMQ Cloud)

1. **Regístrate y crea un clúster**:

   - Accede a HiveMQ Cloud, crea un clúster gratuito y copia los datos de conexión.

2. **Ejemplo de credenciales**:

   - Host: `iotproject-ee93447b.a02.usw2.aws.hivemq.cloud`
   - Puerto: `8883`
   - Usuario: `Admin`
   - Contraseña: `Admin123`

3. **Actualiza el script**: Abre `serial_reader_to_emqx.py`:

   ```python
   MQTT_BROKER   = "iotproject-ee93447b.a02.usw2.aws.hivemq.cloud"  
   MQTT_PORT     = 8883
   MQTT_USERNAME = "Admin"  
   MQTT_PASSWORD = "Admin123" 
   BASE_TOPIC    = "arduino"
   ```

---

## Ejecución

1. **Inicia el sistema**: En una terminal, desde el directorio de los scripts, ejecuta:

   ```bash
   python3 serial_reader_to_emqx.py
   ```

   - Esto lanzará `fake_data_emqx_publisher.py` como subproceso y publicará datos cada 2 segundos en HiveMQ Cloud.
   - Verás mensajes como "📤 Bloque publicado en HiveMQ Cloud" en la consola.

2. **Tópicos publicados**:

   - `arduino/temperature`
   - `arduino/smoke`
   - `arduino/smoke_level`
   - `arduino/distance`
   - `arduino/light`
   - `arduino/timestamp`

---

## Visualización en MQTTX

Para ver los datos en **MQTTX**, sigue estos pasos:

1. **Abre MQTTX**:

   - Descarga e instala desde mqttx.app si aún no lo tienes.

2. **Configura la conexión**:

   - Haz clic en **"+"** o "New Connection" y completa:
     - **Name**: "HiveMQ Broker" (o cualquier nombre).
     - **Host**: `mqtts://iotproject-ee93447b.a02.usw2.aws.hivemq.cloud` (usa tu Host).
     - **Port**: `8883`.
     - **Username**: `Admin` (tu usuario).
     - **Password**: `Admin123` (tu contraseña).
     - **SSL/TLS**: Activa esta opción.

3. **Conéctate**:

   - Haz clic en **Connect**. Deberías ver "Connected" si todo está bien.

4. **Suscríbete a los tópicos**:

   - En la sección de suscripción, agrega `arduino/#` para ver todos los datos, o suscríbete a tópicos específicos como `arduino/temperature`.
   - Los mensajes aparecerán cada 2 segundos con los valores simulados.

---