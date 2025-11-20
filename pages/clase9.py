import dash
from dash import html, dcc, callback, Input, Output, State
import requests
import plotly.graph_objects as go # ¡Corregido el error de importación!
from datetime import datetime

dash.register_page(__name__, path='/pagina9', name='clima', order=9)

# --- Valores iniciales (Ej: Lima, Perú) ---
DEFAULT_LAT = -12.04
DEFAULT_LON = -77.02

layout = html.Div([
    
    html.Div([
        html.H2("Dashboard del Clima", className="title"),

        html.Div([
            html.Label("Latitud:"),
            dcc.Input(
                id="input-lat-clima",
                type="number",
                value=DEFAULT_LAT,
                className="input-field",
            )
        ], className="input-group"),

        html.Div([
            html.Label("Longitud:"),
            dcc.Input(
                id="input-lon-clima",
                type="number",
                value=DEFAULT_LON,
                className="input-field",
            )
        ], className="input-group"),

        html.Button("Consultar Clima", id="btn-actualizar-clima", className="btn-generar"),

        html.Div(
            id="info-actualizado-clima",
            className="info-actualizado" 
        )

    ], className="content left"),

    html.Div([
        html.H2("Clima Actual", className="title"),

        # --- Tarjetas KPI (igual que antes) ---
        html.Div([
            html.H4("Temperatura", className="kpi-card-title kpi-casos"),
            html.H3(id="kpi-temperatura", className="kpi-card-value kpi-casos-val")
        ], className="kpi-card"),

        html.Div([
            html.H4("Humedad", className="kpi-card-title kpi-recuperados"),
            html.H3(id="kpi-humedad", className="kpi-card-value kpi-recuperados-val")
        ], className="kpi-card"),

        html.Div([
            html.H4("Velocidad del Viento", className="kpi-card-title kpi-muertes"),
            html.H3(id="kpi-viento", className="kpi-card-value kpi-muertes-val")
        ], className="kpi-card"),
        
        # --- NUEVO: Contenedor para el Gráfico ---
        # Reutilizamos la clase "graph-box" que ya existe en tu CSS
        html.Div([
            dcc.Graph(id="grafica-clima-forecast")
        ], className="graph-box")

    ], className="content right") 
], className="main-container")


def obtener_datos_clima(lat, lon):
    """
    Consulta la API de Open-Meteo para el clima actual Y EL PRONÓSTICO.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            # 1. Pedimos los datos actuales
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            # 2. Pedimos el pronóstico por hora
            "hourly": ["temperature_2m", "relative_humidity_2m"],
            # 3. Pedimos solo 1 día de pronóstico
            "forecast_days": 1
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos del clima: {e}")
        return None

@callback(
    # Salidas para los KPIs
    Output("kpi-temperatura", "children"),
    Output("kpi-humedad", "children"),
    Output("kpi-viento", "children"),
    # Salida para el mensaje de info
    Output("info-actualizado-clima", "children"),
    # NUEVA Salida para el gráfico
    Output("grafica-clima-forecast", "figure"),
    
    # Entradas
    Input("btn-actualizar-clima", "n_clicks"),
    State("input-lat-clima", "value"),
    State("input-lon-clima", "value"),
    prevent_initial_call=False 
)
def actualizar_dashboard_clima(n_clicks, lat, lon):
    
    # --- Estado de error o inicial ---
    # Creamos una figura vacía por defecto
    fig_vacia = go.Figure()
    fig_vacia.update_layout(
        title="Pronóstico 24h", 
        paper_bgcolor="white", 
        plot_bgcolor="white"
    )
    
    if lat is None or lon is None:
        fig_vacia.add_annotation(text="Ingrese latitud y longitud", showarrow=False)
        return "N/A", "N/A", "N/A", "Por favor, ingrese latitud y longitud.", fig_vacia

    datos = obtener_datos_clima(lat, lon)

    if not datos:
        fig_vacia.add_annotation(text="Error de API", showarrow=False, font=dict(color="red"))
        return "Error", "Error", "Error", "No se pudo conectar a la API del clima.", fig_vacia

    # --- Procesamiento de datos (si todo salió bien) ---
    try:
        # 1. Procesar datos ACTUALES (para KPIs)
        current = datos.get("current", {})
        units = datos.get("current_units", {})

        temp = current.get("temperature_2m", "N/A")
        humedad = current.get("relative_humidity_2m", "N/A")
        viento = current.get("wind_speed_10m", "N/A")

        temp_unit = units.get("temperature_2m", "")
        hum_unit = units.get("relative_humidity_2m", "")
        viento_unit = units.get("wind_speed_10m", "")

        temp_texto = f"{temp} {temp_unit}"
        hum_texto = f"{humedad} {hum_unit}"
        viento_texto = f"{viento} {viento_unit}"
        
        mensaje = f"Clima actualizado para ({lat}, {lon})."
        
        # 2. Procesar datos DEL PRONÓSTICO (para el Gráfico)
        hourly_data = datos.get("hourly", {})
        fechas_str = hourly_data.get("time", [])
        temperaturas_forecast = hourly_data.get("temperature_2m", [])
        humedad_forecast = hourly_data.get("relative_humidity_2m", [])

        if not fechas_str:
            # Si hay datos actuales pero no pronóstico
            fig_vacia.add_annotation(text="No hay datos de pronóstico", showarrow=False)
            return temp_texto, hum_texto, viento_texto, mensaje, fig_vacia

        # Convertir fechas de texto a objetos datetime
        fechas_dt = [datetime.fromisoformat(f) for f in fechas_str]

        # --- Creación del Gráfico ---
        fig = go.Figure()

        # Trace de Temperatura (Eje Y principal)
        fig.add_trace(go.Scatter(
            x=fechas_dt,
            y=temperaturas_forecast,
            mode='lines+markers',
            name='Temperatura (°C)',
            line=dict(color='orange', width=2),
            hovertemplate='Hora: %{x|%H:%M}<br>Temp: %{y}°C<extra></extra>'
        ))

        # Trace de Humedad (Eje Y secundario)
        fig.add_trace(go.Scatter(
            x=fechas_dt,
            y=humedad_forecast,
            mode='lines',
            name='Humedad (%)',
            yaxis="y2", # MUY IMPORTANTE: Asigna al eje y2
            line=dict(color='cyan', width=2, dash='dot'),
            fill='tozeroy',
            hovertemplate='Hora: %{x|%H:%M}<br>Humedad: %{y}%<extra></extra>'
        ))

        fig.update_layout(
            title=f'Pronóstico 24h para ({lat}, {lon})',
            xaxis_title='Fecha y Hora',
            yaxis_title='Temperatura (°C)',
            yaxis=dict(
                color='orange'
            ),
            # Definición del eje Y secundario
            yaxis2=dict(
                title='Humedad (%)',
                overlaying='y', # Superpone sobre el eje 'y'
                side='right',   # Lo pone a la derecha
                color='cyan',
                showgrid=False # Oculta la grilla para no sobrecargar
            ),
            plot_bgcolor='white', 
            paper_bgcolor='white', 
            legend=dict(x=0.01, y=0.98, bgcolor='rgba(255,255,255,0.5)')
        )

        return temp_texto, hum_texto, viento_texto, mensaje, fig

    except Exception as e:
        print(f"Error procesando datos: {e}")
        fig_vacia.add_annotation(text="Error al procesar datos", showarrow=False, font=dict(color="red"))
        return "Error", "Error", "Error", "Error al procesar los datos recibidos.", fig_vacia