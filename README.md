# 🌵 IoT Sonora - Sistema de Monitoreo Climático en Tiempo Real

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)
![RealTime](https://img.shields.io/badge/WebSockets-Channels-red?style=for-the-badge)
![MQTT](https://img.shields.io/badge/IoT-MQTT-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Plataforma integral de monitoreo IoT** desarrollada como Proyecto Final de Ingeniería. El sistema permite la visualización y gestión de variables climáticas en el estado de Sonora en **Tiempo Real**, implementando una arquitectura asíncrona robusta con Django Channels y WebSockets.

---

## 🚀 Características y Funcionalidades

### 📡 Comunicación en Tiempo Real (Real-Time)
* **Arquitectura ASGI:** Servidor asíncrono impulsado por **Daphne** y **Django Channels**.
* **WebSockets:** Conexión bidireccional persistente. Las gráficas se actualizan en el milisegundo exacto en que llega un dato, sin necesidad de recargar la página (latencia < 50ms).
* **Ingesta MQTT:** Cliente Paho-MQTT corriendo en background, suscrito al wildcard `sonora/#` con reconexión automática.

### 📊 Dashboard y Visualización (Frontend)
* **Diseño Glassmorphism:** Interfaz moderna con efectos de transparencia, sombras suaves y diseño responsivo (Bootstrap 5).
* **Gráficas Dinámicas:** Implementación avanzada de **Chart.js** que mantiene un historial local en memoria (últimos 15 puntos) para una experiencia de usuario fluida.
* **Soporte Multi-Variable:** Monitoreo de Temperatura (°C), Humedad (%), Presión (hPa) y Radioactividad (µSv).
* **Alertas Visuales Inteligentes:**
    * 🔥 **Alerta de Fuego:** Indicador rojo y negrita al superar los 38°C.
    * ☢️ **Alerta de Radiación:** Indicador de peligro amarillo al detectar niveles > 5.0 µSv.

### 🛠️ Backend y Gestión
* **Persistencia de Datos:** Todos los eventos se procesan, limpian y almacenan en base de datos SQL.
* **Panel de Administración Custom:** Interfaz `/admin` personalizada con estilos modernos para gestión de usuarios y sensores.
* **Seguridad:** Sistema completo de Autenticación (Login/Logout/Registro) y protección de rutas con decoradores.
* **Reportes:** Módulo de exportación de historial completo a **Excel (CSV)**.
* **API REST Documentada:** Documentación técnica automática generada con **Swagger/OpenAPI** accesible en `/swagger/`.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Lenguaje** | Python 3.10+ | Lógica del servidor y scripts. |
| **Framework Web** | Django 4.2 | Estructura MVC/MVT robusta. |
| **Asincronía** | Django Channels & Daphne | Manejo de WebSockets y protocolo ASGI. |
| **Protocolo IoT** | MQTT (Paho Client) | Ingesta de datos de sensores. |
| **Frontend** | HTML5, CSS3, JS (ES6) | Bootstrap 5 para estilos y lógica de cliente. |
| **Base de Datos** | SQLite3 | Almacenamiento ligero y portable. |
| **Gráficos** | Chart.js | Visualización de datos interactiva. |
