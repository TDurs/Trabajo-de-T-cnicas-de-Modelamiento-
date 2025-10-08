import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path="/pagina3", name="pagina 3")

# Datos para los gráficos (ejemplo - puedes ajustar con tus datos reales)
# Gráfico 1: Modelo Lotka-Volterra simple
t = np.linspace(0, 50, 500)
# Presa
x1 = 1 + 0.9 * np.sin(0.3 * t) * np.exp(0.02 * t)
# Depredador
y1 = 0.5 + 0.7 * np.cos(0.3 * t - 1) * np.exp(0.02 * t)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=t, y=x1, mode='lines', name='Presas', line=dict(color='green', width=2)))
fig1.add_trace(go.Scatter(x=t, y=y1, mode='lines', name='Depredadores', line=dict(color='red', width=2)))
fig1.update_layout(
    title='Modelo Lotka-Volterra: Presa vs Depredador',
    xaxis_title='Tiempo',
    yaxis_title='Población',
    template='plotly_white'
)

# Gráfico 2: Modelo con múltiples especies
t2 = np.linspace(0, 40, 400)
# Dos presas y un depredador
presa1 = 0.8 + 0.6 * np.sin(0.4 * t2) * np.exp(0.015 * t2)
presa2 = 0.6 + 0.5 * np.sin(0.35 * t2 + 1) * np.exp(0.01 * t2)
depredador = 0.4 + 0.4 * np.cos(0.38 * t2 - 0.5) * np.exp(0.018 * t2)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=t2, y=presa1, mode='lines', name='Frankliniella occidentalis', line=dict(color='blue', width=2)))
fig2.add_trace(go.Scatter(x=t2, y=presa2, mode='lines', name='Bemisia tabaci', line=dict(color='orange', width=2)))
fig2.add_trace(go.Scatter(x=t2, y=depredador, mode='lines', name='Macrolophus caliginosus', line=dict(color='red', width=2)))
fig2.update_layout(
    title='Modelo Multi-Especies: Dos Presas y un Depredador',
    xaxis_title='Tiempo (semanas)',
    yaxis_title='Densidad de Población',
    template='plotly_white'
)

layout = html.Div([
    # Introducción en la parte superior
    html.Div([
        html.H2("Modelos matemáticos de depredador-presa en cultivos hortícolas en invernadero en el Sudeste de la Península Ibérica"),
        dcc.Markdown("""
En el estudio de la dinámica de población de las especies plaga dentro del cultivo, es fundamental considerar los sistemas depredador-presa, parasitoide-hospedante y patógeno-hospedante, según sea el tipo de enemigo natural en el que estemos interesados (depredador, parasitoide o patógeno). En relación con la descripción del sistema depredador-presa (o parasitoide-hospedante), numerosos trabajos han abordado el tema desde un punto de vista matemático; especialmente destacan los trabajos iniciales de LOTKA (1925), VOLTERRA (1926), NICHOLSON (1933) y NICHOLSON y BAILEY (1935); así como los posteriores de SOLOMON (1949), WATT (1959), HOLLING (1959, 1963, 1966), HASSELL (1966), ROYAMA (1971), HUFFAKER y STINNER (1971) y CURRY y DeMICHELE (1977).

En la actualidad, se han revisado los trabajos realizados sobre la relación depredador-presa, especialmente cuando se aplican, como en el presente caso, a insectos plaga (MILLS y GETZ, 1996).

Las aplicaciones prácticas de la relación depredador-presa para el estudio de la importancia del control natural en la dinámica de población de las especies plaga, así como en la utilización de la lucha biológica, se señalaron mucho después de su desarrollo matemático (HASSELL y WAAGE, 1984; HASSELL, 1988; MAY y HASSELL, 1988; MACKAUER et al., 1990); por lo tanto, pocos han sido los trabajos que han abordado este aspecto aplicado. En el caso de la evaluación del control natural, debemos señalar los trabajos sobre tres grupos de especies plaga: áfidos (GUTIÉRREZ et al., 1984), ácaros (SABELIS, 1985) y tisanópteros (LEWIS, 1997).
        """, mathjax=True)
    ], className="content introduccion"),

    # Primera fila: descripción y gráfico
    html.Div([
        html.Div([
            html.H3("Modelo de Lotka-Volterra: Caso Simple"),
            dcc.Markdown("""
**Contexto Experimental:**
- **Especie plaga:** *Frankliniella occidentalis*
- **Depredador:** *Orius* sp.
- **Cultivo:** Pimiento (variedad California)
- **Ubicación:** La Mojonera (Almería)
- **Periodos:** Campañas 1991/92 y 1997/98

**Metodología del Ensayo 1:**
- Invernadero de 2,000 m² con pimiento variedad Tango
- Marco de plantación: 2 plantas por m²
- Periodo: 08/08/91 al 26/11/91 (10 muestreos semanales)
- Muestreo: 108 frutos por parcela
- Liberación depredador: 1 individuo/m² en 5 fechas diferentes

**Metodología del Ensayo 2:**
- Invernadero de 3,500 m² con cultivo hidropónico
- Muestreo quincenal en flores y hojas
- 15 plantas fijas + 5 plantas al azar durante 30 semanas
- Liberación única en semana décima
            """, mathjax=True),
        ], className="content left"),
        
        html.Div([
            html.H3("Dinámica Poblacional: Presa-Depredador"),
            dcc.Graph(
                figure=fig1,
                style={'height': '500px', 'width': '100%'}
            ),
            dcc.Markdown("""
**Interpretación del Gráfico:**
- **Línea verde:** Población de *Frankliniella occidentalis* (presa)
- **Línea roja:** Población de *Orius* sp. (depredador)
- Se observa el comportamiento cíclico característico del modelo Lotka-Volterra
            """, mathjax=True)
        ], className="content right"),
    ], className="main-container"),

    # Segunda fila: ecuaciones y gráfico
    html.Div([
        html.Div([
            html.H3("Modelo Extendido: Múltiples Especies"),
            dcc.Markdown(r"""
**Contexto Experimental:**
- **Especies plaga:** *Helicoverpa armígera* y *Bemisia tabaci*
- **Depredador:** *Macrolophus caliginosus*
- **Cultivo:** Tomate (variedad Daniela)
- **Ubicación:** Mazarrón (Murcia)
- **Periodo:** Campaña 1996/97

**Metodología:**
- Invernadero de 4,620 m²
- Marco de plantación: 2 plantas por m²
- Muestreo semanal durante 20 semanas
- 15 plantas fijas + 5 plantas al azar
- Liberación depredador: 1 por planta en semana octava

**Modelo Matemático:**

Para el caso de n-presas y un depredador, el sistema diferencial autónomo es:

$$
\begin{align*}
x_i' &= x_i \left[ a_i - \sum_{j=1}^n b_{ij} x_j - d_i y \right], \quad 1 \leq i \leq n \\
y' &= y \left[ \alpha + \sum_{i=1}^n \beta_i x_i - \gamma y \right]
\end{align*}
$$

**Parámetros:**
- $\alpha, \beta_i, d_i, \gamma > 0,\ 1 \leq i \leq n$
- $b_{ii} > 0 > b_{ij},\ \forall i \neq j$

**Variables:**
- $x_i$: Densidad de población de la especie presa $(i)$
- $y$: Densidad de población del depredador
- $a_i, \alpha$: Tasas de crecimiento intrínseco
- $b_{ij}$: Tasa de competencia entre especies $x_i$ y $x_j$
- $\gamma$: Tasa de competencia intra-específica del depredador
- $d_i$: Tasa de depredación
- $\beta_i$: Beneficio del depredador por convivencia con presas
            """, mathjax=True),
        ], className="content left"),
        
        html.Div([
            html.H3("Dinámica Multi-Especies"),
            dcc.Graph(
                figure=fig2,
                style={'height': '500px', 'width': '100%'}
            ),
            dcc.Markdown("""
**Interpretación del Gráfico:**
- **Línea azul:** *Helicoverpa armígera* (presa 1)
- **Línea naranja:** *Bemisia tabaci* (presa 2)
- **Línea roja:** *Macrolophus caliginosus* (depredador)
- Se observan interacciones complejas entre las tres especies
            """, mathjax=True)
        ], className="content right"),
    ], className="main-container"),

], className="page-container")