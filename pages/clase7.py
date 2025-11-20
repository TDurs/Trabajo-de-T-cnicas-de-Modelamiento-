import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go


dash.register_page(__name__, path="/trabajoaparte", name="Extra", order=7)

layout = html.Div([
    # --- Panel Izquierdo (Controles) ---
    html.Div([
        html.H2("Modelo de Rumor (SIR)", className="title"),

        # --- Grupo de Sliders Interactivos ---
        html.Div([
            html.Label("Tasa de Infección (b):"),
            html.Div([
                # Sliders ajustados a valores muy pequeños porque la ecuación es b*S*I
                dcc.Slider(
                    id="slider-b", min=0, max=0.01, step=0.0001, value=0.002,
                    marks=None, tooltip={"placement": "bottom", "always_visible": False}
                ),
                dcc.Input(
                    id="input-b", type='number', value=0.002, step=0.0001, 
                    className="input-field", style={'width': '90px', 'marginLeft': '15px'}
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de Curación/Convencimiento (k):"),
            html.Div([
                dcc.Slider(
                    id="slider-k", min=0, max=0.01, step=0.0001, value=0.001,
                    marks=None, tooltip={"placement": "bottom", "always_visible": False}
                ),
                dcc.Input(
                    id="input-k", type='number', value=0.001, step=0.0001, 
                    className="input-field", style={'width': '90px', 'marginLeft': '15px'}
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], className="input-group"),

        html.Hr(style={'border': 'none', 'borderTop': '1px solid var(--color-beige)', 'margin': '25px 0'}),

        # --- Grupo de Condiciones Iniciales ---
        html.Div([
            html.Label("Población Total (N):"),
            dcc.Input(id="input-n-poblacion", type='number', value=1000, className="input-field")
        ], className="input-group"),
        
        html.Div([
            html.Label("Propagadores Iniciales (I₀):"),
            dcc.Input(id="input-i0", type='number', value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Racionales Iniciales (R₀):"),
            html.P("Necesario > 0 para iniciar la cura", style={'fontSize':'0.8em', 'color':'gray', 'margin':'0'}),
            dcc.Input(id="input-r0", type='number', value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo a Simular (t):"),
            dcc.Input(id="input-tmax", type='number', value=100, className="input-field")
        ], className="input-group"),

        html.Button("Simular Rumor", id="btn-simular", className="btn-generar"),

        html.Div([
            html.H3("Ecuaciones:"),
            html.P("dS/dt = -bSI"),
            html.P("dI/dt = bSI - kIR"),
            html.P("dR/dt = kIR"),
        ], style={"marginTop": "20px", "color": "var(--color-text-light)"})

    ], className="content left"),

    # --- Panel Derecho (Gráfica e Info) ---
    html.Div([
        html.H2("Dinámica de Propagación del Rumor", className="title"),
        dcc.Graph(id="grafica-rumor", style={"height":"450", "width":"100%"}),
        html.Div(id='info-rumor') 
    ], className="content right")
], className="main-container")


# ==========================================================
# CALLBACKS DE SINCRONIZACIÓN (Slider <-> Input)
# ==========================================================
@callback(Output("input-b", "value"), Input("slider-b", "value"))
def sync_b_slider(val): return val

@callback(Output("slider-b", "value"), Input("input-b", "value"))
def sync_b_input(val): return val

@callback(Output("input-k", "value"), Input("slider-k", "value"))
def sync_k_slider(val): return val

@callback(Output("slider-k", "value"), Input("input-k", "value"))
def sync_k_input(val): return val

# ==========================================================
# CALLBACK PRINCIPAL (Lógica del Modelo)
# ==========================================================
@callback(
    [Output("grafica-rumor", "figure"),
     Output("info-rumor", "children")],
    Input("btn-simular", "n_clicks"),
    State("input-n-poblacion", "value"),
    State("input-i0", "value"),
    State("input-r0", "value"),
    State("input-b", "value"),
    State("input-k", "value"),
    State("input-tmax", "value"),
    prevent_initial_call=False
)
def actualizar_grafica_rumor(n_clicks, N, I0, R0, b, k, t_max):
    try:
        # Conversión de tipos
        N = float(N)
        I0 = float(I0)
        R0 = float(R0)
        b = float(b)
        k = float(k)
        t_max = int(t_max)
        
        # S0 se calcula restando el resto
        S0 = N - I0 - R0
        
        # Configuración del Solver Euler
        dt = 0.1 # Paso de tiempo más fino para precisión
        n_steps = int(t_max / dt)
        t = np.linspace(0, t_max, n_steps)
        
        S = np.zeros(n_steps)
        I = np.zeros(n_steps)
        R = np.zeros(n_steps)
        
        S[0], I[0], R[0] = S0, I0, R0
        
        # --- Bucle Principal (Tus Ecuaciones) ---
        for i in range(n_steps - 1):
            # Variables actuales
            St, It, Rt = S[i], I[i], R[i]
            
            # Ecuaciones Diferenciales
            # dS/dt = -bSI
            dS = -b * St * It
            
            # dI/dt = bSI - kIR
            dI = (b * St * It) - (k * It * Rt)
            
            # dR/dt = kIR
            dR = k * It * Rt
            
            # Método de Euler (actualización)
            S[i+1] = St + dS * dt
            I[i+1] = It + dI * dt
            R[i+1] = Rt + dR * dt
            
            # Corrección para no tener poblaciones negativas
            if S[i+1] < 0: S[i+1] = 0
            if I[i+1] < 0: I[i+1] = 0
            if R[i+1] < 0: R[i+1] = 0

        # Estadísticas
        peak_I = np.max(I)
        peak_day = t[np.argmax(I)]
        final_R = R[-1]
        final_S = S[-1]

        info_mensajes = [
            html.Div([
                html.H4(f"Resultados Finales"),
                html.P(f"Máximo de Propagadores: {int(peak_I)} (Día {peak_day:.1f})"),
                html.P(f"Alumnos que NUNCA creyeron (S final): {int(final_S)}"),
                html.P(f"Total de Convencidos/Racionales (R final): {int(final_R)}"),
            ])
        ]

        # Gráfica
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (No saben)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Propagadores (Creen)', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Racionales (No creen)', line=dict(color='green')))
        
        fig.update_layout(
            title=dict(text=f"<b>Modelo de Rumor (b={b}, k={k})</b>", x=0.5, font=dict(color='var(--color-dark)')),
            xaxis_title="Tiempo",
            yaxis_title="Población",
            paper_bgcolor="var(--color-cream)",
            plot_bgcolor="white",
            font=dict(family="Outfit", size=12),
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=True, gridcolor='var(--color-light-blue)')
        fig.update_yaxes(showgrid=True, gridcolor='var(--color-light-blue)')
        
        return fig, info_mensajes

    except Exception as e:
        return go.Figure(), html.Div(f"Error: {str(e)}")

if __name__ == '__main__':
    app.run_server(debug=True)