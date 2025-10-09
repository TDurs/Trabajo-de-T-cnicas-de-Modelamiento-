import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div([
    html.H1("Bienvenido a Mi Portafolio", className="app-header"),
    
    # Sección de presentación personal
    html.Div([
        # Contenedor para imagen y texto lado a lado
        html.Div([
            # Imagen
            html.Div([
                html.Img(
                    src="/assets/Image/foto1.jpg",  # Asegúrate de tener esta imagen en la carpeta assets
                    alt="Mi Foto",
                    className="profile-image"
                )
            ], className="image-container"),
            
            # Texto de presentación
            html.Div([
                html.H2("Hola, soy Juan Jose", className="profile-name"),
                html.P("Desarrollador Python | Científico de Datos | Estudiante de Modelamiento", 
                       className="profile-title"),
                html.P("""
                    Soy un apasionado por la tecnología y el análisis de datos. Actualmente me encuentro 
                    expandiendo mis conocimientos en modelamiento matemático y desarrollo de aplicaciones 
                    interactivas para la visualización de datos.
                """, className="profile-description"),
                
                html.Div([
                    html.Span(" Lima, Perú"),
                    html.Span(" UNMSM"),
                    html.Span(" Python, Dash, Plotly")
                ], className="profile-tags")
                
            ], className="text-container")
        ], className="profile-container"),
        
        # Sección de aspiraciones y carrera
        html.Div([
            html.H3("Mi Carrera y Aspiraciones", className="section-title"),
            html.Div([
                html.Div([
                    html.H4("Mis Objetivos"),
                    html.P("""
                        Aspiro a convertirme en un especialista en modelamiento matemático y ciencia de datos, 
                        aplicando mis conocimientos para resolver problemas complejos en diversos campos como 
                        la economía, biología y ingeniería. Mi meta es contribuir al desarrollo de soluciones 
                        innovadoras que impacten positivamente en la sociedad.
                    """)
                ], className="aspiration-card"),
                
                html.Div([
                    html.H4("Formación Académica"),
                    html.P("""
                        Actualmente curso mis estudios en la Universidad Nacional Mayor de San Marcos, 
                        donde me estoy formando en técnicas avanzadas de modelamiento y análisis de datos. 
                        Me especializo en el uso de herramientas como Python, Dash, Plotly y diversas 
                        librerías científicas para el desarrollo de modelos predictivos y visualizaciones 
                        interactivas.
                    """)
                ], className="aspiration-card"),
                
                html.Div([
                    html.H4("Proyectos Futuros"),
                    html.P("""
                        Entre mis planes se encuentra el desarrollo de modelos más complejos que integren 
                        machine learning y análisis de series temporales. También busco colaborar en 
                        proyectos de investigación que utilicen el modelamiento matemático para abordar 
                        problemas sociales y científicos relevantes.
                    """)
                ], className="aspiration-card")
            ], className="aspirations-grid")
        ], className="aspirations-section")
        
    ], className="page-containe-inicio")
])
