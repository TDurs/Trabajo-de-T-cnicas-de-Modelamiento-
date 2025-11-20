import dash
from dash import html, dcc, callback, Input, Output, State
# import numpy as np  <- Eliminado (no se usa)
import plotly.graph_objects as go
import requests
from datetime import datetime

def formatear_numero(numero):
    """
    Convierte un número (ej: 1234567) en una cadena 
    de texto con comas (ej: "1,234,567").
    """
    if numero is None:
        return "N/A"
    try:
        return f"{int(numero):,}"
    except (ValueError, TypeError):
        # Si no se puede formatear, lo devuelve como texto
        return str(numero)

dash.register_page(__name__, path='/pagina8', name='covid-19', order=8)

layout = html.Div([
    
    html.Div([
        html.H2("Dashboard Covid-19", className="title"),

        html.Div([
            html.Label("Seleccione el país:"),
            dcc.Dropdown(
                id="dropdown-pais",
                options=[
                    {"label": "Perú", "value": "Peru"},
                    {"label": "México", "value": "Mexico"},
                    {"label": "Estados Unidos", "value": "USA"},
                    {"label": "Canadá", "value": "Canada"}
                ],
                value="Peru", 
                className="input-field",
                # style={"width": "100%"} <- Movido a CSS
            )
        ], className="input-group"),

        html.Div([
            html.Label("Días historico"),
            dcc.Dropdown(
                id="dropdown-dias-covid",
                options=[
                    {"label": "30 días", "value": 30},
                    {"label": "60 días", "value": 60},
                    {"label": "90 días", "value": 90},
                    {"label": "120 días", "value": 120},
                    {"label": "Todo el histórico", "value": "all"}
                ],
                value=30,
                className="input-field",
                # style={"width": "100%"} <- Movido a CSS
            )
        ], className="input-group"),

        html.Button("Actualizar Datos", id="btn-actualizar-covid", className="btn-generar"),

        html.Div(
            id="info-actualizado-covid"
        )

    ], className="content left"), 

    html.Div([
        html.H2("Estadísticas en tiempo real", className="title"),

        html.Div([
            html.H4("Total Casos", className="kpi-card-title kpi-casos"),
            html.H3(id="total-casos", className="kpi-card-value kpi-casos-val")
        ], className="kpi-card"),

        html.Div([
            html.H4("Casos nuevos", className="kpi-card-title kpi-nuevos"),
            html.H3(id="casos-nuevos", className="kpi-card-value kpi-nuevos-val")
        ], className="kpi-card"),

        html.Div([
            html.H4("Total muertes", className="kpi-card-title kpi-muertes"),
            html.H3(id="total-muertes", className="kpi-card-value kpi-muertes-val")
        ], className="kpi-card"),

        html.Div([
            html.H4("Recuperados", className="kpi-card-title kpi-recuperados"),
            html.H3(id="total-recuperados", className="kpi-card-value kpi-recuperados-val")
        ], className="kpi-card"),
        # --- Fin de Tarjetas KPI ---

        html.Div([
            dcc.Graph(id="grafica-covid")
        ], className="graph-box") 

    ], className="content right") 
], className="main-container")

def obtener_datos_pais(pais):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos del país: {e}")
        return None

def obtener_historico_pais(pais, dias):
    try:
        
        dias_param = "all" if dias == "all" else str(dias)
        url = f"https://disease.sh/v3/covid-19/historical/{pais}"
        params = {"lastdays": dias_param}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener histórico del país ({pais}): {e}")
        return None

@callback(
    Output("total-casos", "children"),
    Output("casos-nuevos", "children"),
    Output("total-muertes", "children"),
    Output("total-recuperados", "children"),
    Output("grafica-covid", "figure"), 
    Output("info-actualizado-covid", "children"),
    Input("btn-actualizar-covid", "n_clicks"),
    State("dropdown-pais", "value"),
    State("dropdown-dias-covid", "value"),
    prevent_initial_call=False 
)
def actualizar_dashboard_covid(n_clicks, pais, dias):
    datos_actuales = obtener_datos_pais(pais)
    historico = obtener_historico_pais(pais, dias)

    # Manejo de error si la API falla
    if not datos_actuales or not historico:
        fig = go.Figure()
        fig.add_annotation(
            text="Error al obtener datos",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=15, color="red")
        )
        fig.update_layout(
            paper_bgcolor="lightcyan",
            plot_bgcolor="white"
        )
        
        return "N/A", "N/A", "N/A", "N/A", fig, "No se pudieron actualizar los datos."

    total_casos = datos_actuales.get("cases", 0)
    casos_hoy = datos_actuales.get("todayCases", 0)
    total_muertes = datos_actuales.get("deaths", 0)
    total_recuperados = datos_actuales.get("recovered", 0)

    total_casos_texto = formatear_numero(total_casos) 
    casos_hoy_texto = formatear_numero(casos_hoy)
    total_muertes_texto = formatear_numero(total_muertes)
    total_recuperados_texto = formatear_numero(total_recuperados)


    # --- INICIO DE CORRECCIÓN DE BUG ---
    
    timeline = historico.get("timeline") or {} 
    
    # --- FIN DE CORRECCIÓN DE BUG ---

    casos_historicos = timeline.get("cases", {})
    muertes_historicas = timeline.get("deaths", {})

    fechas = list(casos_historicos.keys())
    valores_casos = list(casos_historicos.values())
    valores_muertes = list(muertes_historicas.values())
    
    if not fechas:
        fig = go.Figure()
        fig.add_annotation(text=f"No hay datos históricos para {pais}.", 
                            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return total_casos_texto, casos_hoy_texto, total_muertes_texto, total_recuperados_texto, fig, "Datos actuales cargados (sin histórico)."

    fechas_dt = [datetime.strptime(fecha, "%m/%d/%y") for fecha in fechas]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_casos,
        mode='lines',
        name='Casos Totales',
        line=dict(color='orange', width=2),
        fill='tozeroy', # Rellena el área bajo la línea
        hovertemplate='Fecha: %{x|%d %b %Y}<br>Casos: %{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_muertes,
        mode='lines',
        name='Muertes Totales',
        line=dict(color='red', width=2),
        hovertemplate='Fecha: %{x|%d %b %Y}<br>Muertes: %{y:,}<extra></extra>'
    ))

    fig.update_layout(
        title=f'Histórico de Casos y Muertes en {pais}',
        xaxis_title='Fecha',
        yaxis_title='Número de Personas',
        plot_bgcolor='white', 
        paper_bgcolor='white', 
        legend=dict(x=0.01, y=0.98, bgcolor='rgba(255,255,255,0.5)') 
    )

    mensaje_actualizacion = f"Datos actualizados para {pais}."
    
    
    return(
        total_casos_texto, 
        casos_hoy_texto, 
        total_muertes_texto, 
        total_recuperados_texto, 
        fig, 
        mensaje_actualizacion
        
    )