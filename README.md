# 🌐 Footprint Analyzer 

¡Bienvenido a **Footprint Analyzer**! Una aplicación web interactiva diseñada para auditar, concienciar y predecir el impacto ambiental y la huella de carbono digital que generan las páginas web en tiempo real. 

Este proyecto fue desarrollado bajo la metodología **Vibe Coding**, priorizando el prototipado ágil y la integración inteligente de modelos predictivos mediante IA.

---

## 📄 Descripción del Proyecto

El internet consume una cantidad masiva de electricidad a nivel global. Cada vez que un usuario visita una URL, se transfieren megabytes de datos a través de servidores que, en su mayoría, dependen de combustibles fósiles. 

**Footprint Analyzer** permite a cualquier usuario introducir una URL para:
1. **Escanear en tiempo real** el peso estimado de la página web mediante peticiones HTTP.
2. **Calcular las emisiones de CO2** basándose en constantes científicas de consumo energético ($0.81 \text{ kWh/GB}$) y el tipo de infraestructura (Hosting Estándar vs. Green Hosting).
3. **Asignar un Eco-Score Digital** (calificaciones de la A a la D) según el nivel de optimización.
4. **Visualizar equivalencias cotidianas** para entender el impacto real (tazas de té hervidas, cargas de smartphone, km en coche eléctrico y árboles necesarios para absorber el impacto).
5. **Predecir a futuro** mediante un modelo entrenado de **Machine Learning** el acumulado de emisiones a 1, 3, 6 y 12 meses, considerando una tasa variable de crecimiento de tráfico de usuarios.

---

## 🧠 El Modelo de Machine Learning (Regresión Lineal)

Para cumplir con el enfoque analítico del Bootcamp, la aplicación integra un modelo formal de **Regresión Lineal** de la librería `scikit-learn`. 

* **Entrenamiento:** El modelo genera internamente un conjunto de datos (dataset sintético) que simula el comportamiento de emisiones de los últimos 6 meses del sitio web, aplicando de forma compuesta el porcentaje de crecimiento de tráfico seleccionado por el usuario.
* **Predicción:** Usando la ecuación de la recta optimizada por el algoritmo, el sistema realiza un pronóstico de variables continuas para proyectar el CO2 acumulado a largo plazo, plasmándolo de manera visual en un gráfico interactivo de barras con `Plotly`.

---

## 🛠️ Requisitos e Instalación Local

Para ejecutar este proyecto en tu computadora, asegúrate de tener instalado **Python 3.9 o superior** y sigue estos pasos en tu terminal:

### 1. Clonar el proyecto o situarte en la carpeta
Abre tu terminal y navega hasta la carpeta raíz donde se encuentra el archivo `app_web.py`.

### 2. Crear y activar tu Entorno Virtual (Recomendado)
```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual (En Mac / Linux)
source venv/bin/activate

# Activar el entorno virtual (En Windows)
venv\Scripts\activate
