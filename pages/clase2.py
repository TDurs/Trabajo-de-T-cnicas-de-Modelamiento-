import dash
from dash import html, dcc

dash.register_page(__name__, path ="/pagina2", name="pagina 2")

layout = html.Div(children=[
    html.Div(children=[
        # Cuadro izquierdo - Contenido teórico
        html.Div(children=[
            html.H2("Modelo Depredador-Presa con Difusión", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Markdown("""
Uno de los temas en el área de la biología matemática es determinar y estudiar la dinámica existente entre la interacción de presas y depredadores bajo diversas hipótesis, representados normalmente por sistemas de ecuaciones diferenciales.

Los sistemas tipo depredador–presa exhiben amplios comportamientos dinámicos, los cuales dependen de los parámetros del modelo, que van desde cambios de estabilidad local en puntos de equilibrio hasta la existencia de ciclos límites y órbitas heteroclínicas u homoclínicas.

Al considerar la difusión espacial, en al menos una de las poblaciones, se hace una contribución significativa a la dinámica de las poblaciones, especialmente a la propagación de especies. Según Kuznetsov [6], la interacción de presas \\(0 \\leq u \\leq K\\) y depredadores \\(v \\geq 0\\) puede ser descrita mediante el modelo:

\\[
\\begin{cases}
u_t = D_1 u_{xx} + ru\\left(1 - \\frac{u}{K}\\right) - \\frac{buv}{1 + ev}, \\\\
v_t = D_2 v_{xx} + \\frac{muv}{1 + eu} - dv,
\\end{cases}
\\quad (1)
\\]

con \\(D_1 > 0\\) y \\(D_2 > 0\\) las constantes de difusión de las especies, respectivamente, \\(r > 0\\) la tasa de crecimiento de presas en ausencia de depredación, \\(K > 0\\) la capacidad de carga de las presas, \\(b > 0\\) y \\(m > 0\\) las tasas de encuentro entre las dos especies, \\(e > 0\\) la constante de saturación de las presas y \\(d > 0\\) la tasa de mortalidad de los depredadores.

### Estudio de Ondas Viajeras

Por otro lado, la existencia de soluciones tipo ondas viajeras para modelos tipo depredador-presa con difusión, han sido estudiadas por diversos investigadores. Por ejemplo:

- **Dunbar [1]** prueba la existencia de soluciones tipo onda viajera para un modelo equivalente a (1), con re-escalamiento de variables y reducción de sus parámetros.
- **Wan-Tong [8]** analiza la existencia de ondas viajeras para un modelo equivalente a (1) con funcional de respuesta tipo Holling III.
- **Chufen Wu [11]** estudia un funcional tipo Holling de la forma \\(f(u,v) = \\frac{u^p v}{a + u^p}\\), \\(p > 0\\), y reducción de sus parámetros.

### Contribución de este Trabajo

Al considerar que las presas se distribuyen uniformemente con el fin de simplificar el análisis al modelo (1), esto es \\(D_1 = 0\\), y a diferencia de los trabajos presentados por Chufen Wu [11] y Dunbar [1], en este trabajo se analiza la existencia de soluciones tipo ondas viajeras con re-escalamiento de la variable espacial y **sin reducción de los parámetros** en el modelo sin difusión.

### Metodología

Para ello, se desarrollan los siguientes pasos:

1. **Sección 2**: Se presentan preliminares matemáticos para probar los resultados de este trabajo.
2. **Sección 3**: Análisis cualitativo local y global del modelo (1) sin difusión para determinar los equilibrios espaciales.
3. **Sección 4**: Demostración final de la existencia de soluciones tipo ondas viajeras.
""", mathjax=True, style={'textAlign': 'justify'})
        ], className="graph-box", style={'flex': '1', 'padding': '20px', 'margin': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),

        # Cuadro derecho - Gráfica y simulación
        html.Div(children=[
            html.H2("Simulación del Modelo", style={'textAlign': 'center', 'color': '#2c3e50'}),
            html.P("Aquí se mostrarán las simulaciones numéricas del sistema depredador-presa y las soluciones de onda viajera.", 
                   style={'textAlign': 'center', 'marginBottom': '20px'}),
            
            # Selector de tipo de gráfica
            html.Div([
                html.Label("Seleccionar tipo de simulación:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='simulation-type',
                    options=[
                        {'label': 'Dinámica Temporal', 'value': 'temporal'},
                        {'label': 'Ondas Viajeras', 'value': 'traveling'},
                        {'label': 'Planos de Fase', 'value': 'phase'}
                    ],
                    value='temporal',
                    style={'marginBottom': '20px'}
                )
            ]),
            
            # Gráfica principal con tamaño limitado
            html.Div([
                dcc.Graph(
                    id='predator-prey-plot',
                    figure={
                        'data': [
                            {'x': [0, 1, 2, 3, 4, 5], 'y': [2, 1.5, 1.2, 1.8, 1.4, 1.6], 'type': 'line', 'name': 'Presas (u)', 'line': {'color': '#3498db'}},
                            {'x': [0, 1, 2, 3, 4, 5], 'y': [1, 1.8, 1.5, 1.2, 1.7, 1.3], 'type': 'line', 'name': 'Depredadores (v)', 'line': {'color': '#e74c3c'}},
                        ],
                        'layout': {
                            'title': 'Dinámica Temporal del Sistema Depredador-Presa',
                            'xaxis': {'title': 'Tiempo'},
                            'yaxis': {'title': 'Población'},
                            'plot_bgcolor': '#ecf0f1',
                            'paper_bgcolor': '#ffffff',
                            'font': {'color': '#2c3e50'},
                            'height': 400,  # Altura fija
                            'margin': {'l': 50, 'r': 50, 't': 60, 'b': 50}  # Márgenes ajustados
                        }
                    },
                    config={'displayModeBar': True, 'displaylogo': False},
                    style={'height': '400px'}  # Altura fija en el estilo
                )
            ], style={'height': '400px', 'marginBottom': '20px'}),  # Contenedor con altura fija
            
            # Parámetros del modelo
            html.Div([
                html.H4("Parámetros del Modelo", style={'marginTop': '20px', 'color': '#2c3e50'}),
                html.Ul([
                    html.Li("r = Tasa de crecimiento de presas"),
                    html.Li("K = Capacidad de carga"),
                    html.Li("b, m = Tasas de encuentro"),
                    html.Li("e = Constante de saturación"),
                    html.Li("d = Tasa de mortalidad"),
                ], style={'textAlign': 'left'})
            ])
        ], className="graph-box", style={'flex': '1', 'padding': '20px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '20px', 'padding': '20px'})
])