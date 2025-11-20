import dash
from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx
import requests
import re 
import random 
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- 1. Registro de la Página ---
dash.register_page(__name__,
                   path='/pagina10',
                   name='series',
                   order=10)

# --- 2. Configuración de la API ---
TVMAZE_SEARCH_URL = 'https://api.tvmaze.com/search/shows'
TVMAZE_SHOWS_URL = 'https://api.tvmaze.com/shows' 

# --- 3. Funciones Helper Mejoradas ---

def build_show_layout(data):
    """
    Toma los datos JSON de una serie y devuelve el layout HTML de Dash con diseño mejorado.
    """
    try:
        resumen = data.get('summary', 'No hay descripción disponible.')
        generos = ", ".join(data.get('genres', []))
        if not generos: generos = "N/A"
        
        rating = data.get('rating', {}).get('average')
        if not rating: 
            rating = "N/A"
            rating_float = 0
        else:
            rating_float = float(rating)
            # Color del rating basado en su valor
            if rating_float >= 8:
                rating_color = "#4CAF50"  
            elif rating_float >= 6:
                rating_color = "#FF9800"  
            else:
                rating_color = "#F44336"  
        poster_url = data.get('image', {}).get('medium', 'https://via.placeholder.com/210x295/6D94C5/FFFFFF?text=No+Image')
        
        # Determinar color de estado
        status = data.get('status', 'N/A')
        status_color = {
            'Running': '#4CAF50',
            'Ended': '#F44336',
            'In Development': '#2196F3',
            'To Be Determined': '#FF9800'
        }.get(status, '#757575')

        layout_resultado = html.Div(className='show-result animated-fadein', children=[
            html.Div(className='show-poster-container', children=[
                html.Img(
                    src=poster_url, 
                    className='show-poster',
                    alt=f"Poster de {data.get('name', 'Serie')}"
                ),
                # Badge de rating
                html.Div(className='rating-badge', children=[
                    html.Span("★", style={'color': '#FFD700', 'marginRight': '3px'}),
                    html.Span(str(rating), style={'color': rating_color if rating != "N/A" else '#757575'})
                ]) if rating != "N/A" else None
            ]),
            html.Div(className='show-details', children=[
                html.H3(data.get('name'), className='show-name'),
                html.Div(className='show-meta-info', children=[
                    html.Span([
                        html.Strong("Estreno: "),
                        data.get('premiered', 'N/A')
                    ], className='meta-item'),
                    html.Span([
                        html.Strong("Estado: "),
                        html.Span(data.get('status', 'N/A'), style={'color': status_color, 'fontWeight': 'bold'})
                    ], className='meta-item'),
                    html.Span([
                        html.Strong("Tipo: "),
                        data.get('type', 'N/A')
                    ], className='meta-item'),
                    html.Span([
                        html.Strong("Idioma: "),
                        data.get('language', 'N/A')
                    ], className='meta-item')
                ]),
                html.Div(className='genres-container', children=[
                    html.Strong("Géneros: ", style={'color': '#2C3E50'}),
                    *[html.Span(genre, className='genre-tag') for genre in data.get('genres', [])]
                ]) if data.get('genres') else None,
                dcc.Markdown(
                    resumen, 
                    className='show-summary',
                    dangerously_allow_html=True
                ),
                
            ])
        ])
        return layout_resultado
    except Exception as e:
        return html.Div(className='error-container', children=[
            html.I(className="fas fa-exclamation-triangle", style={'fontSize': '2em', 'color': '#D32F2F', 'marginBottom': '10px'}),
            html.P(f"Error al cargar la serie: {str(e)}", className='error-message')
        ])

def get_comparison_series(selected_show_data, count=5):
    """
    Obtiene series aleatorias para comparar con la serie seleccionada.
    """
    try:
        comparison_shows = []
        show_ids = set([selected_show_data.get('id')])  
        
        selected_genres = selected_show_data.get('genres', [])
        
        for _ in range(10):  
            if len(comparison_shows) >= count:
                break
                
            random_page = random.randint(0, 30)
            response = requests.get(TVMAZE_SHOWS_URL, params={'page': random_page}, timeout=8)
            response.raise_for_status()
            shows_list = response.json()
            
            if not shows_list:
                continue
                
            for show in shows_list:
                try:
                    if (show and isinstance(show, dict) and 
                        show.get('id') and show.get('name') and 
                        show.get('rating') and show.get('rating', {}).get('average') is not None and
                        show['id'] not in show_ids):
                        
                        show_genres = show.get('genres', [])
                        genre_match = any(genre in selected_genres for genre in show_genres) if selected_genres else False
                        
                        comparison_shows.append({
                            'id': show['id'],
                            'name': show['name'],
                            'rating': show['rating']['average'],
                            'genres': show_genres,
                            'genre_match': genre_match,
                            'image': show.get('image', {}).get('medium')
                        })
                        show_ids.add(show['id'])
                        
                        if len(comparison_shows) >= count + 5: 
                            break
                except (AttributeError, KeyError, TypeError):
                    continue
        
        comparison_shows.sort(key=lambda x: (-x['genre_match'], x['rating'] or 0), reverse=True)
        
        return comparison_shows[:count]
        
    except Exception as e:
        print(f"Error getting comparison series: {e}")
        return []

def create_rating_comparison_chart(selected_show_data, comparison_shows):
    """
    Crea una gráfica de comparación de ratings.
    """
    try:
        if not selected_show_data or not comparison_shows:
            return html.Div(className='chart-error', children=[
                html.P("No hay datos suficientes para generar la comparación.", 
                      style={'textAlign': 'center', 'color': '#666', 'padding': '20px'})
            ])
        
        selected_rating = selected_show_data.get('rating', {}).get('average')
        selected_name = selected_show_data.get('name', 'Serie Seleccionada')
        
        data = []
        
        if selected_rating:
            data.append({
                'Serie': selected_name,
                'Rating': selected_rating,
                'Tipo': 'Serie Actual',
                'Color': '#4a76a8'
            })
        
        for show in comparison_shows:
            if show.get('rating'):
                data.append({
                    'Serie': show['name'],
                    'Rating': show['rating'],
                    'Tipo': 'Comparación',
                    'Color': '#E8DFCA'
                })
        
        if not data:
            return html.Div(className='chart-error', children=[
                html.P("No hay ratings disponibles para comparar.", 
                      style={'textAlign': 'center', 'color': '#666', 'padding': '20px'})
            ])
        
        df = pd.DataFrame(data)
        
        # Crear la gráfica
        fig = go.Figure()
        
        comparison_df = df[df['Tipo'] == 'Comparación']
        if not comparison_df.empty:
            fig.add_trace(go.Bar(
                x=comparison_df['Rating'],
                y=comparison_df['Serie'],
                orientation='h',
                name='Otras Series',
                marker=dict(color='#E8DFCA'),
                hovertemplate='<b>%{y}</b><br>Rating: %{x}/10<extra></extra>'
            ))
        
        selected_df = df[df['Tipo'] == 'Serie Actual']
        if not selected_df.empty:
            fig.add_trace(go.Bar(
                x=selected_df['Rating'],
                y=selected_df['Serie'],
                orientation='h',
                name='Serie Actual',
                marker=dict(color='#4a76a8'),
                hovertemplate='<b>%{y}</b><br>Rating: %{x}/10<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text='📊 Comparación de Ratings',
                x=0.5,
                font=dict(size=18, color='#2C3E50')
            ),
            xaxis=dict(
                title='Rating (0-10)',
                range=[0, 10],
                gridcolor='#f0f0f0',
                zerolinecolor='#ddd'
            ),
            yaxis=dict(
                title='',
                categoryorder='total ascending',
                tickfont=dict(size=11)
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            margin=dict(l=10, r=10, t=60, b=20),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            bargap=0.3
        )
        
        return dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            className='rating-comparison-chart'
        )
        
    except Exception as e:
        print(f"Error creating chart: {e}")
        return html.Div(className='chart-error', children=[
            html.P(f"Error al generar la gráfica: {str(e)}", 
                  style={'textAlign': 'center', 'color': '#D32F2F', 'padding': '20px'})
        ])

def get_initial_show():
    """
    Obtiene una serie aleatoria de la API y construye su layout.
    """
    try:
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                random_page = random.randint(0, 50)
                response_list = requests.get(TVMAZE_SHOWS_URL, params={'page': random_page}, timeout=10)
                response_list.raise_for_status()
                shows_list = response_list.json()
                
                if not shows_list:
                    continue
                    
                valid_shows = []
                for show in shows_list:
                    try:
                        if (show and 
                            isinstance(show, dict) and 
                            show.get('id') and 
                            show.get('name') and 
                            show.get('image')):
                            valid_shows.append(show)
                    except (AttributeError, KeyError, TypeError):
                        continue
                
                if not valid_shows:
                    continue
                    
                random_show = random.choice(valid_shows)
                show_id = random_show.get('id')
                
                if not show_id:
                    continue
                    
                response_detail = requests.get(f"{TVMAZE_SHOWS_URL}/{show_id}", timeout=10)
                response_detail.raise_for_status()
                data = response_detail.json()
                
                if data and isinstance(data, dict) and data.get('name'):
                    return data, create_rating_comparison_chart(data, [])
                    
            except requests.exceptions.RequestException:
                continue
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                continue
        
        return get_welcome_message(), None
        
    except Exception as e:
        print(f"Error loading initial show: {e}")
        return get_welcome_message(), None

def get_welcome_message():
    """Mensaje de bienvenida estilizado"""
    return html.Div(className='welcome-container', children=[
        html.Div(className='welcome-icon', children="🎬"),
        html.H3("¡Bienvenido al Buscador de Series!", className='welcome-title'),
        html.P("Comienza buscando una serie o explora nuestras sugerencias aleatorias.", className='welcome-text'),
        html.Div(className='welcome-features', children=[
            html.Div(className='feature-item', children=[
                html.I(className="fas fa-search", style={'color': '#4a76a8'}),
                html.Span("Busca entre miles de series")
            ]),
            html.Div(className='feature-item', children=[
                html.I(className="fas fa-random", style={'color': '#4a76a8'}),
                html.Span("Descubre series aleatorias")
            ]),
            html.Div(className='feature-item', children=[
                html.I(className="fas fa-chart-bar", style={'color': '#4a76a8'}),
                html.Span("Compara ratings")
            ])
        ])
    ])

def get_random_suggestions(count=8):
    """
    Obtiene 'count' series aleatorias y devuelve una lista de html.Img clickeables.
    """
    suggestions = []
    show_ids = set() 
    try:
        for _ in range(3):
            if len(suggestions) >= count: 
                break
                
            random_page = random.randint(0, 50)
            response = requests.get(TVMAZE_SHOWS_URL, params={'page': random_page}, timeout=10)
            response.raise_for_status()
            shows_list = response.json()
            
            if not shows_list: 
                continue
            
            valid_shows = []
            for show in shows_list:
                try:
                    if (show and 
                        isinstance(show, dict) and 
                        show.get('id') and 
                        show.get('name') and 
                        show.get('image') and 
                        show['image'].get('medium')):
                        valid_shows.append(show)
                except (AttributeError, KeyError, TypeError):
                    continue
            
            if not valid_shows:
                continue
                
            random.shuffle(valid_shows)

            for show in valid_shows:
                try:
                    show_id = show.get('id')
                    poster_url = show.get('image', {}).get('medium')
                    show_name = show.get('name', 'Sin título')
                    
                    if not show_id or not poster_url or show_id in show_ids:
                        continue

                    # Crear un div clickeable completo en lugar de solo la imagen
                    suggestion_card = html.Div(
                        id={'type': 'random-suggestion-card', 'id': show_id},
                        className='suggestion-card',
                        n_clicks=0,
                        children=[
                            html.Img(
                                src=poster_url,
                                className='suggestion-img',
                                alt=f"Poster de {show_name}"
                            ),
                            html.Div(className='suggestion-overlay', children=[
                                html.P(show_name, className='suggestion-title'),
                                html.Span("Click para ver", className='suggestion-hint')
                            ])
                        ]
                    )
                    suggestions.append(suggestion_card)
                    show_ids.add(show_id)
                    
                    if len(suggestions) >= count: 
                        break
                        
                except Exception as e:
                    print(f"Error procesando serie {show.get('id', 'unknown')}: {e}")
                    continue
        
        if not suggestions:
            return html.Div(className='suggestions-error', children=[
                html.I(className="fas fa-exclamation-triangle", style={'marginRight': '8px'}),
                "No se pudieron cargar sugerencias en este momento"
            ])
        
        return html.Div(className='suggestions-grid', children=suggestions)
        
    except Exception as e:
        print(f"Error loading suggestions: {e}")
        return html.Div(className='suggestions-error', children=[
            html.I(className="fas fa-sync-alt", style={'marginRight': '8px'}),
            "Error cargando sugerencias. Intenta actualizar."
        ])

def get_default_dropdown_options():
    """
    Obtiene la primera página de shows para usarla como caché.
    """
    try:
        response = requests.get(TVMAZE_SHOWS_URL, params={'page': 0}, timeout=10)
        response.raise_for_status()
        shows = response.json()
        
        options = []
        for show in shows:
            try:
                if (show and 
                    isinstance(show, dict) and 
                    show.get('name') and 
                    show.get('id')):
                    options.append({'label': f"🎬 {show['name']}", 'value': show['id']})
            except (AttributeError, KeyError, TypeError):
                continue
                
        return options
    except Exception as e:
        print(f"Error loading default options: {e}")
        return []

layout = html.Div(className='series-page-container', children=[
    
    dcc.Store(id='default-options-store'),
    dcc.Store(id='current-show-data'),  
    dcc.Interval(
        id='page-load-interval',
        interval=800,
        max_intervals=1
    ),
    
    html.Div(className='series-header', children=[
        html.Div(className='header-content', children=[
            html.H1("🎬 Buscador de Series", className='main-title'),
            html.P("Descubre y explora miles de series de televisión", className='subtitle'),
            html.Div(className='header-decoration', children=[
                html.Span("•", className='decoration-dot'),
                html.Span("•", className='decoration-dot'),
                html.Span("•", className='decoration-dot')
            ])
        ])
    ]),
    
    html.Div(className='series-main-content wide-search', children=[

        html.Div(className='search-column wide', children=[
            html.Div(className='search-card', children=[
                html.Div(className='card-header', children=[
                    html.H2("🔍 Buscar Series", className='card-title'),
                    html.Div(className='search-icon', children="📺")
                ]),
                
                html.Div(className='search-section', children=[
                    html.Label("Nombre de la Serie", className='input-label'),
                    html.Div(className='search-input-group wide', children=[
                        dcc.Dropdown(
                            id='dropdown-serie-10',
                            placeholder='Escribe el nombre de una serie...',
                            options=[],
                            value=None,
                            className='series-dropdown wide',
                            searchable=True,
                            clearable=True
                        ),
                        html.Button(
                            html.Span(['🔍', html.Span('Buscar', className='btn-text')]),
                            id='btn-buscar-serie-10',
                            n_clicks=0,
                            className='search-button wide'
                        )
                    ]),
                    html.Div(className='search-tips', children=[
                        html.Small("💡 Tip: Escribe al menos 3 caracteres para mejores resultados")
                    ])
                ]),
                
                html.Hr(className='section-divider'),
                
                html.Div(className='suggestions-section', children=[
                    html.Div(className='suggestions-header', children=[
                        html.H3("🎲 Series Recomendadas", className='suggestions-title'),
                        html.Button(
                            html.Span(['🔄', html.Span('Actualizar', className='btn-text')]),
                            id='btn-refresh-suggestions',
                            n_clicks=0,
                            className='refresh-button'
                        )
                    ]),
                    html.Div(id='random-suggestions-container', children=[
                        html.Div(className='loading-suggestions', children=[
                            html.Div(className='loading-spinner'),
                            html.Span("Cargando sugerencias...")
                        ])
                    ])
                ])
            ])
        ]),

        html.Div(className='results-column narrow', children=[
            html.Div(className='results-card', children=[
                html.Div(className='card-header', children=[
                    html.H2("📋 Detalles de la Serie", className='card-title'),
                    html.Div(className='results-stats', id='results-stats', children=[
                        html.Span("Cargando...", className='stats-text')
                    ])
                ]),
                
                dcc.Loading(
                    id='loading-spinner-series',
                    type='circle',
                    color='#4a76a8',
                    children=[
                        html.Div(id='output-resultados-serie-10', children=[
                            html.Div(className='initial-loading', children=[
                                html.Div(className='loading-animation', children=[
                                    html.Div(className='film-strip', children=[
                                        html.Span("🎬"),
                                        html.Span("📺"),
                                        html.Span("🎭"),
                                        html.Span("🌟")
                                    ]),
                                    html.P("Cargando serie aleatoria...", className='loading-text')
                                ])
                            ])
                        ])
                    ]
                ),
                
                html.Div(className='chart-section', children=[
                    html.Hr(className='chart-divider'),
                    html.Div(className='chart-header', children=[
                        html.H3("📊 Comparación de Ratings", className='chart-title'),
                        html.Small("Compara el rating de esta serie con otras similares", 
                                 className='chart-subtitle')
                    ]),
                    html.Div(id='rating-comparison-chart-container', children=[
                        html.Div(className='chart-placeholder', children=[
                            html.I(className="fas fa-chart-bar", 
                                 style={'fontSize': '3em', 'color': '#E8DFCA', 'marginBottom': '15px'}),
                            html.P("Selecciona una serie para ver la comparación de ratings", 
                                 style={'color': '#666', 'textAlign': 'center'})
                        ])
                    ])
                ])
            ])
        ])
    ]),
    
    
])


@dash.callback(
    Output('output-resultados-serie-10', 'children'),
    Output('random-suggestions-container', 'children'),
    Output('default-options-store', 'data'),
    Output('current-show-data', 'data'),
    Input('page-load-interval', 'n_intervals'),
    prevent_initial_call=False
)
def on_page_load(n):
    if n is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
    initial_show_data, _ = get_initial_show()
    initial_show_layout = build_show_layout(initial_show_data) if isinstance(initial_show_data, dict) else initial_show_data
    suggestions_layout = get_random_suggestions()
    default_options = get_default_dropdown_options()
    
    return initial_show_layout, suggestions_layout, default_options, initial_show_data

@dash.callback(
    Output('random-suggestions-container', 'children', allow_duplicate=True),
    Input('btn-refresh-suggestions', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_suggestions(n_clicks):
    if n_clicks:
        return get_random_suggestions()
    return dash.no_update

@dash.callback(
    Output('dropdown-serie-10', 'options'),
    Input('dropdown-serie-10', 'search_value'),
    State('default-options-store', 'data')
)
def update_dropdown_options(search_value, default_options):
    if not search_value or len(search_value) < 2:
        return default_options if default_options else []

    try:
        response = requests.get(TVMAZE_SEARCH_URL, params={'q': search_value}, timeout=10)
        response.raise_for_status()
        search_results = response.json()
        options = [{'label': f"🎬 {result['show']['name']}", 'value': result['show']['id']} 
                  for result in search_results if result['show'].get('name') and result['show'].get('id')]
        return options
    except requests.exceptions.RequestException:
        return []

@dash.callback(
    Output('output-resultados-serie-10', 'children', allow_duplicate=True),
    Output('dropdown-serie-10', 'value'),
    Output('dropdown-serie-10', 'search_value'),
    Output('results-stats', 'children'),
    Output('current-show-data', 'data', allow_duplicate=True),
    Output('rating-comparison-chart-container', 'children'),
    Input('btn-buscar-serie-10', 'n_clicks'),
    Input({'type': 'random-suggestion-card', 'id': ALL}, 'n_clicks'),  # Cambiado a 'random-suggestion-card'
    State('dropdown-serie-10', 'value'),
    prevent_initial_call=True
)
def update_results(btn_n_clicks, card_n_clicks_list, dropdown_value):
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggered_id = ctx.triggered_id
    show_id = None
    error_msg = None

    print(f"Triggered: {triggered_id}")

    if triggered_id == 'btn-buscar-serie-10':
        if not dropdown_value:
            error_msg = "Por favor, selecciona una serie de la lista."
        else:
            show_id = dropdown_value
    
    elif isinstance(triggered_id, dict) and triggered_id.get('type') == 'random-suggestion-card':
        # Obtener el ID directamente del triggered_id
        show_id = triggered_id['id']
        print(f"Clicked suggestion card ID: {show_id}")

    if error_msg:
        error_layout = html.Div(className='error-container', children=[
            html.I(className="fas fa-exclamation-circle"),
            html.P(error_msg, className='error-message')
        ])
        stats = html.Span("❌ Error en búsqueda", className='stats-text error')
        return error_layout, None, "", stats, dash.no_update, dash.no_update

    if not show_id:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    try:
        url_detalle_serie = f"{TVMAZE_SHOWS_URL}/{show_id}"
        print(f"Fetching show details for ID: {show_id}")
        response = requests.get(url_detalle_serie, timeout=10)

        if response.status_code == 404:
            raise requests.exceptions.HTTPError(f"No se encontró la serie con ID '{show_id}'.")
        
        response.raise_for_status() 
        data = response.json()
        print(f"Successfully loaded: {data.get('name')}")
        
        # Stats actualizados
        rating = data.get('rating', {}).get('average', 'N/A')
        stats_text = f"✅ {data.get('name')} • Rating: {rating}/10" if rating != "N/A" else f"✅ {data.get('name')}"
        stats = html.Span(stats_text, className='stats-text success')
        
        # Obtener series para comparación y crear gráfica
        comparison_shows = get_comparison_series(data)
        chart = create_rating_comparison_chart(data, comparison_shows)
        
        return build_show_layout(data), None, "", stats, data, chart

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        error_layout = html.Div(className='error-container', children=[
            html.I(className="fas fa-wifi"),
            html.P(f"Error de conexión: {str(e)}", className='error-message')
        ])
        stats = html.Span("❌ Error de conexión", className='stats-text error')
        return error_layout, None, "", stats, dash.no_update, dash.no_update