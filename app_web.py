#librería Streamlit para construir la interfaz gráfica de la aplicación web
import streamlit as st
# Pandas para manejar la estructura de tablas de datos que usará nuestro gráfico
import pandas as pd
# Plotly Express para generar el gráfico de barras dinámico e interactivo
import plotly.express as px
# Requests para conectarnos a internet y poder inspeccionar las páginas web
import requests
#  el modelo matemático de Regresión Lineal desde la librería estándar de Machine Learning
from sklearn.linear_model import LinearRegression
# Importamos Numpy para estructurar los datos en forma de matrices o vectores numéricos rápidos
import numpy as np

# Configuramos los parámetros visuales básicos 
st.set_page_config(page_title="Footprint Analyzer", page_icon="🌐", layout="centered")

st.title("🌐 Footprint Analyzer")

st.markdown("### Descubre el impacto ambiental analizando URLs")

# --- CONSTANTES CIENTÍFICAS DE ENERGÍA Y CARBONO ---
# Guardamos los Kilovatios-hora (kWh) promedio que consume transferir 1 Gigabyte (GB) de datos en internet
KWH_PER_GB = 0.81

# Guardamos los gramos de CO2 que emite un servidor normal que funciona con combustibles fósiles
CO2_PER_KWH_FOSIL = 442

# Guardamos los gramos de CO2 que emite un servidor ecológico que funciona con energía renovable
CO2_PER_KWH_VERDE = 50

# --- FUNCIÓN PARA ESCANEAR EL TAMAÑO DE LA WEB ---
# Definimos una función propia llamada 'obtener_peso_web' que recibirá la dirección URL que introduzca el usuario
def obtener_peso_web(url):
    # Verificamos si la URL ingresada no comienza con los protocolos estándar de red 'http' o 'https'
    if not url.startswith("http://") and not url.startswith("https://"):
        # Si le faltan los protocolos, le anteponemos 'https://' automáticamente por compatibilidad
        url = "https://" + url
    
    # Abrimos un bloque de seguridad 'try' para ejecutar operaciones que podrían fallar (errores de red)
    try:
        # Creamos una identidad simulada de navegador de internet para evitar bloqueos automáticos de seguridad
        headers = {"User-Agent": "Mozilla/5.0"}
        # Realizamos una petición HTTP GET a la URL configurando un tiempo límite de espera de 5 segundos
        respuesta = requests.get(url, headers=headers, timeout=5)
        # Medimos la longitud en caracteres/bytes del contenido descargado de la página web
        peso_bytes = len(respuesta.content)
        # Convertimos los bytes medidos a Megabytes dividiendo consecutivamente dos veces entre 1024
        peso_mb = peso_bytes / (1024 * 1024)
        # Devolvemos el peso final redondeado a 2 decimales (mínimo 0.5 MB) junto con la señal True (Éxito)
        return max(round(peso_mb, 2), 0.5), True
    # Si la página web da un error, está caída o bloquea la lectura, se activa este bloque de emergencia
    except:
        # Devolvemos un peso promedio estándar (2.4 MB) y la señal False indicando que no se pudo escanear
        return 2.4, False

# --- INTERFAZ DE USUARIO ---

st.sidebar.header("⚙️ Configuración")
url_web = st.text_input("Introduce la URL a analizar:", "www.wikipedia.org")

# Llamamos a nuestra función de escaneo enviándole la URL y guardamos las dos respuestas obtenidas
peso_detectado, escaneo_exitoso = obtener_peso_web(url_web)

# Si la variable 'escaneo_exitoso' contiene un valor verdadero (True), mostramos un mensaje verde
if escaneo_exitoso:
    # Desplegamos el aviso confirmando que se detectó el peso automáticamente
    st.success(f"✨ ¡Escaneo exitoso! Hemos detectado que '{url_web}' pesa aproximadamente **{peso_detectado} MB**.")
# Si la variable contiene un valor falso (False), mostramos un mensaje amarillo de advertencia
else:
    # Desplegamos el aviso informando que usaremos una aproximación ajustable manualmente
    st.warning(f"⚠️ No pudimos escanear '{url_web}' automáticamente. Usaremos un peso estimado, pero puedes ajustarlo abajo.")

col1, col2 = st.columns(2)

# Asignamos los componentes que se van a renderizar exclusivamente dentro de la columna 1 (Izquierda)
with col1:
    # Creamos una casilla numérica interactiva para el peso en MB, usando por defecto el peso detectado
    peso_web_mb = st.number_input("Tamaño de la página cargada (en MB):", min_value=0.1, max_value=50.0, value=peso_detectado, step=0.1)
    # Creamos otra casilla numérica interactiva para capturar las visitas mensuales que recibe la página web
    visitas_mensuales = st.number_input("Visitas actuales al mes:", min_value=100, max_value=1000000, value=15000, step=500)

# Asignamos los componentes que se van a renderizar exclusivamente dentro de la columna 2 (Derecha)
with col2:
    # Creamos dos botones radiales para seleccionar el tipo de energía que alimenta al servidor de la web
    tipo_hosting = st.radio("¿El servidor utiliza energía renovable?", ["No / No lo sé (Energía Estándar)", "Sí (Green Hosting Certificado)"])
    # Creamos un deslizador numérico para estimar el porcentaje mensual de crecimiento del tráfico web
    crecimiento_trafico = st.slider("Crecimiento mensual estimado del tráfico (%)", 0, 50, 10)

# --- LÓGICA DE CIENCIA DE DATOS BASE ---
# Convertimos el tamaño de la página de Megabytes a Gigabytes dividiendo entre 1024
peso_gb = peso_web_mb / 1024
# Calculamos los kWh consumidos por visita multiplicando los Gigabytes por la constante de consumo eléctrico
energia_kwh = peso_gb * KWH_PER_GB
# Usamos un condicional simplificado para asignar la intensidad de CO2 dependiendo del hosting seleccionado
intensidad_carbono = CO2_PER_KWH_VERDE if "Sí" in tipo_hosting else CO2_PER_KWH_FOSIL

# Calculamos los gramos de CO2 por visita multiplicando la energía consumida por el factor de carbono
co2_por_visita_gramos = round(energia_kwh * intensidad_carbono, 3)
# Calculamos los kg de CO2 mensuales dividiendo los gramos entre 1000 y multiplicando por las visitas actuales
co2_mensual_kg = round((co2_por_visita_gramos * visitas_mensuales) / 1000, 2)

# --- CLASIFICACIÓN DE ECO-SCORE ---
# Si la web emite menos de 0.2 gramos por visita, califica con la nota máxima ecológica
if co2_por_visita_gramos < 0.2:
    # Guardamos la etiqueta de la nota y asignamos el color verde para el texto
    eco_score, color_score = "A (Ultra Eficiente)", "green"
# Si la web emite entre 0.2 y 0.5 gramos por visita, califica con una buena nota
elif co2_por_visita_gramos < 0.5:
    # Guardamos la etiqueta de la nota y asignamos el color azul para el texto
    eco_score, color_score = "B (Optimizado)", "blue"
# Si la web emite entre 0.5 y 1.0 gramos por visita, califica dentro del promedio global
elif co2_por_visita_gramos < 1.0:
    # Guardamos la etiqueta de la nota y asignamos el color naranja para el texto
    eco_score, color_score = "C (Promedio Global)", "orange"
# Si supera 1.0 gramo por cada visita, califica como una web con problemas de contaminación digital
else:
    # Guardamos la etiqueta de la nota y asignamos el color rojo de alerta para el texto
    eco_score, color_score = "D (Pesada / Requiere Optimización)", "red"

# --- IMPRESIÓN DE RESULTADOS EN PANTALLA ---
# Dibujamos una línea divisoria horizontal en la pantalla
st.markdown("---")
# Colocamos un subtítulo intermedio para la sección del reporte estadístico actual
st.subheader(f"📊 Reporte Ecológico Automatizado")

# Volvemos a dividir la pantalla en dos columnas para ubicar dos tarjetas numéricas lado a lado
m1, m2 = st.columns(2)
# Código asignado para la primera mini-columna
with m1:
    # Mostramos los gramos de CO2 emitidos por una sola visita en una tarjeta grande resaltada
    st.metric(label="Huella por visita", value=f"{co2_por_visita_gramos} g CO2")
# Código asignado para la segunda mini-columna
with m2:
    # Mostramos los kilogramos totales calculados para el mes en curso en otra tarjeta grande
    st.metric(label="Emisiones Mes Actual", value=f"{co2_mensual_kg} kg CO2")

# Mostramos el resultado del Eco-Score aplicando etiquetas de color dinámicas integradas en Streamlit
st.markdown(f"### Eco-Score Digital: :{color_score}[{eco_score}]")

# --- 💡 SECCIÓN: EQUIVALENCIAS ECOLÓGICAS CREATIVAS ---
# Dibujamos una línea sutil para separar las tarjetas de las equivalencias de la vida real
st.markdown("---")
# Colocamos un subtítulo llamativo para los datos interesantes
st.markdown("### 🌍 ¿Qué significan estos números en la vida real?")
# Ponemos una nota aclaratoria amigable indicando que los datos son una estimación
st.caption("A continuación te mostramos a qué equivalen tus emisiones acumuladas en un año entero:")

# Calculamos el CO2 total que generará la página en todo un año multiplicando el dato mensual por 12
co2_anual_kg = co2_mensual_kg * 12

# Convertimos los kilogramos anuales a tazas de té hirviendo (multiplicando por 135 tazas por cada kg)
tazas_te = round(co2_anual_kg * 135)
# Convertimos los kilogramos anuales a cargas de smartphone (multiplicando por 117 cargas por cada kg)
cargas_movil = round(co2_anual_kg * 117)
# Calculamos cuántos árboles se necesitan dividiendo el CO2 anual entre 22 (lo que absorbe un árbol al año)
# Usamos max(..., 1) para que si el resultado da cero, al menos muestre '1 árbol' como mínimo visual
arboles_necesarios = max(round(co2_anual_kg / 22), 1)
# Calculamos los kilómetros de coche eléctrico dividiendo el CO2 anual entre 0.15 kg que genera cada kilómetro
km_coche = round(co2_anual_kg / 0.15)

# Dividimos el layout en 2 nuevas columnas para que las equivalencias queden ordenadas estéticamente
eq1, eq2 = st.columns(2)

# Programamos lo que se verá en la primera columna de equivalencias (Lado Izquierdo)
with eq1:
    # Usamos st.info para mostrar un recuadro azul bonito con el dato de las tazas de té
    st.info(f"🫖 **{tazas_te:,} tazas de té**\n\nEl mismo CO2 que se produce al hervir agua para tantas tazas.")
    # Usamos st.info para mostrar el dato del coche eléctrico justo debajo
    st.info(f"🚗 **{km_coche:,} km en coche eléctrico**\n\nElectricidad suficiente para recorrer esta distancia.")

# Programamos lo que se verá en la segunda columna de equivalencias (Lado Derecho)
with eq2:
    # Usamos st.info para mostrar un recuadro bonito con el dato de las cargas de teléfonos móviles
    st.info(f"📱 **{cargas_movil:,} cargas de smartphone**\n\nEquivale a cargar la batería de un móvil normal desde cero.")
    # Usamos st.info para mostrar cuántos árboles se necesitarían para limpiar esa contaminación
    st.info(f"🌳 **{arboles_necesarios} árboles al año**\n\nSe requiere esta cantidad de árbol(es) para absorber este carbono.")

# --- 🧠 INTEGRADOR DE PREDICCIÓN CON MACHINE LEARNING ---
# Dibujamos una línea divisoria horizontal en la pantalla
st.markdown("---")
# Colocamos el subtítulo principal de la sección predictiva del proyecto
st.subheader("🔮 Predicción Inteligente del Impacto Ambiental (Machine Learning)")
# Escribimos un pequeño bloque explicativo de cara al usuario final de la aplicación
st.write("Entrenando un modelo de Regresión Lineal para predecir la acumulación de emisiones considerando el crecimiento de tu comunidad.")

# 1. Creamos un vector numérico con Numpy representando una secuencia de los meses históricos del 1 al 6
# Usamos el método .reshape(-1, 1) para transformar la lista en una matriz de una sola columna exigida por Sklearn
meses_historicos = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)

# Calculamos mediante un bucle comprimido las emisiones acumuladas simuladas para el entrenamiento del modelo
# El cálculo considera el crecimiento porcentual acumulativo configurado por el usuario en el control deslizante
emisiones_historicas = np.array([co2_mensual_kg * m * (1 + (crecimiento_trafico/100)) for m in range(1, 7)])

# 2. Inicializamos una instancia vacía del algoritmo matemático de Regresión Lineal de Scikit-Learn
modelo_ml = LinearRegression()
# Entrenamos formalmente el modelo matemático pasándole los meses históricos y los resultados de emisiones calculados
modelo_ml.fit(meses_historicos, emisiones_historicas)

# 3. Creamos una nueva matriz con Numpy indicando los periodos futuros clave que queremos pronosticar (1, 3, 6 y 12 meses)
meses_futuros = np.array([1, 3, 6, 12]).reshape(-1, 1)
# Usamos el modelo matemático previamente entrenado para predecir los kilogramos acumulados en esos meses del futuro
predicciones_co2 = modelo_ml.predict(meses_futuros)

# --- CONSTRUCCIÓN DEL GRÁFICO INTERACTIVO CON LOS DATOS PREDICTIVOS ---
# Estructuramos una tabla organizada (DataFrame) emparejando los textos del futuro con los valores numéricos redondeados que predijo el modelo
df_proyeccion = pd.DataFrame({
    "Tiempo de Operación": ["1 Mes", "3 Meses", "6 Meses", "1 Año"],
    "Predicción CO2 Acumulado (kg)": np.round(predicciones_co2, 2)
})

# Le pedimos a Plotly Express que construya un gráfico de barras a partir de la tabla predictiva generada
fig = px.bar(
    df_proyeccion, 
    x="Tiempo de Operación", 
    y="Predicción CO2 Acumulado (kg)", 
    title="Predicción de Emisiones Acumuladas según el Modelo ML",
    color="Predicción CO2 Acumulado (kg)",
    color_continuous_scale=px.colors.sequential.Reds
)
# Dibujamos finalmente el objeto gráfico de barras en la pantalla de nuestra aplicación web
st.plotly_chart(fig)