import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from callbacks import register_callbacks

# Inicializando o app com temas do Bootstrap e fontes externas
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap'
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, height=device-height"}]
)

# Navbar moderno com gradiente e logo
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/logo.png", height="50px"), width="auto"),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Trabalho de Conclusão de Curso - João Paes",
                            className="ms-2",
                            style={"font-size": "18px", "font-weight": "500"}
                        ),
                        width="auto"
                    ),
                ],
                align="center",
                className="g-0"
            ),
            dbc.Nav(
                [dbc.NavItem(dbc.NavLink("Relatórios", href="#"))],
                className="ms-auto",
                navbar=True
            )
        ],
        fluid=True
    ),
    style={
        "background": "linear-gradient(to right, #4A90E2, #0033A0)",
        "margin-bottom": "5px"
    },
    dark=True
)

# Sidebar (responsiva e altura ajustada)
sidebar = dbc.Col(
    [
        dbc.Card(
            [
                html.H2(
                    "Menu",
                    style={
                        "font-family": "'Roboto', sans-serif",
                        "font-size": "28px",
                        "font-weight": "500",
                        "color": "#ffffff",
                        "text-align": "center",
                        "margin-bottom": "15px"
                    }
                ),
                html.Hr(),
                html.H5(
                    "Selecione um Gráfico:",
                    style={
                        "margin-top": "20px",
                        "font-size": "16px",
                        "color": "#ffffff",
                        "font-weight": "400"
                    }
                ),
                dcc.Dropdown(
                    id='grafico-selector',
                    options=[{'label': f'Gráfico {i}', 'value': i} for i in range(1, 17)],
                    value=1,
                    style={
                        'margin-top': '10px',
                        'padding': '8px',
                        'border-radius': '8px',
                        'border': '1px solid #ccc',
                        'width': '100%'
                    }
                ),
                html.Div(
                    [
                        dbc.Button(
                            [html.I(className="fas fa-arrow-left"), " Anterior"],
                            id="previous-button",
                            n_clicks=0,
                            style={
                                "border-radius": "10px",
                                "padding": "8px 15px",
                                "background": "#4A90E2",
                                "color": "white",
                                "border": "none",
                                "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.2)",
                                "cursor": "pointer",
                                "margin-right": "5px"
                            }
                        ),
                        dbc.Button(
                            ["Próximo ", html.I(className="fas fa-arrow-right")],
                            id="next-button",
                            n_clicks=0,
                            style={
                                "border-radius": "10px",
                                "padding": "8px 15px",
                                "background": "#4A90E2",
                                "color": "white",
                                "border": "none",
                                "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.2)",
                                "cursor": "pointer"
                            }
                        )
                    ],
                    style={
                        "margin-top": "20px",
                        "text-align": "center"
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "Exportar tabela mescla_final",
                            style={
                                "font-size": "14px",
                                "font-weight": "bold",
                                "color": "#ffffff",
                                "margin-bottom": "5px"
                            }
                        ),
                        dbc.Button(
                            html.Img(src="/assets/excel.png", style={"height": "40px"}),
                            id="excel-button",
                            n_clicks=0,
                            style={
                                "border-radius": "6px",
                                "background": "#4A90E2",
                                "color": "white",
                                "border": "none",
                                "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.2)",
                                "cursor": "pointer",
                                "padding": "10px 18px"
                            }
                        ),
                        dcc.Download(id="download-excel-file")
                    ],
                    style={
                        "margin-top": "200px",
                        "text-align": "center"
                    }
                ),
            ],
            style={
                "background": "linear-gradient(to bottom, #4A90E2, #0033A0)",
                "border-radius": "12px",
                "box-shadow": "0 3px 8px rgba(0, 0, 0, 0.2)",
                "padding": "15px",
                "min-height": "90vh"  # Altura ajustada para caber na tela sem barra de rolagem
            }
        )
    ],
    xs=12, sm=12, md=2, lg=2, xl=2
)

# Coluna do gráfico (responsiva e altura reduzida)
graph_col = dbc.Col(
    [
        dcc.Graph(
            id='grafico',
            style={
                "height": "90vh",  # Reduz a altura total do gráfico
                "width": "100%",
                "background-color": "#ffffff",
                "border-radius": "12px",
                "box-shadow": "0 3px 6px rgba(0, 0, 0, 0.1)"
            }
        )
    ],
    xs=12, sm=12, md=10, lg=10, xl=10,
    style={"padding": "0 10px"}
)

# Layout principal
app.layout = html.Div(
    [
        navbar,
        dbc.Row([sidebar, graph_col], className="g-0", style={"margin": "0", "padding": "0"})
    ],
    style={
        "background": "linear-gradient(to bottom, #E3F2FD, #FFFFFF)",
        "padding": "0",
        "overflow-x": "hidden",
        "min-height": "100vh"
    }
)

# Registrar callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)


