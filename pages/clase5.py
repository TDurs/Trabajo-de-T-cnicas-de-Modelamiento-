import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path="/pagina5", name="pagina 5")

layout = html.Div([
    html.Div([
        html.H2("Campo Vectorial 2D", className="title"),

        html.Div([
            html.Label("Ecuación dx/dt = "),
            dcc.Input(id="input-fx", type='text', value="np.sin(X)", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Ecuación dy/dt = "),
            dcc.Input(id="input-fy", type='text', value="np.cos(X)", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango del Eje X:"),
            dcc.Input(id="input-xmax", type='number', value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango del Eje Y:"),
            dcc.Input(id="input-ymax", type='number', value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Mallado"),
            dcc.Input(id="input-n", type='number', value=15, className="input-field")
        ], className="input-group"),

        html.Button("Generar campo", id="btn-generar", className="btn-generar"),

        # Ejemplos
        html.Div([
            html.H3("Ejemplos para probar: "),
            html.P("• dx/dt = X, dy/dt = Y"),
            html.P("• dx/dt = -Y, dy/dt = X"),
            html.P("• dx/dt = X+Y, dy/dt = np.cos(Y)"),
        ])
    ], className="content left"),

    html.Div([
        html.H2("Visualización del Campo Vectorial", className="title"),
        dcc.Graph(id="grafica-campo", style={"height":"450", "width":"100%"}),

        html.Div(id='info-campo')
    ], className="content right")
], className="main-container")


#callbacks
@callback(
    [Output("grafica-campo", "figure"),
     Output("info-campo", "children")],
    Input("btn-generar", "n_clicks"),
    State("input-fx", "value"),
    State("input-fy", "value"),
    State("input-xmax", "value"),
    State("input-ymax", "value"),
    State("input-n", "value"),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, fx_str, fy_str, xmax, ymax, n):
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    info_mesaje = ""
    
    try:
        diccionario ={
            'X': X,
            'Y': Y,
            'np': np,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'e': np.e
            
        }
        fx = eval(fx_str, diccionario)
        fy = eval(fy_str, diccionario)

        mag = np.sqrt(fx**2 + fy**2)
        mag_max = np.max(mag)
        mag_min = np.min(mag)
        info_mesaje = f"Magnitud: min = {mag_min:.2f}, max = {mag_max:.2f}"
        
    except Exception as error:
        fx = np.zeros_like(X)
        fy = np.zeros_like(Y)
        info_mesaje = f"Error en las ecuaciones: {error}"
        
    fig = go.Figure()
    
    for i in range(n):
        for j in range(n):
            x0, y0 = X[i, j], Y[i, j]
            x1, y1 = x0 + fx[i, j], y0 + fy[i, j] 
            
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines+markers',
                line=dict(color='blue', width=2),
                marker=dict(size=[3, 5], color=['blue', "red"]), 
                showlegend=False,
                hovertemplate=f"Punto: ({x0:.1f}, {y0:.1f})<br>Vector: ({fx[i,j]:.2f}, {fy[i,j]:.2f})"
            ))

    fig.update_layout(
        title=dict(
            text=f"<b>Campo Vectorial: dx/dt ={fx_str}, dy/dt = {fy_str}</b>",
            x=0.5, font=dict(size=16, color='green')
        ),
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        paper_bgcolor="lightyellow",
        plot_bgcolor="white",
        font=dict(family="Outfit", size=12),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='Lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        range=[-xmax*1.1, xmax*1.1]
    )
    
    
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='Lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        range=[-ymax*1.1, ymax*1.1],
        scaleanchor="x", 
        scaleratio=1
    )
    
    return fig, info_mesaje
        
            
            