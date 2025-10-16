import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go

from scipy.integrate import solve_ivp # Intallar pip install scipy


dash.register_page(__name__, path="/pagina4", name="pagina 4")

# Función para el modelo de Lotka-Volterra
def lotka_volterra(t, Z, a, b, c, d):
    """
    Sistema de ecuaciones diferenciales para el modelo Lotka-Volterra.
    Z[0] = Presa (P)
    Z[1] = Depredador (D)

    dP/dt = a*P - b*P*D
    dD/dt = -c*D + d*P*D
    """
    P, D = Z
    dPdt = a * P - b * P * D
    dDdt = -c * D + d * P * D
    return [dPdt, dDdt]

# Estructura del layout de la página 4
layout = html.Div([
    # Contenido Izquierdo: Entradas de Parámetros
    html.Div([
        html.H2("Modelo de Lotka-Volterra", className="title"),
        html.P("Simulación de la Dinámica Poblacional Presa-Depredador"),

        html.Div([
            html.H3("Parámetros de la Presa (P)"),
            html.Div([
                html.H4("Población Inicial P(0):", className="input-label"),
                dcc.Input(id="input-p0-lv", type="number", value=10, className="input-field")
            ], className="input-group-item"),
            html.Div([
                html.H4("Tasa de Crecimiento (a):", className="input-label"),
                dcc.Input(id="input-a-lv", type="number", value=1.0, step=0.01, className="input-field")
            ], className="input-group-item"),
            html.Div([
                html.H4("Tasa de Depredación (b):", className="input-label"),
                dcc.Input(id="input-b-lv", type="number", value=0.1, step=0.01, className="input-field")
            ], className="input-group-item"),
        ], className="input-group"),

        html.Div([
            html.H3("Parámetros del Depredador (D)"),
            html.Div([
                html.H4("Población Inicial D(0):", className="input-label"),
                dcc.Input(id="input-d0-lv", type="number", value=5, className="input-field")
            ], className="input-group-item"),
            html.Div([
                html.H4("Tasa de Muerte (c):", className="input-label"),
                dcc.Input(id="input-c-lv", type="number", value=0.5, step=0.01, className="input-field")
            ], className="input-group-item"),
            html.Div([
                html.H4("Tasa de Eficiencia (d):", className="input-label"),
                dcc.Input(id="input-d-lv", type="number", value=0.075, step=0.001, className="input-field")
            ], className="input-group-item"),
        ], className="input-group"),
        
        html.Div([
            html.H4("Tiempo Máximo (t_max):", className="input-label"),
            dcc.Input(id="input-tmax-lv", type="number", value=100, className="input-field")
        ], className="input-group-item full-width"),

        html.Button("Generar Gráfico Lotka-Volterra", id="btn-generar-lv", className="btn-generar")

    ], className="content left"),

    # Contenido Derecho: Gráfico
    html.Div([
        html.Div([
            html.H2("Dinámica Poblacional", className="title"),
        ]),
        dcc.Graph(
            id="graph-output-lv",
            style={'height': '600px', 'width': '100%'},
        ),
    ], className="content right"),

], className="main-container")

@callback(
    Output("graph-output-lv", "figure"),
    Input("btn-generar-lv", "n_clicks"),
    State("input-p0-lv", "value"),
    State("input-a-lv", "value"),
    State("input-b-lv", "value"),
    State("input-d0-lv", "value"),
    State("input-c-lv", "value"),
    State("input-d-lv", "value"),
    State("input-tmax-lv", "value"),
    prevent_initial_call=False
)
def actualizar_grafico_lv(n_clicks, P0, a, b, D0, c, d, t_max):
    # Valores por defecto en caso de inputs nulos o cero (para prevenir errores)
    P0 = P0 if P0 is not None and P0 > 0 else 10
    a = a if a is not None and a > 0 else 1.0
    b = b if b is not None and b > 0 else 0.1
    D0 = D0 if D0 is not None and D0 > 0 else 5
    c = c if c is not None and c > 0 else 0.5
    d = d if d is not None and d > 0 else 0.075
    t_max = t_max if t_max is not None and t_max > 0 else 100

    # Condición inicial [Presa, Depredador]
    Z0 = [P0, D0]

    # Rango de tiempo para la simulación
    t_span = [0, t_max]
    t = np.linspace(t_span[0], t_span[1], 500)

    # Resolver el sistema de EDOs
    sol = solve_ivp(
        lotka_volterra,
        t_span,
        Z0,
        args=(a, b, c, d),
        t_eval=t,
        method='RK45'
    )

    # Extraer las poblaciones
    P_t = sol.y[0]
    D_t = sol.y[1]

    # Crear la figura
    fig = go.Figure()

    # Trazado de la Presa
    fig.add_trace(go.Scatter(
        x=t,
        y=P_t,
        mode='lines',
        name='Presa P(t)',
        line=dict(color='green', width=3),
        hovertemplate='Tiempo: %{x:.2f}<br>Presa: %{y:.2f}<extra></extra>'
    ))

    # Trazado del Depredador
    fig.add_trace(go.Scatter(
        x=t,
        y=D_t,
        mode='lines',
        name='Depredador D(t)',
        line=dict(color='red', width=3),
        hovertemplate='Tiempo: %{x:.2f}<br>Depredador: %{y:.2f}<extra></extra>'
    ))

    # Configuración del layout
    fig.update_layout(
        title=dict(
            text='<b>Modelo de Lotka-Volterra: Dinámica Presa-Depredador</b>',
            font=dict(size=20, color='#0066cc'),
            x=0.5
        ),
        xaxis_title='Tiempo',
        yaxis_title='Población',
        template='plotly_white',
        margin=dict(l=40, r=40, t=70, b=40),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.7)'),
        height=550
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='LightGray',
        zeroline=True, zerolinewidth=2, zerolinecolor='LightGray',
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='LightGray',
        zeroline=True, zerolinewidth=2, zerolinecolor='LightGray',
        rangemode='nonnegative' # Asegura que las poblaciones no sean negativas
    )

    return fig