import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go


dash.register_page(__name__, path="/clase6", name="clase 6")
app = dash.Dash(__name__)

layout = html.Div([
    # --- Panel Izquierdo (Controles) ---
    html.Div([
    html.H2("Simulador de Modelo SEIR", className="title"),

    html.Div([
        html.Label("Tasa de Transmisión (β):"),
        html.Div([ # Contenedor Flex para alinear Slider e Input
            dcc.Slider(
                id="slider-beta", min=0, max=1.5, step=0.01, value=0.4,
                marks=None, tooltip={"placement": "bottom", "always_visible": False}
            ),
            dcc.Input(
                id="input-beta", type='number', value=0.4, step=0.01, 
                className="input-field", style={'width': '80px', 'marginLeft': '15px'}
            )
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], className="input-group"),

    html.Div([
        html.Label("Tasa de Incubación (σ) (1/días):"),
        html.Div([
            dcc.Slider(
                id="slider-sigma", min=0, max=1, step=0.01, value=0.2, # 0.2 es 1/5 días
                marks=None, tooltip={"placement": "bottom", "always_visible": False}
            ),
            dcc.Input(
                id="input-sigma", type='number', value=0.2, step=0.01, 
                className="input-field", style={'width': '80px', 'marginLeft': '15px'}
            )
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], className="input-group"),

    html.Div([
        html.Label("Tasa de Recuperación (γ) (1/días):"),
        html.Div([
            dcc.Slider(
                id="slider-gamma", min=0, max=1, step=0.01, value=0.1, # 0.1 es 1/10 días
                marks=None, tooltip={"placement": "bottom", "always_visible": False}
            ),
            dcc.Input(
                id="input-gamma", type='number', value=0.1, step=0.01, 
                className="input-field", style={'width': '80px', 'marginLeft': '15px'}
            )
        ], style={'display': 'flex', 'alignItems': 'center'})
    ], className="input-group"),

    html.Hr(style={'border': 'none', 'borderTop': '1px solid var(--color-beige)', 'margin': '25px 0'}),

    html.Div([
        html.Label("Población Total (N):"),
        dcc.Input(id="input-n-poblacion", type='number', value=1000, className="input-field")
    ], className="input-group"),
    
    html.Div([
        html.Label("Infectados Iniciales (I₀):"),
        dcc.Input(id="input-i0", type='number', value=1, className="input-field")
    ], className="input-group"),

    html.Div([
        html.Label("Expuestos Iniciales (E₀):"),
        dcc.Input(id="input-e0", type='number', value=0, className="input-field")
    ], className="input-group"),

    html.Div([
        html.Label("Días a Simular (T):"),
        dcc.Input(id="input-tmax", type='number', value=150, className="input-field")
    ], className="input-group"),

 
    html.Button("Simular Modelo", id="btn-simular", className="btn-generar"),

], className="content left"),

    
    html.Div([
        html.H2("Evolución Temporal del Modelo SEIR", className="title"), 
        dcc.Graph(id="grafica-seir", style={"height":"450", "width":"100%"}),

        html.Div(id='info-seir') 
    ], className="content right") 
], className="main-container") 


app.layout = layout

# --- Callback para actualizar la gráfica SEIR ---
@callback(
    [Output("grafica-seir", "figure"),
     Output("info-seir", "children")],
    Input("btn-simular", "n_clicks"),
    State("input-n-poblacion", "value"),
    State("input-i0", "value"),
    State("input-e0", "value"),
    State("input-beta", "value"),
    State("input-sigma", "value"),
    State("input-gamma", "value"),
    State("input-tmax", "value"),
    prevent_initial_call=False
)





def actualizar_grafica_seir(n_clicks, N, I0, E0, beta, sigma, gamma, t_max):
    

    try:
        N = float(N)
        I0 = float(I0)
        E0 = float(E0)
        beta = float(beta)
        sigma = float(sigma)
        gamma = float(gamma)
        t_max = int(t_max)
        
        dt = 1
        n_steps = t_max
        
        t = np.linspace(0, t_max, n_steps)
        S = np.zeros(n_steps)
        E = np.zeros(n_steps)
        I = np.zeros(n_steps)
        R = np.zeros(n_steps)
        
        S[0] = N - I0 - E0
        E[0] = E0
        I[0] = I0
        R[0] = 0
        
        for i in range(n_steps - 1):
            if S[i] < 0: S[i] = 0
            if E[i] < 0: E[i] = 0
            if I[i] < 0: I[i] = 0
            
            dS_dt = (-beta * I[i] * S[i]) / N
            dE_dt = (beta * I[i] * S[i]) / N - sigma * E[i]
            dI_dt = sigma * E[i] - gamma * I[i]
            dR_dt = gamma * I[i]
            
            S[i+1] = S[i] + dS_dt * dt
            E[i+1] = E[i] + dE_dt * dt
            I[i+1] = I[i] + dI_dt * dt
            R[i+1] = R[i] + dR_dt * dt
            
        R0 = 0
        if gamma > 0:
            R0 = beta / gamma
        
        peak_I = np.max(I)
        peak_day = t[np.argmax(I)]
        
        info_mensajes = [
            html.H4(f"Número Básico de Reproducción (R₀ = β/γ): {R0:.2f}"),
            html.P(f"Pico de infectados (max(I)): {peak_I:.0f} personas (Día {peak_day:.0f})")
        ]

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=E, mode='lines', name='Expuestos (E)', line=dict(color='orange')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='green')
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Simulación SEIR (N={N:.0f}, R₀={R0:.2f})</b>",
                x=0.5, font=dict(size=16, color='green')
            ),
            xaxis_title="Tiempo (Días)",
            yaxis_title="Número de Personas",
            paper_bgcolor="lightyellow",
            plot_bgcolor="white",
            font=dict(family="Outfit", size=12),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        fig.update_xaxes(
            showgrid=True, gridwidth=1, gridcolor='Lightpink',
            zeroline=True, zerolinewidth=2, zerolinecolor='red',
            range=[0, t_max]
        )
        fig.update_yaxes(
            showgrid=True, gridwidth=1, gridcolor='Lightpink',
            zeroline=True, zerolinewidth=2, zerolinecolor='red',
            range=[0, N * 1.1] 
        )
        
        return fig, info_mensajes

    except Exception as error:
        info_mesaje = f"Error en la simulación: {error}"
        return go.Figure(), [html.P(info_mesaje)]
    


if __name__ == '__main__':
    app.run_server(debug=True)