import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

#############################################

P0 = 100
r = 0.03
t = np.linspace(0, 100, 100)
P = P0 * np.exp(r * t)

# Crear un scatter plot CORREGIDO
trace = go.Scatter(
    x=t,
    y=P,
    mode='lines+markers',  # CORREGIDO: 'markes' -> 'markers'
    line=dict(
        dash='dot',
        color='black', 
        width=2),
    
    marker=dict(  # CORREGIDO: 'market' -> 'marker'
        color='blue',
        symbol='square',
        size=8
    ),
    name='P(t) = P0 * e^(rt)',
    hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'  # CORREGIDO: %{x:2f} -> %{x:.2f}
)

# Crear la figura 
fig = go.Figure(data=trace)  

# Mejorar el layout de la figura
fig.update_layout(
    title=dict(
        text='<b>Crecimiento Exponencial de la Población</b>',
        font=dict(
            size=20,
            color='red'
            ),
            x=0.5,
            y=0.9,
        ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    height=350
)

#############################################

dash.register_page(__name__, path="/pagina1", name="pagina 1")

layout = html.Div(children=[
    # Contenedor Principal que contiene izquierdo y derecho
   
        # Contenedor Izquierdo
        html.Div(children=[
            html.H2("Crecimiento de la población y capacidad de carga"),
            
            dcc.Markdown("""
        Para modelar el crecimiento de la población mediante una ecuación diferencial, primero tenemos que introducir algunas variables y términos relevantes. 

        La variable \\( t \\) representará el tiempo. Las unidades de tiempo pueden ser horas, días, semanas, meses o incluso años. Cualquier problema dado debe especificar las unidades utilizadas en ese problema en particular. 

        La variable \\( P \\) representará a la población. Como la población varía con el tiempo, se entiende que es una función del tiempo. Por lo tanto, utilizamos la notación \\( P(t) \\) para la población en función del tiempo. Si \\( P(t) \\) es una función diferenciable, entonces la primera derivada \\(\\frac{dP}{dt}\\) representa la tasa instantánea de cambio de la población en función del tiempo.

        En Crecimiento y decaimiento exponencial, estudiamos el crecimiento y decaimiento exponencial de poblaciones y sustancias radiactivas. Un ejemplo de función de crecimiento exponencial es \\( P(t) = P_0 e^{rt} \\). 

        En esta función:
        - \\( P(t) \\) representa la población en el momento \\( t \\)
        - \\( P_0 \\) representa la **población inicial** (población en el tiempo \\( t = 0 \\))
        - La constante \\( r > 0 \\) se denomina **tasa de crecimiento**

        La Figura 4.18 muestra un gráfico de \\( P(t) = 100e^{0.03t} \\). Aquí \\( P_0 = 100 \\) y \\( r = 0.03 \\).
        """, mathjax=True)
        ], className="content left"),

        # Contenedor Derecho
        html.Div(children=[
            html.H2("Gráfica", className="title"),
            dcc.Graph(
                figure=fig,
                style={'height': '350px', 'width': '100%'}
            )
        ], className="content right")
], className="main-container")