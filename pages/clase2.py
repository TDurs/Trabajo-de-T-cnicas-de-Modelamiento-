import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np 
import plotly.graph_objects as go

dash.register_page(__name__, path ="/pagina2", name="pagina 2")



layout = html.Div([
    #Contenido Izquierdo
    html.Div([
        html.H2("Esta es la pagina 2", className="title"),
        
        
        html.Div([
            html.H2("Poblacion inicial P(0):"),
            dcc.Input(id="input-p0", type="number", value=200, className="input-field")               
        ], className="input-group"),
        
        html.Div([
            html.H2("Tasa de crecimiento (r):"),
            dcc.Input(id="input-r", type="number", value=0.04, className="input-field")
               
        ], className="input-group"),
        
        html.Div([
            html.H2("Poblacion inicial (k):"),
            dcc.Input(id="input-k", type="number", value=750, className="input-field")
               
        ], className="input-group"),
        
        html.Div([
            html.H2("Poblacion inicial (t):"),
            dcc.Input(id="input-t", type="number", value=100, className="input-field")
               
        ], className="input-group"),
        
        html.Button("Generar Grafico", id="btn-generar",  className="btn-generar")
        
    ],className="content left"),
    
    #Contenido Derecho
    html.Div([
        html.Div([
            html.H2("Grafico", className="title"),
        ]),
        dcc.Graph(
        id="graph-output", 
        style={'height': '500px', 'width': '100%'},
        ),
        
    ],className="content right"),
    
    
        
    
],className="main-container")

@callback(
    Output("graph-output", "figure"),
    Input("btn-generar", "n_clicks"),
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),
    State("input-t", "value"),
    prevent_initial_call=False
)

def actualizar_grafico(n_clicks, P0, r, K, t_max):
    # Generar los valores el tiempo
    t = np.linspace(0, t_max, 20)
    
    # Ecuacion
    P = (P0 * K * np.exp(r * t)) / ((K - P0) + P0 * np.exp(r * t))
    
    # Crear la figura
    trace_poblacion = go.Scatter(
        x=t, 
        y=P, 
        mode='lines+markers', 
        name='P(t)',
        line=dict(
            color='blue',
            width=2
                  ),
        marker=dict(
            size=6, 
            color='blue', 
            symbol='circle'
            ),
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )
    
    # Crear grafico de la capacidad de carga
    trace_capacidad = go.Scatter(
        x=[0, t_max], 
        y=[K, K], 
        mode='lines', 
        name='Capacidad de Carga (K)',
        line=dict(
            color='red',
            width=2,
            dash='dash'
        ),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )
    
    fig = go.Figure(data=[trace_poblacion, trace_capacidad])
    
    
    fig.update_layout(
    title=dict(
        text='<b>Crecimiento Exponencial de la Población</b>',
        font=dict(
            size=20,
            color='red'
            ),
            x=0.5,
            y=1.0,
        ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=70, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(
        family="Outfit",
        size=12, 
        color='black'
        ),
    height=350
)
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='LightGray',
        zeroline=True, zerolinewidth=2, zerolinecolor='LightGray',
        showline=True, linewidth=2, linecolor='Black', mirror=True,
    )
    
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='LightGray',
        zeroline=True, zerolinewidth=2, zerolinecolor='LightGray',
        showline=True, linewidth=2, linecolor='Black', mirror=True,
    )
    
    return fig